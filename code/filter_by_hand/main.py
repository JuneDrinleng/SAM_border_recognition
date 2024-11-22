from module import *
from tqdm.auto import tqdm

def main():
    for npy in tqdm(npy_list):
        video_name=os.path.basename(npy).split('_')[0]
        video_output_folder=os.path.join(output_folder,video_name+'_output')
        check_path(video_output_folder)
        border_output_folder=os.path.join(video_output_folder,'border')
        check_path(border_output_folder)
        check_output_folder=os.path.join(video_output_folder,'check')
        check_path(check_output_folder)
        npy_file_list=os.listdir(npy)
        video_path=os.path.join(npy_parents_folder,video_name+'_split_video')
        for npy_file in tqdm(npy_file_list):
            frame=(npy_file.split('_')[0]).split('.')[0]
            npy_file_path=os.path.join(npy,npy_file)
            masks=np.load(npy_file_path,allow_pickle=True)
            masks_num=len(masks)

            frame_path=os.path.join(video_path,frame+'.tiff')
            for i in (range(masks_num)):
                segment=masks[i]['segmentation']
                area=masks[i]['area']
                boundary_points,x_coords,y_coords=get_mask_border(masks[i],height=segment.shape[0],width=segment.shape[1])
                img_drawed=draw_border(frame_path,boundary_points)
                img_name=frame+'_'+str(i)+'.png'
                img_path=os.path.join(check_output_folder,img_name)
                cv2.imwrite(img_path,img_drawed)
                txt_filename=frame+'_'+str(i)+'.txt'
                txt_path=os.path.join(border_output_folder,txt_filename)
                write_txt(txt_path,boundary_points,area)

                pass

if __name__ == '__main__':
    npy_parents_folder='data/Intermediate_variables'
    output_folder='data/check_by_hand_results'
    if os.path.exists(output_folder)==False:
        os.makedirs(output_folder)
    folder_list=os.listdir(npy_parents_folder)
    npy_list=[]
    for file in folder_list:
        if '_npy' in file:
            file_path=os.path.join(npy_parents_folder,file)
            npy_list.append(file_path)
            pass
    main()
    print('done')