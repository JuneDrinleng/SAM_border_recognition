import os
from tqdm import tqdm
import numpy as np
import cv2

def check_file_list(folder_path):
    file_list=os.listdir(folder_path)
    return file_list

def read_txt(txt_path):
    data=np.loadtxt(txt_path)
    return data

def calculate_area_with_image_processing(border):
    # 创建一个空白图像
    image_size=(1600, 1200)
    img = np.zeros(image_size, dtype=np.uint8)
    
    # 将边界点转换为适合绘制的格式
    border_points = np.array(border, dtype=np.int32)
    border_points = border_points.reshape((-1, 1, 2))
    
    # 绘制多边形
    cv2.polylines(img, [border_points], isClosed=True, color=255, thickness=1)
    cv2.fillPoly(img, [border_points], color=255)
    
    # 查找轮廓
    contours, _ = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # 计算面积
    area = cv2.contourArea(contours[0])
    return area