import os
from tqdm import tqdm
import pandas as pd

# Rename all files in a directory
origin_data_dir='./data/origin_data'
new_data_list=[]

file_list=os.listdir(origin_data_dir)
for i in tqdm(range(len(file_list))):
    file=file_list[i]
    origin_file_name=file.split('.')[0]
    file_type=file.split('.')[1]
    new_file_name=f"{i:04d}"
    new_file=f"{new_file_name}.{file_type}"
    new_data_list.append(new_file)
    os.rename(f"{origin_data_dir}/{file}",f"{origin_data_dir}/{new_file}")
    pass

df=pd.DataFrame({'old_name':file_list,'new_name':new_data_list})
df.to_excel('./data/ComparisonTable.xlsx',index=False)

