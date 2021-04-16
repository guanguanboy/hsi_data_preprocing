import spectral.io.envi as envi
import matplotlib.pyplot as plt
from spectral import *
import numpy as np
import scipy.io
from PIL import Image
import os
print(os.getcwd())

file_name =   'D:\DataSets\hyperspectraldatasets\lowlight_hyperspectral_datasets\captured_1_8\\2021-01-08_13-18-38_123_orange2_zao_1ms\capture\\2021-01-08_13-18-38_123_orange2.hdr'

print(file_name)
img = envi.open(file_name)
print(img)

print(img.shape) #(390, 512, 448)
print(type(img)) #<class 'spectral.io.bilfile.BilFile'>

#scipy.io.savemat('lowlight.mat', {'lowlight':array})
#print(img[:,:,])

array = img.load()
print(type(array)) #<class 'spectral.image.ImageArray'>
print('array.shape', array.shape) #array.shape (390, 512, 448)
print(isinstance(array, np.ndarray)) #True,返回True，说明array是numpy.ndarray类型

band_150 = array[:,:,150]
print(band_150.shape)
band_150_squeezed = band_150.squeeze()
print(band_150_squeezed.dtype)
plt.imshow(band_150_squeezed, 'gray')
plt.show()

#spectral_slice = array[(390//2 - 32):(390//2 + 32), (512//2 - 32):(512//2 + 32), 0:30]
spectral_slice = array[100:200, 200:300, 135:165]
print(spectral_slice.shape)
spectral_int16 = spectral_slice.astype(np.int16) #这里把它转换为np.int16类型是为了让其适应算法的输入
scipy.io.savemat('lowlight_1ms.mat', {'img':spectral_slice})


mat_data = scipy.io.loadmat('lowlight_1ms.mat')
print(type(mat_data)) #<class 'dict'>
mat_data_content = mat_data['img']
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
#plt.imshow(color_mat)

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