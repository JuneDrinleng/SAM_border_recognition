# SAM_border_recognition
 this is the final edition of recognizing the bacteria's border using SAM(Segment Anything Meta)+ Canny detecting algorithm

## 1 code introduction

the code is stored in the [code](./code)，its iner distribution we can use the following file tree to represent:

├─0_preprocess  
│   
├─1_SAM_image_detect  
│  
├─2_check  
│  └─video_produce  
│       
├─3_time_fingerprint  
│    
└─4_timefinger_bar_drawing  

the [0_preprocess](./data/0_preprocess) is used to rename the file, we can use [rename.py](./code/0_preprocess/rename.py) to realize it. The name comparisiontable is stored in the [rename_table](./data/ComparisionTable.xlsx)

the [1_SAM_image_detect](./code/1_SAM_image_detect) is used to get the border data. After using it to recognize, we need to check the recognization failed frame, and we can use the [count_blank_files.py](./code/0_preprocess/count_blank_files.py) to achieve it

after checking the failure files, we need to change the filters to recoginzed again

this code doesn't use the streaming reading, so it will cost plenty of memory

the [2_check](./code/2_check) is used to generate the check video of the above generated data

the [3_time_fingerprint](./code/3_time_fingerprint) is used to draw time finger plot

the [4_timefinger_bar_drawing](./code/4_timefinger_bar_drawing) is used to draw the scale bar of the time-finger plot

## 2 data storage

all the data are stored in the [data](./data) folder  

the distribution is given in the following:  
├─output_timefinger  
│  
├─check_result  
│  
├─origin_data  
│  
├─ComparisonTable.xlsx  
│    
├─output_video  
│    
├─Intermediate_variables  
│    
├─output_video  
│    
└─recognized_border_data  

the [origin_data](./data/origin_data)  is used to store the output of origin data. each data's format is tiff  

the [recognized_border_data](./data/recognized_border_data) is used to store the output of [1_SAM_image_detect](./code/1_SAM_image_detect)   

the [check_result](./data/check_result) is used to store the output of [2_check ](./code/2_check) 

the [output_timefinger](./data/output_timefinger) is used to store the output of [3_time_fingerprint](./code/3_time_fingerprint)  

the [ComparisonTable.xlsx](./data\ComparisonTable.xlsx) stores the rename results

the [output_video](./data\output_video) stores the check results video

the [Intermediate_variables](./data\Intermediate_variables) stores the intermediate variables, such as tiff img used to draw checking image, npy the SAM get

the [check_by_hand_results](./data\check_by_hand_results) stores the re-filter results, including all the border/area and check img

## 3 model

all the model can be downloaded from https://github.com/facebookresearch/segment-anything?tab=readme-ov-file  

you can choose 1 model fit your situation best to use  

this folder [model](./model) is used to store the model downloading from the  above website  

## 4 Workflow

1. rename：using [rename.py](./code/0_preprocess/rename.py) to rename all the data into 0000,0001 such format  
2. generate npy: using [main.py](./code/1_SAM_image_detect/main.py) to get all the npy mask data stored in[Intermediate_variables](./data\Intermediate_variables)  
3. check: using [check](./code/2_check) to generate check video  
4. re-filter: using [filtered_by_hand](./code\filter_by_hand) to generate all the border we recognize and all the check image. the area and border are include in the result in [check_by_hand_results](./data\check_by_hand_results) ,area data is in the bottom of the border txt file  

