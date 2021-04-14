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
print('count of all envi files:',len(img_path_name_list))

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

#assert len(img_name_list_15ms) == len(img_name_list_0_1ms)

output_root_dir = '../mat_captured_1_8/'

#img_path_name_list 中保存着类似2021-01-08_13-18-38_123_orange2_zao_1ms的名称
#去掉2021-01-08_13-18-38_123_orange2_zao_1ms中前32个字符就会得到zao_lms

abc = '2021-01-08_13-18-38_123_orange2_zao_1ms'
print(abc[32:])

mat_file_name = abc[32:] + '.mat'
print(mat_file_name)
suffix_list = [target_substring_1ms, target_substring_15ms, target_substring_9ms]
for i in range(pathlistlen ):
    mat_file_name =  ""
    for suffix in suffix_list:
        if img_path_name_list[i].endswith(suffix):
            path = output_root_dir + suffix
            if not os.path.exists(path):
                os.mkdir(path)
            mat_file_name = output_root_dir + suffix + '/' + img_path_name_list[i][32:] + '.mat'

    if mat_file_name.strip(): #如果字符串不为空
        #读取hdr文件
        cur_path = img_name_list_hdr[i]
        img = envi.open(cur_path)
        array = img.load()
        spectral_int16 = array.astype(np.int16)  # 这里把它转换为np.int16类型是为了让其适应算法的输入
        scipy.io.savemat(mat_file_name, {'img': spectral_int16})