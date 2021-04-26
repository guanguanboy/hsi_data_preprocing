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
for i in range(len(img_path_name_list)):

    img = io.imread(file_dir + img_path_name_list[i])
    img = img.astype(np.float32)
    img = (img/2047)*255
    img = img.astype(np.uint8)

    img = cv2.resize(img, (640, 480))
    print(img.shape)
    #img_color = np.stack((img, img, img), 2)
    img_color = gray2rgb(img)
    video.write(img_color)

video.release()