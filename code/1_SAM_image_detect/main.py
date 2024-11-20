from module import *






def main():
    folderization(origin_data_folder_path=origin_data_folder_path,
                  Intermediate_variables_folder_path=Intermediate_variables_folder_path,
                  output_folder_path=output_folder_path,
                  checkpoint_path=checkpoint_path,
                  module_name=module_name)


    print("down!")

if __name__ == '__main__':
    # initial path
    origin_data_folder_path='data/origin_data'
    Intermediate_variables_folder_path='data/Intermediate_variables'
    output_folder_path='data/recognized_border_data'
    check_path(output_folder_path)
    check_path(Intermediate_variables_folder_path)

    checkpoint_path='model/sam_vit_b_01ec64.pth' #model path
    module_name='vit_b' # besides: 'vit_h'和'vit_l'
    main()
