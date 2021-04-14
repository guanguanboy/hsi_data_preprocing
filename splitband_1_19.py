import spectral.io.envi as envi
import matplotlib.pyplot as plt
from spectral import *
import numpy as np
import scipy.io
from PIL import Image
import os

dataset_root_path = '../light_1_20/'
img_path_name_list = os.listdir(dataset_root_path)  # 得到path目录下所有图片名称的一个list

pathlistlen = len(img_path_name_list)
print(len(img_path_name_list))

print(type(img_path_name_list))
print(img_path_name_list[0])

img_name_list_hdr = []
for i in range(pathlistlen ):
    img_name_list_hdr.append(dataset_root_path + img_path_name_list[i] + '/capture/' + img_path_name_list[i][0:20] + '.hdr')
    print(img_name_list_hdr[i])


image_count = 0
for i in range(len(img_name_list_hdr)):
    filename_0_1ms = img_name_list_hdr[i]
   
    spectral_img_0_1ms = envi.open(filename_0_1ms)
    
    splited_dataset_path = dataset_root_path + img_path_name_list[i] + '/splitedrgb/'

    spectral_img_0_1ms_band_count = spectral_img_0_1ms.shape[2]

    for i in range(spectral_img_0_1ms_band_count):
        single_band_noise_img = spectral_img_0_1ms.read_band(i)
        im = Image.fromarray(single_band_noise_img)
        image_name = splited_dataset_path + str(image_count) + '.png'
        im.save(image_name)

        #single_band_clean_img = spectral_img_15ms.read_band(i)
        #im_clean = Image.fromarray(single_band_clean_img)
        #image_name_clean = splited_dataset_clean_path + str(image_count) + '.png'
        #im_clean.save(image_name_clean)

        image_count += 1

