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
    im_1=cv.imread('data\\Intermediate_variables\\0000_split_video\\0026.tiff') 
    masks=np.load(npy_path,allow_pickle=True)
    masks_1=np.load('data\\Intermediate_variables\\0000_mask_npy\\0026.npy',allow_pickle=True)
    plt.figure(figsize=(12,16),dpi=100)
    plt.imshow(im_1)
    show_anns(masks_1)
    plt.show() 
    pass