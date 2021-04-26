import os
import cv2
import numpy as np
from skimage import io
from skimage.color import gray2rgb

file_dir='D:/DataSets/hyperspectraldatasets/424capture/lowlight_Apple_2021-04-24_08-42-16/splitedrgb/'
img_path_name_list = os.listdir(file_dir) #Return a list containing the names of the files in the directory.
print(len(img_path_name_list))
print(type(img_path_name_list))
print(img_path_name_list[0])
video = cv2.VideoWriter('D:/DataSets/hyperspectraldatasets/424capture/lowlight_Apple_2021-04-24_08-42-16/hyper.avi', cv2.VideoWriter_fourcc(*'MJPG'), 10, (640, 480))
"""
方案1：

for i in range(len(img_path_name_list)):

    img = io.imread(file_dir + img_path_name_list[i])
    img = img.astype(np.float32)
    img = (img/2047)*255
    img = img.astype(np.uint8)

    img = cv2.resize(img, (640, 480))
    print(img.shape)
    #img_color = np.stack((img, img, img), 2)
    img_color = gray2rgb(img) #一定要转换成rgb格式才可以写入cv2.VideoWriter
    video.write(img_color)
"""

for i in range(len(img_path_name_list)):

    #img = io.imread(file_dir + img_path_name_list[i])
    img = cv2.imread(file_dir + img_path_name_list[i], cv2.IMREAD_UNCHANGED)
    img = img.astype(np.float32)
    img = (img/2047)*255
    img = img.astype(np.uint8)

    img = cv2.resize(img, (640, 480))
    print(img.shape)

    img_color = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB) ##一定要转换成rgb24格式才可以写入cv2.VideoWriter
    video.write(img_color)

video.release()