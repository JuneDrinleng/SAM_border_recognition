from video_produce import *

fps = 1  #视频帧率
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # 或者根据你的系统选择合适的编码器
tiff_folder_path='D:\\Lab\\work\\AnalysisChemistry_WorkCode\\YOLO_detect\\Intermediate_variables'
txt_folder_path='D:\\Lab\\work\\AnalysisChemistry_WorkCode\\YOLO_detect\\output\\flow_0204output'
video_output_path='D:\\Lab\\work\\AnalysisChemistry_WorkCode\\YOLO_detect\\output\\video'

def main():
    video_produce(tiff_folder_path=tiff_folder_path,
                  txt_folder_path=txt_folder_path,
                  fourcc=fourcc,
                  video_output_path=video_output_path,
                  frame_rate=fps)


if __name__ == '__main__':
    main()