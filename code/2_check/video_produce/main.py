from video_produce import *

fps = 1  #视频帧率
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # 或者根据你的系统选择合适的编码器
tiff_folder_path_total='data\\Intermediate_variables'
txt_folder_path_total='data\\recognized_border_data'
video_output_path='data\\output_video'

def main():
    file_list=os.listdir(txt_folder_path_total)
    for i in (range(0,len(file_list))):
        file_name=file_list[i]
        tiff_name=file_name.split('_')[0]+'_split_video'
        tiff_folder_path=os.path.join(tiff_folder_path_total,tiff_name)
        txt_folder_path=os.path.join(txt_folder_path_total,file_name)
        video_produce(tiff_folder_path=tiff_folder_path,
                    txt_folder_path=txt_folder_path,
                    fourcc=fourcc,
                    video_output_path=video_output_path,
                    frame_rate=fps)


if __name__ == '__main__':
    main()