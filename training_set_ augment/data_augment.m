function [outputArg1,outputArg2] = data_augment(lowlight, label, savePath)
    global count
    %imresize(A, SCALE) returns an image that is SCALE times the
    %size of A, which is a grayscale, RGB, or binary image.
    %input = imresize(label, 1/upscale_factor, 'bicubic');%对于cave数据集，label大小为64*64*31，upscale_factor值为2
    %所以input的大小为32*32*31，作为网络的输入，对应label的大小为64*64*31
    
    count = count+1; 
    count_name = num2str(count, '%05d');
    lowlight = permute(lowlight, [3 1 2]); %[3 1 2]表示把通道数移动到第一维
    highlight = permute(label, [3 1 2]);
    lowlight = single(lowlight);
    label = single(highlight);
    
    %将高光谱数据保存成mat格式的,Save workspace variables to file
    save([savePath,count_name,'.mat'],'lowlight','label'); % save augmented hyperspectral image to "savePath"
end

