from module import *


def main():
    area_df = pd.DataFrame(np.nan, index=range(60), columns=[]) # 60 max frame num
    area_df=folderization(origin_data_folder_path=origin_data_folder_path,
                  Intermediate_variables_folder_path=Intermediate_variables_folder_path,
                  output_folder_path=output_folder_path,
                  checkpoint_path=checkpoint_path,
                  module_name=module_name,area_df=area_df)
    area_output_path=os.path.join(output_folder_path,'area.xlsx')
    area_df.to_excel(area_output_path)

    print("down!")

if __name__ == '__main__':
    # initial path
    origin_data_folder_path='data/origin_data_1'
    Intermediate_variables_folder_path='data/Intermediate_variables_1'
    output_folder_path='data/recognized_border_data_1'
    check_path(output_folder_path)
    check_path(Intermediate_variables_folder_path)

    checkpoint_path='model/sam_vit_b_01ec64.pth' #model path
    module_name='vit_b' # besides: 'vit_h'和'vit_l'
    main()
