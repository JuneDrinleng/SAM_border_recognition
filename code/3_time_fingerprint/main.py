from module import *



# 初始设置
folder_path='3_r_border_data' # 存放所有视频边界文件的文件夹
output_path='3_output_timefinger'# 存放图片的文件夹
sampling_rate=100 #每隔多少帧画一个轮廓

def main():
    folder_path_list,folders_name_list=find_folder_path(folder_path=folder_path)
    format_txt_name(folder_path_list=folder_path_list)
    create_save_img_adjust(folder_path_list=folder_path_list,
                  folders_name_list=folders_name_list,
                  output_path=output_path)



if __name__ == '__main__':
    main()