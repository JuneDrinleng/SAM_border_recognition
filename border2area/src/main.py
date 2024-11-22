from utils import *
from matplotlib import pyplot as plt
import pandas as pd

def main():

    print("This is the code to calculate area from border data!")
    data_folder_path=r'data/recognized_border_data'
    video_data_list=check_file_list(data_folder_path)
    scale=1*5.86/0.7*0.001 #mm/pixel
    df=pd.DataFrame()
    for video_data in tqdm(video_data_list):
        video_data_path=os.path.join(data_folder_path,video_data)
        border_data_list=check_file_list(video_data_path)
        video_area_list=[]
        for border_data in tqdm(border_data_list):
            border_data_path=os.path.join(video_data_path,border_data)
            border=read_txt(border_data_path)
            area = calculate_area_with_image_processing(border)*scale*scale
            video_area_list.append(area)
        video_area_data=np.array(video_area_list)
        plt.plot(video_area_list,label=video_data)
        df[video_data]= pd.Series(video_area_data[:2800])#from frame0 to frame2800
    # plt.legend()
    # plt.savefig('results\\visualization_results\\result.png')
    df.to_excel('data\\results\\calculate_result\\video_areas.xlsx', index=True)
    print("The results have been saved in the results folder!")


if __name__ == '__main__':

    main()