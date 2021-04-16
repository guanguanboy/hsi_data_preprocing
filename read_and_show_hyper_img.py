import spectral.io.envi as envi
import matplotlib.pyplot as plt
from spectral import *
import numpy as np
import scipy.io
from PIL import Image
from skimage import io

file_name = '../captured_1_8/2021-01-08_13-36-30_123_orange2_twoorage_15ms/capture/2021-01-08_13-36-30_123_orange2.hdr'
img = envi.open(file_name)
print(img)

print(img.shape)
print(type(img))
array = img.load()
print(type(array))
print('array.shape', array.shape)

#scipy.io.savemat('lowlight.mat', {'lowlight':array})
#print(img[:,:,])
bands = [i for i in range(img.shape[2])]
print('band num=',len(bands))
gt0 = img.read_band(bands)


print('gt0 type:', type(gt0))
print('gt0.shape',gt0.shape)
gt = img.read_band(29)
print('gt type:', type(gt))
print(gt.shape)
print(gt.dtype)
plt.imshow(gt,cmap='gray')
plt.show()
print("gt max = ", gt.max())
print('gt min =', gt.min())
gt8bit = gt.astype(np.float)
print('gt8bit origin type=', gt8bit.dtype)
gt8bit = (gt8bit / 2047)*255 #归一化，因为相机内部是12bit的，所以可是使用除以2047来归一化数据

gt8bit = gt8bit.astype(np.uint8)

print(gt8bit.max(), gt8bit.min())
print('gt8bit nomoralized type=', gt8bit.dtype)
plt.imshow(gt8bit,cmap='gray')
plt.show()

save_rgb('rgb.jpg', img, [29, 19, 9])
save_rgb('rgb_192.jpg', img, [192, 117, 42]) #default bands = {192, 117, 42}, rgb 通道所在的band


#从磁盘读取rgb.jpg
rgb_img = io.imread('rgb.jpg')
plt.imshow(rgb_img)
plt.show()

rgb_img_192 = io.imread('rgb_192.jpg')
plt.imshow(rgb_img_192)
plt.show()

"""

plt.imshow(gt)
plt.show()
save_rgb('rgb.jpg', img, [29, 19, 9])
view = imshow(img, [29, 19, 9])
print(view)
"""