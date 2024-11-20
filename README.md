# SAM_border_recognition
 this is the final edition of recognizing the bacteria's border using SAM(Segment Anything Meta)+ Canny detecting algorithm

## code introduction

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

the [0_preprocess](./data/0_preprocess) is used to rename the file, we can use [rename.py](./code/0_preprocess/rename.py) to realize it


the [1_SAM_image_detect](./code/1_SAM_image_detect) is used to get the border data

the [2_check](./code/2_check) is used to generate the check video of the above generated data

the [3_time_fingerprint](./code/3_time_fingerprint) is used to draw time finger plot

the [4_timefinger_bar_drawing](./code/4_timefinger_bar_drawing) is used to draw the scale bar of the time-finger plot

## data storage

all the data are stored in the [data](./data) folder

the distribution is given in the following:
├─output_timefinger
│  
├─check_result
│  
├─origin_data
│  
└─recognized_border_data

the [origin_data](./data/origin_data)  is used to store the output of origin data. each data's format is tiff

the [recognized_border_data](./data/recognized_border_data) is used to store the output of [1_SAM_image_detect](./code/1_SAM_image_detect) 

the [check_result](./data/check_result) is used to store the output of [2_check](./code/2_check)

the [output_timefinger](./data/output_timefinger) is used to store the output of  [3_time_fingerprint](./code/3_time_fingerprint)
