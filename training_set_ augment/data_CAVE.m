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
imagePatch = patchSize*upscale_factor; %imagePatchֵΪ64
scales = [1.0, 0.75, 0.5];
%% bulid upscale folder
savePath=['D:/DataSets/hyperspectraldatasets/',data_type,'/train_processed/',num2str(upscale_factor),'/']; %upscale_factorֵΪ2
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

    singlePath= [srPath, name, '/', name]; %png��ʽ�Ĳ����������ڵ�λ��
    singleFile=fullfile(singlePath);
    srdirOutput=dir(fullfile(singleFile,'/*.png'));
    singlefileNames={srdirOutput.name}'; %ȡ����31������png��ʽ���ļ���
    Band = length(singlefileNames);
    source = zeros(512*512, Band); %��һ���߹������ݣ�������band��������ϵ���һ��
    for i = 1:Band %�������в��ε���Ϣ
        srName = char(singlefileNames(i));
        srImage = imread([singlePath,'/',srName]);
        if i == 1
            width = size(srImage,1);
            height = size(srImage,2);
        end
        source(:,i) = srImage(:);   %srImage(:)�Ĺ����ǽ�srImageչ������һά������
    end

    %% normalization
    imgz=double(source(:));
    img=imgz./65535;%���������16λint���Ĺ�һ��
    t = reshape(img, width, height, Band);

    %%
    for sc = 1:length(scales) %����scales
        newt = imresize(t, scales(sc));%�Ȱ�Image�������ţ�1����С���䣬0.75��������Ϊԭ����0.75����0.5��������Ϊ256    
        %imresize(A, SCALE) returns an image that is SCALE times the
        %size of A, which is a grayscale, RGB, or binary image.
        
        %size(newt,1)Ϊȡ��newt�е�һά�Ĵ�С��size(newt,2)Ϊnewt�еڶ�ά�Ĵ�С
        %imagePatch = patchSize*upscale_factor;
        %patchSize = 32;
        x_random = randperm(size(newt,1) - imagePatch, randomNumber); %imagePatchֵΪ64��randomNumberֵΪ24
        y_random = randperm(size(newt,2) - imagePatch, randomNumber);
        %P = randperm(N,K) returns a row vector containing K unique integers
        %selected randomly from 1:N.  For example, randperm(6,3) might be [4 2 5].
        for j = 1:randomNumber %randomNumberֵΪ24
            %�зֳ�һ��Сpatch hrImage��hrImage�Ĵ�СΪ64*64*31
            hrImage = newt(x_random(j):x_random(j)+imagePatch-1, y_random(j):y_random(j)+imagePatch-1, :);

            %��Сpatch����5����ʽ����ǿ
            label = hrImage;   
            data_augment(label, upscale_factor, savePath);

            label = imrotate(hrImage,180);%��ת180��  
            data_augment(label, upscale_factor, savePath);

            label = imrotate(hrImage,90);%��ת90��
            data_augment(label, upscale_factor, savePath);

            label = imrotate(hrImage,270);%��ת270��
            data_augment(label, upscale_factor, savePath);

            label = flipdim(hrImage,1); %ˮƽ��ת
            data_augment(label, upscale_factor, savePath);

        end
        clear x_random;
        clear y_random;
        clear newt;

    end
    clear t;
end