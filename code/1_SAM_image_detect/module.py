import os
import tifffile as tiff
from tqdm import tqdm
import psutil
import glob
from segment_anything import SamAutomaticMaskGenerator, sam_model_registry
import cv2 as cv
import numpy as np
import pandas as pd
import torch


def format_memory_size(size):
    # 根据大小自动选择单位
    for unit in ['', 'K', 'M', 'G', 'T']:
        if size < 1024:
            return f"{size:.2f} {unit}B"
        size /= 1024
    return f"{size:.2f} PB"

def load_tif(video_path,frames_dir,output_file_path):
    """目前仅对tiff的page=1时可用"""
    if not os.path.exists(frames_dir):
        os.mkdir(frames_dir)
    tif=tiff.TiffFile(video_path)
    pages_len=len(tif.pages)
    # if pages_len==1:
    if not os.path.exists(output_file_path):
        os.makedirs(output_file_path)
    txt_path=os.path.join(frames_dir, 'frames_num.txt')
    if os.path.exists(txt_path):
        with open(txt_path,'r') as f:
            frames_num=int(f.read())
        # 后续可以添加进一步验证split_video中的文件数目是否等于帧数
        tiff_path=os.path.join(frames_dir, '0000.tiff')
        mats=tiff.imread(tiff_path)
        # print(mats.shape)
        height=mats.shape[0]
        width=mats.shape[1]
        print("已经分割好视频，无需重复分割")
    else:
        mats=tiff.imread(video_path)
        tiff_dic = {key: value for key, value in enumerate(mats)}
        len_tiff_dic = len(tiff_dic)
        # print(mats.shape)
        shapes=mats.shape
        del mats
        frames_num=shapes[0]
        height=shapes[1]
        width=shapes[2]
        print(f"当前进程占用内存：{format_memory_size(psutil.Process(os.getpid()).memory_info().rss)}")
        for i in tqdm(range(0,len_tiff_dic)):
            segment_frame=tiff_dic[i]
            tiff.imwrite(os.path.join(frames_dir, f"{'%04d' % i}.tiff"), segment_frame)
            pass
        with open(txt_path,'w') as f:
            f.write(str(frames_num))
        print("视频分割完成")
    return frames_num,height,width

def count_files(directory):
    """
    计算文件夹中的文件数目，不包含子文件夹
    """
    return len([name for name in os.listdir(directory) if os.path.isfile(os.path.join(directory, name))])

def read_folder(folder_Path,frames_dir,device,frame_num,checkpoint_path,module_name):
    """
    folder_Path:分解的视频帧的文件夹路径
    frames_dir:生成的mask文件夹路径
    device:选择用CPU还是cuda进行运算
    """
    print("现在开始SAM运算生成mask")
    if not os.path.exists(frames_dir):
        os.mkdir(frames_dir)
    files = glob.glob(os.path.join(folder_Path, '*.tiff'))
    # for fileIdx in tqdm(range(len(files))):
    if count_files(frames_dir)>=frame_num-1: # 这里暂时选择的是1s取1帧
        print("已经有生成了的mask")
        print("可以直接利用已生成的mask进行下一步操作")
    else:
        sam = sam_model_registry[module_name](checkpoint=checkpoint_path)
        sam.to(device)
        mask_generator = SamAutomaticMaskGenerator(sam)
        for fileIdx in tqdm(range(0,len(files))):
        # 构建文件的完整路径
            filePath = files[fileIdx]
            im = cv.imread(filePath)
            im = cv.cvtColor(im, cv.COLOR_BGR2RGB)
            masks = mask_generator.generate(im)
            np.save(os.path.join(frames_dir, f"{'%04d' % fileIdx}.npy"),masks)
            del im
            torch.cuda.empty_cache() 
            pass
        print("已经完成mask生成")


def get_mask(frames_dir,frame_series_num):
    """
    frame_series_num是需要提取第几帧的mask数据,从0开始
    """
    files = glob.glob(os.path.join(frames_dir, '*.npy'))
    filePath = files[frame_series_num]
    masks=np.load(filePath,allow_pickle=True)
    return masks

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


def produce_x_y(frame_dir_SAM,height,width,output_file_path,area_ratio_threshold):
    files = glob.glob(os.path.join(frame_dir_SAM, '*.npy'))
    for i in tqdm(range(0,len(files))):
    # for i in tqdm(range(0,100)):
        masks=get_mask(frames_dir=frame_dir_SAM,frame_series_num=i) 
        selected_mask=sorted_masks_by_bbox_threshold(masks=masks,area_ratio_threshold=area_ratio_threshold) 
        boundary_list,x_coords,y_coords=get_mask_border(selected_mask,height=height,width=width)
        name_npy=os.path.basename(files[i])
        txt_filename=name_npy.replace('.npy','.txt')
        txt_path=os.path.join(output_file_path,txt_filename)
        with open(txt_path, 'w') as f:
    # 遍历列表中的每个元组
            for item in boundary_list:
                # 将元组的两个元素转换为字符串，并用制表符连接
                line = "{}\t{}".format(item[0], item[1])
                # 写入文件并添加换行符
                f.write(line + '\n')

def produce_border_cordinates(file_path,out_path,output_file_path,frame_dir_SAM,checkpoint_path,module_name):
    frame_num,height,width=load_tif(video_path=file_path,frames_dir=out_path,output_file_path=output_file_path)
    print(f"当前进程占用内存：{format_memory_size(psutil.Process(os.getpid()).memory_info().rss)}")
    read_folder(folder_Path=out_path,frames_dir=frame_dir_SAM,device = "cuda",frame_num=frame_num,checkpoint_path=checkpoint_path,module_name=module_name) # frame_dir是SAM运算结果的存储路径 #device是GPU还是CPU,GPU则用cuda
    produce_x_y(frame_dir_SAM=frame_dir_SAM,height=height,width=width,output_file_path=output_file_path,area_ratio_threshold=0.7)

def folderization(origin_data_folder_path,
                  Intermediate_variables_folder_path,
                  output_folder_path,
                  checkpoint_path,
                  module_name):
    files = glob.glob(os.path.join(origin_data_folder_path, '*.tif'))
    for fileIdx in range(0,len(files)):
        filePath = files[fileIdx] #完整路径
        file_path = os.path.basename(filePath)
        fileName=(file_path.split('.'))[0]
        out_path=os.path.join(Intermediate_variables_folder_path,fileName+'_split_video')
        frame_dir_SAM=os.path.join(Intermediate_variables_folder_path,fileName+'_mask_npy')
        output_file_path=os.path.join(output_folder_path,fileName+'_output')
        produce_border_cordinates(file_path=filePath, # 待处理数据
                            out_path=out_path,#视频分割成帧存储文件路径
                            output_file_path=output_file_path,# 边界坐标txt文件的存储路径
                            frame_dir_SAM=frame_dir_SAM,# SAM运算结果的存储路径
                            checkpoint_path=checkpoint_path,
                            module_name=module_name)
        print("已经完成第{}个文件的处理".format(fileIdx))

