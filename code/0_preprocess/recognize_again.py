from module import *

import cv2 as cv
import tifffile as tiff

failed_list_path='data/recognization_failed_list.txt'
intermidiate_variables_folder_path='data/Intermediate_variables'
with open(failed_list_path, 'r') as file:
    failed_list = file.read().splitlines()
for file in failed_list:
    file_name=os.path.basename(file)
    file_path=os.path.dirname(file)
    folder_name=file_path.split('\\')[-1] # str
    frame=file_name.split('.')[0] # str
    video=folder_name.split('_')[0] # str

    npy_path=os.path.join(intermidiate_variables_folder_path,f'{video}_mask_npy')
    npy_path=os.path.join(npy_path,f'{frame}.npy')
    tiff_path=os.path.join(intermidiate_variables_folder_path,f'{video}_split_video')
    tiff_path=os.path.join(tiff_path,f'{frame}.tiff')
    im=cv.imread(tiff_path)
    # im_1=cv.imread('data\\Intermediate_variables\\0000_split_video\\0026.tiff') 
    masks=np.load(npy_path,allow_pickle=True)
    # masks_1=np.load('data\\Intermediate_variables\\0000_mask_npy\\0026.npy',allow_pickle=True)
    boundary_list,x_coords,y_coords=get_mask_border(selected_mask=masks[0],height=im.shape[0],width=im.shape[1])
    plt.figure(figsize=(12,16),dpi=100)
    radius=3
    color = (0, 0, 255)  # 红色
    for point in boundary_list:
        x, y = point
        # 确保坐标值在图片范围内
        if 0 <= x < im.shape[1] and 0 <= y < im.shape[0]:
            cv.circle(im, (int(x), int(y)), radius, color, -1)

    cv.imshow('Image with Points', im)
    cv.waitKey(0)
    input_code=input("0 is wrong, 1 is right \n")
    if input_code=='1':
        with open(file, 'w') as f:
            for item in boundary_list:
                # 将元组的两个元素转换为字符串，并用制表符连接
                line = "{}\t{}".format(item[0], item[1])
                # 写入文件并添加换行符
                f.write(line + '\n')
    pass