import os
from tqdm import tqdm


need_to_check_dir = 'data/recognized_border_data'
output_file_path = 'data/recognization_failed_list.txt'
empty_files_list= []
sub_folders = os.listdir(need_to_check_dir)
for sub_folder in tqdm(sub_folders):
    sub_folder_path = os.path.join(need_to_check_dir, sub_folder)
    if os.path.isdir(sub_folder_path):
        files = os.listdir(sub_folder_path)
        for file in (files):
            file_path = os.path.join(sub_folder_path, file)
            if os.path.getsize(file_path) == 0:
                empty_files_list.append(file_path)
    pass
with open(output_file_path, 'w') as file:
    for item in empty_files_list:
        file.write(f"{item}\n")
print(f"Empty files list has been saved to {output_file_path}")
print(f"Total empty files: {len(empty_files_list)}")