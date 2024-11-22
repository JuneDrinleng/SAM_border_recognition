import glob
from tqdm import tqdm
import numpy as np
import os
import matplotlib.pyplot as plt
import cv2 as cv

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

def get_mask_border(selected_mask,height,width):
    """
    获取掩模的边缘坐标
    """
     # 得到整个菌落的坐标（既包括边界又包括内部）
    selected_mask_segmentation = selected_mask['segmentation']
    coordinates = np.argwhere(selected_mask_segmentation)
    x=coordinates[:,0]
    y=coordinates[:,1]

    # 创建一个全黑的图像数组
    image = np.zeros((height, width, 3), dtype=np.uint8)

    # 在图像上标记坐标点
    for x, y in coordinates:
        # 填充像素，这里以白色为例
        image[x, y] = [255, 255, 255]
    boundary_list,x_coords,y_coords=Canny_edge_detect(image)
    return boundary_list,x_coords,y_coords

def Canny_edge_detect(img,
                      threshold1:int | None = 30,
                      threshold2:int | None = 90):
    """
    应用Canny边缘检测
    """
    # 得到灰度图
    gray_image = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    # 应用Canny边缘检测
    edges = cv.Canny(gray_image, threshold1, threshold2)
    # 提取边界坐标
    y_coords, x_coords = np.where(edges != 0)
    # print(x_coords)
    # # 将坐标存储为(x, y)对的列表
    boundary_points = list(zip(x_coords, y_coords))
    return boundary_points,x_coords,y_coords

def get_mask(frames_dir,frame_series_num):
    """
    frame_series_num是需要提取第几帧的mask数据,从0开始
    """
    files = glob.glob(os.path.join(frames_dir, '*.npy'))
    filePath = files[frame_series_num]
    masks=np.load(filePath,allow_pickle=True)
    return masks

# def produce_x_y(frame_dir_SAM,height,width,output_file_path,area_ratio_threshold):
#     files = glob.glob(os.path.join(frame_dir_SAM, '*.npy'))
#     for i in tqdm(range(0,len(files))):
#     # for i in tqdm(range(0,100)):
#         masks=get_mask(frames_dir=frame_dir_SAM,frame_series_num=i) 
#         selected_mask=sorted_masks_by_bbox_threshold(masks=masks,area_ratio_threshold=area_ratio_threshold) 
#         name_npy=os.path.basename(files[i])
#         txt_filename=name_npy.replace('.npy','.txt')
#         txt_path=os.path.join(output_file_path,txt_filename)
#         try:
#             boundary_list,x_coords,y_coords=get_mask_border(selected_mask,height=height,width=width)
#             with open(txt_path, 'w') as f:
#             # 遍历列表中的每个元组
#                 for item in boundary_list:
#                     # 将元组的两个元素转换为字符串，并用制表符连接
#                     line = "{}\t{}".format(item[0], item[1])
#                     # 写入文件并添加换行符
#                     f.write(line + '\n')
#         except:
#             with open(txt_path, 'w') as file:
#                 pass

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