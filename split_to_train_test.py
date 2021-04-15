"""
脚本目标，随机将80%的样本划分为训练集
将剩余20%的样本划分到测试集
"""
import os
import numpy as np
import scipy.io
import shutil
import sys

mat_source_root_dir = '../mat_selected_1_8/'
mat_output_root_dir = '../lowlight_origin_mat/'
img_path_name_list = os.listdir(mat_source_root_dir)
print('source root dir:',img_path_name_list)

img_path_name_list_corret = img_path_name_list[0:4]
print('img_path_name_list_corret:',img_path_name_list_corret)

TRAIN = 'train/'
TEST = 'test/'
data_using_type = [TRAIN, TEST]
total_sample_num = 0

#计算total sample num
total_sample_num = 12

indices = np.arange(total_sample_num)
rng = np.random.RandomState(123)
permuted_indices = rng.permutation(indices)
print(permuted_indices)

train_size= int(0.8*total_sample_num)
test_size = total_sample_num - train_size
print(train_size, test_size)

train_ind = permuted_indices[:train_size]
test_ind = permuted_indices[train_size:]
print(train_ind)
print(test_ind)

for path in img_path_name_list_corret:
    mat_file_sub_list = os.listdir(mat_source_root_dir + path)#某个path下所有的mat文件

    for data_set_type in data_using_type:
        #创建train和test目录
        datasettype_dir = mat_output_root_dir + data_set_type #存储文件的目标目录
        if not os.path.exists(datasettype_dir):
            os.mkdir(datasettype_dir)

        output_dir = datasettype_dir+ path + '/' #文件输出目录
        if not os.path.exists(output_dir):
            os.mkdir(output_dir)

        if data_set_type == TRAIN:
            train_sample_name = np.array(mat_file_sub_list)[train_ind]
            for mat_file_name in train_sample_name:
                mat_file_full_path = mat_source_root_dir + path + '/' + mat_file_name
                try:
                    shutil.copy(mat_file_full_path, output_dir)
                except IOError as e:
                    print("Unable to copy file. %s" % e)
                except:
                    print("Unexpected error:", sys.exc_info())

        if data_set_type == TEST:
            test_sample_name = np.array(mat_file_sub_list)[test_ind]
            for mat_file_name in test_sample_name:
                mat_file_full_path = mat_source_root_dir + path + '/' + mat_file_name
                try:
                    shutil.copy(mat_file_full_path, output_dir)
                except IOError as e:
                    print("Unable to copy file. %s" % e)
                except:
                    print("Unexpected error:", sys.exc_info())

        #以上已经找到了要复制的文件的名称，下面这些文件分别复制到对应的文件夹下即可。

        #先复制train sample

        #再复制test sample

#sub_list_len = len(mat_file_sub_list)
#print('sub_list_len', sub_list_len)
#total_sample_num = sub_list_len





