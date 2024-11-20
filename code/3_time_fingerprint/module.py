import glob
import os
from tqdm import tqdm
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import imageio
import math

def get_file_path(directory):
    '''
    生成该文件夹下特定后缀的文件的路径的列表
    :param directory: 要读取的文件夹路径
    :return: 一个列表，列表内是该文件夹下的每个文件的路径
    '''
    files = glob.glob(os.path.join(directory, '*.txt'))
    # 此处需要寻找的是tiff后缀的，当然还可以是其他后缀例如txt等
    return files

def find_folder_path(folder_path):
    '''
    生成该文件夹下所有子文件夹的路径
    :return: 一个列表，列表内是该文件夹下的每个文件夹的路径
    '''
    folders_paths = []
    folders_name=[]
    for root, dirs, files in os.walk(folder_path):
        for dir_name in dirs:
            subfolder_path = os.path.join(root, dir_name)
            folders_paths.append(subfolder_path)
            folder_name=os.path.basename(subfolder_path)
            folders_name.append(folder_name)
            # folders_path是文件夹内子文件夹的路径
            # folders_name是文件夹内子文件夹的文件名
    return folders_paths,folders_name

def create_folder(frames_dir):
    '''
    若干文件夹所在的路径不存在该文件夹，则于该路径创建文件夹
    :param frames_dir: frames_dir: 是该文件夹所在的路径
    '''
    if not os.path.exists(frames_dir):
            os.mkdir(frames_dir)

def read_txt(txt_path):
    sepect_data=np.loadtxt(txt_path)
    x=sepect_data[:,0]
    y=sepect_data[:,1]
    return x,y

def create_save_img(folder_path_list,folders_name_list,output_path,sampling_rate):
    """
    每隔多少帧，读取一次边界信息生成图片
    """
    create_folder(frames_dir=output_path)
    for fileidx in tqdm(range(len(folder_path_list))):
        file_path=folder_path_list[fileidx] #需要处理的视频的边界文件夹的路径
        file_name=folders_name_list[fileidx] # 需要处理的视频的边界信息存储文件夹的文件名，用于做以后的输出文件命
        output_file_path=os.path.join(output_path,file_name+'.png') # 输出文件结果的路径 但是需要注意的是，此时的路径是不包括文件后缀的
        files_list=get_file_path(file_path) # 获取文件夹下所有文件的路径
        files_list = [file for file in files_list if os.path.basename(file) != 'frames_num.txt']
        colors=sns.color_palette("viridis", len(files_list))

        plt.figure(figsize=(10, 10))
        
        # 读取并绘制每个 txt 文件的边界
        for txtidx in range(0,len(files_list),sampling_rate):
            txt_path=files_list[txtidx]
            x,y=read_txt(txt_path)
            plt.scatter(x,y, color=colors[txtidx],s=3)
        plt.savefig(output_file_path)
        pass

def fibonacci(maximum):
    fib_sequence = [0, 1]
    while fib_sequence[-1] + fib_sequence[-2] <= maximum:
        fib_sequence.append(fib_sequence[-1] + fib_sequence[-2])
    return fib_sequence[:-1] if fib_sequence[-1] > maximum else fib_sequence
def create_save_img_adjust(folder_path_list,folders_name_list,output_path):
    """
    调整抽帧规则，使得前面比等额抽帧密集，后面比等额抽帧系稀疏，读取一次边界信息生成图片
    """
    create_folder(frames_dir=output_path)
    for fileidx in tqdm(range(len(folder_path_list))):
        file_path=folder_path_list[fileidx] #需要处理的视频的边界文件夹的路径
        file_name=folders_name_list[fileidx] # 需要处理的视频的边界信息存储文件夹的文件名，用于做以后的输出文件命
        output_file_path=os.path.join(output_path,file_name+'.png') # 输出文件结果的路径 但是需要注意的是，此时的路径是不包括文件后缀的
        files_list=get_file_path(file_path) # 获取文件夹下所有文件的路径
        files_list = [file for file in files_list if os.path.basename(file) != 'frames_num.txt']
        # colors=sns.color_palette("viridis", len(files_list))
        colors=sns.color_palette("RdBu", len(files_list))
        # 假设有一个连续的数值变量来对应文件列表
        # data_values = np.linspace(0, 1, len(files_list))

        # # 使用完整的 viridis 色彩映射，并将它应用到这些数值上
        # colors = sns.cubehelix_palette(len(files_list), start=0, rot=-.5) # 或者继续使用 'viridis'
        # norm = plt.Normalize(min(data_values), max(data_values))
        # colors = [sns.desaturate(color, p) for p, color in zip(norm(data_values), sns.color_palette("viridis", len(files_list)))]

        plt.figure(figsize=(10, 10))
        plt.xlim(0,1300)
        plt.ylim(0,1300)
        length=len(files_list)
        # lenghth=30
        # 读取并绘制每个 txt 文件的边界
        for txtidx in range(0,30):
            txtidx=int(txtidx)
            fi=int(90000*math.exp(0.1485*txtidx-math.log(3000)))
            # fi=txtidx
            txt_path=files_list[fi]
            x,y=read_txt(txt_path)
            plt.scatter(x,y, color=colors[fi],s=3)
        plt.savefig(output_file_path)
        pass
def pad_number_to_four_digits(number):
    return "{:04d}.txt".format(int(number))
def format_txt_name(folder_path_list):
    for fileidx in tqdm(range(0,len(folder_path_list))):
        folder_path=folder_path_list[fileidx]
        files_list=glob.glob(os.path.join(folder_path, '*.txt'))
        for i in range(0,len(files_list)):
            file_path=files_list[i]
            file_name=os.path.basename(file_path)
            file_name= pad_number_to_four_digits(os.path.splitext(file_name)[0])
            file_path_new=os.path.join(folder_path,file_name)
            os.rename(file_path,file_path_new)
        pass
def check_for_video(files_list,output_path):
    frames=[]
    for txtidx in range(len(files_list)):
        txt_path=files_list[txtidx]
        x,y=read_txt(txt_path)
        frames.append((x,y))

    def update(frames_number):
        x_coord, y_coord = frames[frames_number]
        plt.scatter(x_coord, y_coord)
        return plt.gcf()

    # 初始化 figure 和 axes
    fig, ax = plt.subplots(figsize=(10, 10))

    # 使用 imageio 导出动画为 mp4 视频
    with imageio.get_writer(output_path, fps=30) as writer:
        for i in range(len(frames)):
            fig.clear()  # 清除上一帧内容
            frame = update(i)
            # 将当前帧转换为 RGB 图像并写入视频
            buffer = fig.canvas.buffer_rgba()
            image = np.array(buffer).copy()
            writer.append_data(image[:, :, :3])  # 只保留 RGB 通道

    # 关闭 figure，完成视频导出
    plt.close(fig)
