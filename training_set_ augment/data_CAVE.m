clc
clear 
close all
 
%% define hyperparameters 
Band = 31;  
patchSize = 32;
randomNumber = 24;
upscale_factor = 2;
data_type = 'CAVE';
global count
count = 0;
imagePatch = patchSize*upscale_factor; %imagePatch值为64
scales = [1.0, 0.75, 0.5];
%% bulid upscale folder
savePath=['D:/DataSets/hyperspectraldatasets/',data_type,'/train_processed/',num2str(upscale_factor),'/']; %upscale_factor值为2
if ~exist(savePath, 'dir')
    mkdir(savePath)
end

%% 
%srPath = 'E:/datas/HyperSR/CAVE/train/';  %source data downlaoded from website 
srPath = 'D:/DataSets/hyperspectraldatasets/CAVE/train/'
srFile=fullfile(srPath);                                                                                                                                                                                                                                                              
srdirOutput=dir(fullfile(srFile));
srfileNames={srdirOutput.name}';
number = length(srfileNames)-2


for index = 1:length(srfileNames)
    width = 0;
    height = 0;
    name = char(srfileNames(index));
    if(isequal(name,'.')||... % remove the two hidden folders that come with the system
           isequal(name,'..'))
               continue;
    end
    disp(['----:',data_type,'----upscale_factor:',num2str(upscale_factor),'----deal with:',num2str(index-2),'----name:',name]);

    singlePath= [srPath, name, '/', name]; %png格式的波段数据所在的位置
    singleFile=fullfile(singlePath);
    srdirOutput=dir(fullfile(singleFile,'/*.png'));
    singlefileNames={srdirOutput.name}'; %取出了31个波段png格式的文件名
    Band = length(singlefileNames);
    source = zeros(512*512, Band); %是一个高光谱数据，将各个band的数据组合到了一起。
    for i = 1:Band %遍历所有波段的信息
        srName = char(singlefileNames(i));
        srImage = imread([singlePath,'/',srName]);
        if i == 1
            width = size(srImage,1);
            height = size(srImage,2);
        end
        source(:,i) = srImage(:);   %srImage(:)的功能是将srImage展开成了一维列向量
    end

    %% normalization
    imgz=double(source(:));
    img=imgz./65535;%这里除以了16位int做的归一化
    t = reshape(img, width, height, Band);

    %%
    for sc = 1:length(scales) %遍历scales
        newt = imresize(t, scales(sc));%先把Image整体缩放，1：大小不变，0.75：长宽都变为原来的0.75倍；0.5：长宽都变为256    
        %imresize(A, SCALE) returns an image that is SCALE times the
        %size of A, which is a grayscale, RGB, or binary image.
        
        %size(newt,1)为取出newt中第一维的大小，size(newt,2)为newt中第二维的大小
        %imagePatch = patchSize*upscale_factor;
        %patchSize = 32;
        x_random = randperm(size(newt,1) - imagePatch, randomNumber); %imagePatch值为64，randomNumber值为24
        y_random = randperm(size(newt,2) - imagePatch, randomNumber);
        %P = randperm(N,K) returns a row vector containing K unique integers
        %selected randomly from 1:N.  For example, randperm(6,3) might be [4 2 5].
        for j = 1:randomNumber %randomNumber值为24
            %切分出一个小patch hrImage，hrImage的大小为64*64*31
            hrImage = newt(x_random(j):x_random(j)+imagePatch-1, y_random(j):y_random(j)+imagePatch-1, :);

            %对小patch进行5种形式的增强
            label = hrImage;   
            data_augment(label, upscale_factor, savePath);

            label = imrotate(hrImage,180);%旋转180度  
            data_augment(label, upscale_factor, savePath);

            label = imrotate(hrImage,90);%旋转90度
            data_augment(label, upscale_factor, savePath);

            label = imrotate(hrImage,270);%旋转270度
            data_augment(label, upscale_factor, savePath);

            label = flipdim(hrImage,1); %水平翻转
            data_augment(label, upscale_factor, savePath);

        end
        clear x_random;
        clear y_random;
        clear newt;

    end
    clear t;
end