import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
from skimage.color import  gray2rgb
file_dir='D:/DataSets/hyperspectraldatasets/424capture/lowlight_Apple_2021-04-24_08-42-16/splitedrgb/'
img_path_name_list = os.listdir(file_dir) #Return a list containing the names of the files in the directory.

#img = cv2.imread(file_dir + img_path_name_list[100],cv2.IMREAD_GRAYSCALE)
#plt.imshow(img)
#plt.show()

#print(img_path_name_list[201])
#img_bgr = cv2.imread(file_dir + img_path_name_list[201])
#print(img_bgr)
#print(img_bgr.shape)
#img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
#plt.imshow(img_bgr)
#plt.show()

#cv2.imshow('bgr', img_bgr)
#cv2.waitKey(0)


from skimage import io
img = io.imread(file_dir + img_path_name_list[201])
#img_color = np.stack((img,img,img), 2)
img_color = gray2rgb(img)
print(img_color.shape)
print(img.shape)
plt.imshow(img_color)
plt.show()