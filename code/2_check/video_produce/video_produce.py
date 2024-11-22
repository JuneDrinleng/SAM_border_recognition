import cv2
import numpy as np
import glob
import os
from tqdm import tqdm

def read_txt(points_path):
    sepect_data=np.loadtxt(points_path)
    if sepect_data.size==0:
        x=np.zeros(256)
        y=np.zeros(256)
    else:
        x=sepect_data[:,0]
        y=sepect_data[:,1]
    return x,y

def check_path(path):
    '''
    检查路径是否存在，若不存在则创建
    :param path: 要检查的路径
    :return: None
    '''
    if not os.path.exists(path):
        os.makedirs(path)

def get_file_path_tiff(directory):
    '''
    生成该文件夹下特定后缀的文件的路径的列表
    :param directory: 要读取的文件夹路径
    :return: 一个列表，列表内是该文件夹下的每个文件的路径
    '''
    files = glob.glob(os.path.join(directory, '*.tiff'))
    # 此处需要寻找的是tiff后缀的，当然还可以是其他后缀例如txt等
    return files
def get_file_path_txt(directory):
    '''
    生成该文件夹下特定后缀的文件的路径的列表
    :param directory: 要读取的文件夹路径
    :return: 一个列表，列表内是该文件夹下的每个文件的路径
    '''
    files = glob.glob(os.path.join(directory, '*.txt'))
    # 此处需要寻找的是tiff后缀的，当然还可以是其他后缀例如txt等
    return files

def pad_number_to_four_digits(number):
    return "{:04d}.txt".format(int(number))
def format_txt_name(folder_path):
    files_list=glob.glob(os.path.join(folder_path, '*.txt'))
    for i in range(0,len(files_list)):
        file_path=files_list[i]
        file_name=os.path.basename(file_path)
        file_name= pad_number_to_four_digits(os.path.splitext(file_name)[0])
        file_path_new=os.path.join(folder_path,file_name)
        os.rename(file_path,file_path_new)
    pass


def video_produce(
    frame_rate,# 生成视频的fps
    tiff_folder_path,# 每一帧图片所在的文件夹的路径
    txt_folder_path,# 每一帧图片对应的边界所在的文件夹的路径
    fourcc,#视频编码 #fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # 或者根据你的系统选择合适的编码器
    video_output_path,#视频生成的输出路径
    

):
    file_name=os.path.basename(txt_folder_path)
    video_output_path=os.path.join(video_output_path,file_name+'.mp4')
    img_list=get_file_path_tiff(tiff_folder_path)
    point_list=get_file_path_txt(txt_folder_path)
    format_txt_name(folder_path=txt_folder_path)
    # print('文件命名格式转换完成')
    point_list=get_file_path_txt(txt_folder_path)
    point_list = [file for file in point_list if os.path.basename(file) != 'frames_num.txt']
    height, width, layers = cv2.imread(img_list[0]).shape #读取第一张图片的格式来作为视频帧的格式
    video_writer = cv2.VideoWriter(video_output_path, fourcc, frame_rate, (width, height))
    if len(img_list)!=len(point_list):
        print('error')
    else:
        for i in (range(len(img_list))):
            img=cv2.imread(img_list[i])
            points_path=point_list[i]
            x,y=read_txt(points_path)
            # 颜色和线条宽度可自定义
            color = (0, 0, 255)  # 红色
            coordinates=[]
            # 在原图上画出坐标点
            for i in range(len(x)):
                xi=float(x[i])
                yi=float(y[i])
                coordinates.append((xi, yi))
            radius=3
            for point in coordinates:
                x, y = point
                # 确保坐标值在图片范围内
                if 0 <= x < img.shape[1] and 0 <= y < img.shape[0]:
                    cv2.circle(img, (int(x), int(y)), radius, color, -1)
            video_writer.write(img)
            pass
    video_writer.release()
    # print('视频生成完成')