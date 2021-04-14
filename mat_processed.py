"""
方案：去掉前24个波段，去掉后24个波段。
剩余400个波段

每8个波段中选择一个波段，最后形成一个50个band的高光谱数据。

使用1ms的数据作为lowlight数据，使用15ms数据作为label数据。
"""
import os
import numpy as np
import scipy.io

mat_source_root_dir = '../mat_captured_1_8/'
mat_output_root_dir = '../mat_selected_1_8/'

img_path_name_list = os.listdir(mat_source_root_dir)
print(img_path_name_list)

mat_file_list = []
NORMLIZED_WIDTH = 390
NORMLIZED_HEIGHT = 512
NORMLIZED_BAND_NUM = 50

for path in img_path_name_list:
    mat_file_sub_list = os.listdir(mat_source_root_dir + path)
    output_dir = mat_output_root_dir + path + '/'
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    for mat_file in mat_file_sub_list:
        #print(mat_file)
        mat_file_complete_path = mat_source_root_dir + path + '/' + mat_file
        mat_data = scipy.io.loadmat(mat_file_complete_path)
        mat_data_content = mat_data['img']
        mat_data_band_deleted = mat_data_content[:,:,24:448-24] #去掉前后各24个band
        width = mat_data_band_deleted.shape[0]
        height = mat_data_band_deleted.shape[1]
        band_num = mat_data_band_deleted.shape[2]
        band_selected = np.zeros((width,height,band_num//8), dtype=np.int16) #用来保存选择到的50个band
        count = 0
        for i in range(band_num):
            if i % 8 == 0:
                band_selected[:,:,count] = mat_data_band_deleted[:,:,i]
                count = count + 1
        band_selected_resized = band_selected[0:NORMLIZED_WIDTH,0:NORMLIZED_HEIGHT,:] #取左上角的390*512*50的内容，使得所有mat文件大小一致
        output_file_name = output_dir + mat_file
        scipy.io.savemat(output_file_name, {'img': band_selected_resized})


