clc
clear 
close all
 
%% define hyperparameters 
patchSize = 64;
randomNumber = 32;
data_type = 'lowlight';
P = 0.5;
global count
count = 0;
imagePatch = patchSize;
scales = [1.0, 0.75, 0.5];

%% bulid hsi save folder
savePath=['../../',data_type,'/train/'];
if ~exist(savePath, 'dir')
    mkdir(savePath)
end

%% 找到训练集文件夹下所有mat文件
lowlight_srPath =  '../../lowlight_origin_mat/train/1ms';
fileFolder=fullfile(lowlight_srPath);
dirOutput=dir(fullfile(fileFolder,'*.mat'));
fileNames={dirOutput.name}';
length(fileNames)

label_srPath =  '../../lowlight_origin_mat/train/15ms';%该目录下的name与'../mat_selected_1_8/1ms'是一致的
label_fileFolder=fullfile(label_srPath);
label_dirOutput=dir(fullfile(label_fileFolder,'*.mat'));
label_fileNames={label_dirOutput.name}';
length(label_fileNames)

for i = 1:length(fileNames) %最外层循环，遍历每一个mat文件
    name = char(fileNames(i));
    disp(['----:',data_type,'----deal with:',num2str(i),'----name:',name]);
    
    %%加载lowlight数据
    lowlight_data_path = [lowlight_srPath, '/', name];
    load(lowlight_data_path) %load执行之后，img这个变量会被创建。
    
    %% normalization
    img_double = double(img);
    lowlight_normalized_hsi = img_double ./ 2047;%max(max(max(ref)))是为了找出ref中的最大值，然后整体除以最大值做归一化
    clear img;%%其中img为mat中数据的key值
 
    %%加载label数据
    label_name = char(label_fileNames(i));
    label_data_path = [label_srPath, '/', label_name];%label的name与lowlight的name是一样的。
    load(label_data_path)
    label_double = double(img);
    label_normalized_hsi = label_double ./ 2047;%max(max(max(ref)))是为了找出ref中的最大值，然后整体除以最大值做归一化
    clear img;%%其中img为mat中数据的key值

    for j = 1:randomNumber %内层循环，遍历每一个path
        for sc = 1:length(scales)
            scaled_lowlight_hsi = imresize(lowlight_normalized_hsi, scales(sc));
            scaled_label_hsi = imresize(label_normalized_hsi, scales(sc));

            x_random = randperm(size(scaled_lowlight_hsi,1) - imagePatch, randomNumber);
            y_random = randperm(size(scaled_lowlight_hsi,2) - imagePatch, randomNumber);
            lowlight_patch_Image = scaled_lowlight_hsi(x_random(j):x_random(j)+imagePatch-1, y_random(j):y_random(j)+imagePatch-1, :);
            label_patch_Image = scaled_label_hsi(x_random(j):x_random(j)+imagePatch-1, y_random(j):y_random(j)+imagePatch-1, :);

            data_augment(lowlight_patch_Image, label_patch_Image, savePath);
            if (rand(1)> P)
                lowlight = imrotate(lowlight_patch_Image,180);
                label = imrotate(label_patch_Image,180);
                data_augment(lowlight, label, savePath);
            end
            if (rand(1)> P)
                lowlight = imrotate(lowlight_patch_Image,90);
                label = imrotate(label_patch_Image,90);  
                data_augment(lowlight, label, savePath);
            end
             if (rand(1)> P)
                lowlight = imrotate(lowlight_patch_Image,270);
                label = imrotate(label_patch_Image,270);  
                data_augment(lowlight, label, savePath);
             end
            if (rand(1)> P)
                lowlight = flipdim(lowlight_patch_Image,1); 
                label = flipdim(label_patch_Image,1);                  
                data_augment(lowlight, label, savePath);
            end
            if (rand(1)> P)
                lowlight = flipdim(lowlight_patch_Image,2);
                label = flipdim(label_patch_Image,2);
                data_augment(lowlight, label, savePath);
            end  

            clear x_random;
            clear y_random;
            clear scaled_lowlight_hsi;
        end%最内层循环，遍历每一个scales，缩放因子
    end
    clear normalized_hsi;
end