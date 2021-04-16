import matplotlib.pyplot as plt
from spectral import *
import numpy as np
import scipy.io
from PIL import Image
import os

filename_orgin = '../lowlight_origin_mat/train/15ms/twoorage_15ms.mat'
filename = '../lowlight/train/03009.mat'

#mat_data = scipy.io.loadmat('lowlight_1ms.mat')
mat_data = scipy.io.loadmat(filename)
print(type(mat_data)) #<class 'dict'>
mat_data_content = mat_data['label']
mat_data_content = np.moveaxis(mat_data_content, 0, -1) #在保存03009.mat文件的时候，将通道置换到了最前面，这里将通道置换回来
print(type(mat_data_content)) #<class 'numpy.ndarray'>
print(mat_data_content.shape)

"""
以伪彩色的方式显示高光谱图像¶
选择9，19，29三个通道作为形成伪彩色
因为原始的高光谱是12bit的数据，所以如果直接显示的话，会出现错误，显示不出来。
log提示如下：Clipping input data to the valid range for imshow with RGB data ([0..1] for floats or [0..255] for integers).
"""
color_mat = mat_data_content[:,:,(9, 19, 29)]
print(color_mat.shape)
print(color_mat.dtype)
plt.imshow(color_mat)
plt.show()
"""
所以需要将数据归一化到[0..1] for floats or [0..255] for integers之间
这里先看归一化到[0..1]之间
"""
print("gt max = ", color_mat.max())
print('gt min =', color_mat.min())
color_min = color_mat.min()
color_max = color_mat.max()
print(color_mat.dtype)

gt8bit = ( (color_mat - color_min)/ (color_max - color_min))
print(gt8bit.dtype)
print("gt max = ", gt8bit.max())
print('gt min =', gt8bit.min())
#print(gt8bit[:,:,0])
plt.imshow(gt8bit)
plt.show()

#归一化到[0..255]之间
gt8bit_float = ((color_mat - color_min)/ (color_max - color_min))*255
gt8bit_int = gt8bit_float.astype(np.int8)
print(gt8bit_int.max())
print(gt8bit_int[:,:,1])
#plt.imshow(gt8bit_int)

gt16bit_int = gt8bit_float.astype(np.int16)
print(gt16bit_int.max())
plt.imshow(gt16bit_int)
plt.show()