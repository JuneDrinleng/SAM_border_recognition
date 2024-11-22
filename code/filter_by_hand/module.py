import os
import numpy as np
import cv2

def check_path(path):
    if not os.path.exists(path):
        os.makedirs(path)

def Canny_edge_detect(img,
                      threshold1:int | None = 30,
                      threshold2:int | None = 90):
    """
    应用Canny边缘检测
    """
    # 得到灰度图
    gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # 应用Canny边缘检测
    edges = cv2.Canny(gray_image, threshold1, threshold2)
    # 提取边界坐标
    y_coords, x_coords = np.where(edges != 0)
    # print(x_coords)
    # # 将坐标存储为(x, y)对的列表
    boundary_points = list(zip(x_coords, y_coords))
    return boundary_points,x_coords,y_coords

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

def draw_border(input_img_path,border):
    img=cv2.imread(input_img_path)
     # 颜色和线条宽度可自定义
    color = (0, 0, 255)  # 红色

    radius=3
    for point in border:
        x, y = point
        # 确保坐标值在图片范围内
        if 0 <= x < img.shape[1] and 0 <= y < img.shape[0]:
            cv2.circle(img, (int(x), int(y)), radius, color, -1)
    return img

def write_txt(txt_path,boundary_list,area):
    with open(txt_path, 'w') as f:
    # 遍历列表中的每个元组
        for item in boundary_list:
            # 将元组的两个元素转换为字符串，并用制表符连接
            line = "{}\t{}".format(item[0], item[1])
            # 写入文件并添加换行符
            f.write(line + '\n')
        line_area = "area:{}".format(area)
        f.write(line_area + '\n')