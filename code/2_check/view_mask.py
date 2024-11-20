import numpy as np
import matplotlib.pyplot as plt
from segment_anything import SamAutomaticMaskGenerator, sam_model_registry
import cv2 as cv
import math


masks = np.load('D:\\Lab\\work\\2024\\border_detection_plus\\SAM\Intermediate_variables\\flow_0204_mask_npy\\0014.npy', allow_pickle=True) 
im=cv.imread('D:\\Lab\work\\2024\\border_detection_plus\\SAM\Intermediate_variables\\flow_0204_split_video\\0014.tiff')

def show_anns(anns):
    if len(anns) == 0:
        return
    sorted_anns = sorted(anns, key=(lambda x: x['area']), reverse=True)
    ax = plt.gca()
    ax.set_autoscale_on(False)

    img = np.ones((sorted_anns[0]['segmentation'].shape[0], sorted_anns[0]['segmentation'].shape[1], 4))
    img[:,:,3] = 0
    for ann in sorted_anns:
        m = ann['segmentation']
        color_mask = np.concatenate([np.random.random(3), [0.35]])
        img[m] = color_mask
    ax.imshow(img)

def sorted_masks(
    area_rank: int | None = None
):
    """
    根据面积降序排序掩模列表  →在bbox里面不是最长的，但又是面积最大的
    """
    if area_rank is None:
        area_rank=1
    # 根据面积降序排序masks列表
    sorted_masks = sorted(masks, key=lambda x: x['area'], reverse=True)

    # 选择面积第二大的掩模
    selected_mask = sorted_masks[area_rank]
    return selected_mask

def sorted_masks_BboxAndArea(masks):

    # 计算每个 mask 的 bbox 大小并找到最大的那个
    max_bbox_length = 0
    max_bbox_index = -1

    for i, mask in enumerate(masks):
        bbox = mask["bbox"]  # 假设 bbox 格式为 [x, y, width, height]
        x1, y1 = float(bbox[0]), float(bbox[1])
        x2, y2 = float(bbox[2]), float(bbox[3])
        bbox_length=math.hypot(x2 - x1, y2 - y1)
        if bbox_length > max_bbox_length:
            max_bbox_length = bbox_length
            max_bbox_index = i

    # 从列表中移除 bbox 最大的 mask
    if max_bbox_index >= 0:
        # del masks[max_bbox_index] # 无法对读取的npy进行del
        masks=np.delete(masks,max_bbox_index)

    # 在剩余的 masks 中找到 area 最大的 mask
    max_area = 0
    max_area_mask = None
    for mask in masks:
        if mask["area"] > max_area:
            max_area = mask["area"]
            max_area_mask = mask
    return max_area_mask

def sorted_masks_only_bbox(masks):
    # 初始化最大和第二大的 bbox 长度及其索引
    max_bbox_length = 0
    second_max_bbox_length = 0
    max_bbox_index = -1
    second_max_bbox_index = -1
    bbox_length_list=[]
    for i, mask in enumerate(masks):
        bbox = mask["bbox"]  
        x2, y2 = float(bbox[2]), float(bbox[3])
        # bbox_length = math.hypot(x2 - x1, y2 - y1)
        bbox_length=x2+y2
        bbox_length_list.append(bbox_length)
        # 更新最大和第二大的 bbox
        if bbox_length > max_bbox_length:
            second_max_bbox_length = max_bbox_length
            second_max_bbox_index = max_bbox_index
            max_bbox_length = bbox_length
            max_bbox_index = i
        elif bbox_length > second_max_bbox_length:
            second_max_bbox_length = bbox_length
            second_max_bbox_index = i
        
    # 返回具有第二大 bbox 的 mask
    if second_max_bbox_index >= 0:
        return masks[second_max_bbox_index]
    else:
        return None
    

def sorted_masks_by_bbox_threshold(masks,area_ratio_threshold):
    def calculate_bbox_length(bbox):
        # 计算 bbox 对角线长度
        x1, y1, width, height = bbox
        return width+height
    # 去除 bbox_length 最长的 mask
    masks = sorted(masks, key=lambda x: calculate_bbox_length(x['bbox']), reverse=True)
    masks.pop(0)

    # 筛选面积占 bbox 面积的比例大于阈值的 mask
    filtered_masks = []
    for mask in masks:
        bbox_area = mask['bbox'][2] * mask['bbox'][3]
        area_ratio = mask['area'] / bbox_area
        if area_ratio >= area_ratio_threshold:
            filtered_masks.append(mask)

    # 在剩下的 mask 中挑选 bbox_length 长的
    if filtered_masks:
        selected_mask = max(filtered_masks, key=lambda x: calculate_bbox_length(x['bbox']))
        return selected_mask
    else:
        return None


selected_mask=sorted_masks_by_bbox_threshold(masks=masks,area_ratio_threshold=0.70)
# selected_mask=sorted_masks_only_bbox(masks=masks)


selected_mask_segmentation = selected_mask['segmentation']
coordinates = np.argwhere(selected_mask_segmentation)

x=coordinates[:,0]
y=coordinates[:,1]





import matplotlib.pyplot as plt
plt.figure(figsize=(12,16),dpi=100)
plt.imshow(im)
show_anns(masks)
plt.show() 

# # 确定目标图像的尺寸
height = 1200  # 高度
width = 1600   # 宽度
# 创建一个全黑的图像数组
image = np.zeros((height, width, 3), dtype=np.uint8)

# 在图像上标记坐标点
for x, y in coordinates:
    # 填充像素，这里以白色为例
    image[x, y] = [255, 255, 255]

gray_image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
img=gray_image
# 应用Canny边缘检测
edges = cv.Canny(img, threshold1=30, threshold2=90)
# 提取边界坐标
y_coords, x_coords = np.where(edges != 0)
# print(x_coords)
# # 将坐标存储为(x, y)对的列表
boundary_points = list(zip(x_coords, y_coords))

plt.scatter(x_coords,y_coords, color='red')

plt.xlim(min(x_coords)-10, max(x_coords)+10)
plt.ylim(min(y_coords)-10, max(y_coords)+10)

# 设置横纵坐标轴比例相等
plt.gca().set_aspect('equal', adjustable='box')

# 反转Y轴
plt.gca().invert_yaxis()

# 添加标题和标签
plt.title("Graph of X and Y")
plt.xlabel("X")
plt.ylabel("Y")

# 显示图形
plt.show()
x=x_coords.tolist()
y=y_coords.tolist()
img=im
coordinates_new=[]
for i in range(len(x)):
    xi=float(x[i])
    yi=float(y[i])
    coordinates_new.append((xi, yi))
radius=3
color = (0, 0, 255)  # 红色
for point in coordinates_new:
    x, y = point
    # 确保坐标值在图片范围内
    if 0 <= x < img.shape[1] and 0 <= y < img.shape[0]:
        cv.circle(img, (int(x), int(y)), radius, color, -1)

cv.imshow('Image with Points', img)
cv.waitKey(0)