function [outputArg1,outputArg2] = data_augment(lowlight, label, savePath)
    global count
    %imresize(A, SCALE) returns an image that is SCALE times the
    %size of A, which is a grayscale, RGB, or binary image.
    %input = imresize(label, 1/upscale_factor, 'bicubic');%����cave���ݼ���label��СΪ64*64*31��upscale_factorֵΪ2
    %����input�Ĵ�СΪ32*32*31����Ϊ��������룬��Ӧlabel�Ĵ�СΪ64*64*31
    
    count = count+1; 
    count_name = num2str(count, '%05d');
    lowlight = permute(lowlight, [3 1 2]); %[3 1 2]��ʾ��ͨ�����ƶ�����һά
    highlight = permute(label, [3 1 2]);
    lowlight = single(lowlight);
    label = single(highlight);
    
    %���߹������ݱ����mat��ʽ��,Save workspace variables to file
    save([savePath,count_name,'.mat'],'lowlight','label'); % save augmented hyperspectral image to "savePath"
end

