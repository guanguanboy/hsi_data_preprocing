import spectral.io.envi as envi
import matplotlib.pyplot as plt
from spectral import *
import numpy as np
import scipy.io
from PIL import Image
import os

dataset_root_path = '../captured_1_8/'
img_path_name_list = os.listdir(dataset_root_path)  # 得到path目录下所有图片名称的一个list

pathlistlen = len(img_path_name_list)
print(len(img_path_name_list))

print(type(img_path_name_list))
print(img_path_name_list[0])

img_name_list_hdr = []
for i in range(pathlistlen ):
    img_name_list_hdr.append(dataset_root_path + img_path_name_list[i] + '/capture/' + img_path_name_list[i][0:31] + '.hdr')
    print(img_name_list_hdr[i])

img_name_list_0_1ms = []
img_name_list_15ms = []
img_name_list_9ms = []
img_name_list_1ms = []

target_substring = '0.1ms'
target_substring_1ms = '1ms'

target_substring_15ms = '15ms'
target_substring_9ms = '9ms'

for i in range(len(img_name_list_hdr) ):
    if target_substring in img_name_list_hdr[i]:
        img_name_list_0_1ms.append(img_name_list_hdr[i])
    if target_substring_15ms in img_name_list_hdr[i]:
        img_name_list_15ms.append(img_name_list_hdr[i])
    if target_substring_9ms in img_name_list_hdr[i]:
        img_name_list_9ms.append(img_name_list_hdr[i])
    if target_substring_1ms in img_name_list_hdr[i] and target_substring not in img_name_list_hdr[i]:
        img_name_list_1ms.append(img_name_list_hdr[i])

print('len of 0.1ms list',len(img_name_list_0_1ms))
for i in range(len(img_name_list_0_1ms)):
    print(img_name_list_0_1ms[i])

print('len of 1ms list',len(img_name_list_1ms))
for i in range(len(img_name_list_1ms)):
    print(img_name_list_1ms[i])

assert len(img_name_list_15ms) == len(img_name_list_0_1ms)

splited_dataset_root_path = './band_splited_dataset'
splited_dataset_noise_path = splited_dataset_root_path + '/noise/'
splited_dataset_clean_path = splited_dataset_root_path + '/clean/'
image_count = 0
for i in range(len(img_name_list_15ms)):
    filename_0_1ms = img_name_list_0_1ms[i]
    filename_15ms = img_name_list_15ms[i]
    filename_9ms = img_name_list_9ms[i]
    filename_1ms = img_name_list_1ms[i]

    spectral_img_0_1ms = envi.open(filename_0_1ms)
    spectral_img_15ms = envi.open(filename_15ms)
    spectral_img_9ms = envi.open(filename_9ms)
    spectral_img_1ms = envi.open(filename_1ms)


    spectral_img_0_1ms_band_count = spectral_img_0_1ms.shape[2]
    spectral_img_15ms_band_count = spectral_img_15ms.shape[2]

    if spectral_img_0_1ms_band_count != spectral_img_15ms_band_count:
        continue

    for i in range(spectral_img_0_1ms_band_count):
        single_band_noise_img = spectral_img_1ms.read_band(i)
        im = Image.fromarray(single_band_noise_img)
        image_name = splited_dataset_noise_path + str(image_count) + '.png'
        im.save(image_name)

        #single_band_clean_img = spectral_img_15ms.read_band(i)
        #im_clean = Image.fromarray(single_band_clean_img)
        #image_name_clean = splited_dataset_clean_path + str(image_count) + '.png'
        #im_clean.save(image_name_clean)

        image_count += 1

img = envi.open('./captured_1_8/2021-01-08_13-17-07_123_orange2_zao_15ms/capture/2021-01-08_13-17-07_123_orange2.hdr')
print(img)

print(img.shape)
print(type(img))
array = img.load()
print(type(array))
print('array.shape', array.shape)

gt = img.read_band(150)
print('gt type:', type(gt))
print(gt.shape)

im = Image.fromarray(gt)
im.save('band150.png')
"""
scipy.io.savemat('lowlight.mat', {'lowlight':array})
#print(img[:,:,])
bands = [i for i in range(img.shape[2])]
print(len(bands))
gt0 = img.read_band(bands)
print('gt0 type:', type(gt0))
print('gt0.shape',gt0.shape)
gt = img.read_band(150)
print('gt type:', type(gt))
print(gt.shape)
plt.imshow(gt)
plt.show()
save_rgb('rgb.jpg', img, [29, 19, 9])
view = imshow(img, [29, 19, 9])
print(view)
"""
