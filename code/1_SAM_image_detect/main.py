from module import *


# 初始条件设定
origin_data_folder_path='D:\\Lab\\work\\2024\\border_detection_plus\\SAM\\origin_data\\videos'
Intermediate_variables_folder_path="D:\\Lab\\work\\2024\\border_detection_plus\\SAM\\Intermediate_variables"
# output_folder_path='D:\\Lab\\work\\2024\\border_detection_plus\\SAM\\output'
output_folder_path='SAM_image_detect\\debug_output'

checkpoint_path='D:\\Lab\\work\\2024\\border_detection_plus\\SAM\\origin_data\\module\\sam_vit_b_01ec64.pth' #模型路径
module_name='vit_b' # 除此之外还有 'vit_h'和'vit_l'



def main():
    folderization(origin_data_folder_path=origin_data_folder_path,
                  Intermediate_variables_folder_path=Intermediate_variables_folder_path,
                  output_folder_path=output_folder_path,
                  checkpoint_path=checkpoint_path,
                  module_name=module_name)


    print("已经完成所有边界坐标的产生")

if __name__ == '__main__':
    main()
