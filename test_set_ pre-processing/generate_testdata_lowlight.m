clear 
clc
close all

data_type = 'lowlight';
test_hsi_width = 384;
test_hsi_height = 384;
%% bulid hsi save folder
savePath=['../../',data_type,'/test/'];
if ~exist(savePath, 'dir')
    mkdir(savePath)
end

%% obtian all the original hyperspectral image
lowlight_srPath =  '../../lowlight_origin_mat/test/1ms';
fileFolder=fullfile(lowlight_srPath);
dirOutput=dir(fullfile(fileFolder,'*.mat'));
fileNames={dirOutput.name}';
lowlight_num = length(fileNames);

label_srPath =  '../../lowlight_origin_mat/test/15ms';%��Ŀ¼�µ�name��'../mat_selected_1_8/1ms'��һ�µ�
label_fileFolder=fullfile(label_srPath);
label_dirOutput=dir(fullfile(label_fileFolder,'*.mat'));
label_fileNames={label_dirOutput.name}';
label_num = length(label_fileNames);

assert(lowlight_num == label_num)

for index = 1 : lowlight_num
    name = char(fileNames(index));
    %if(isequal(name,'.')||... % remove the two hidden folders that come with the system
    %       isequal(name,'..'))
    %           continue;
    %end
    disp(['-----deal with:',num2str(index),'----name:',name]); 

    lowlight_data_path = [lowlight_srPath, '/', name];
    load(lowlight_data_path) %loadִ��֮��img��������ᱻ������
    
    %% normalization
    img_double = double(img);
    lowlight_normalized_hsi = img_double ./ 2047;%max(max(max(ref)))��Ϊ���ҳ�ref�е����ֵ��Ȼ������������ֵ����һ��
    clear img;%%����imgΪmat�����ݵ�keyֵ

    %%����label����
    label_name = char(label_fileNames(index));
    disp(['-----deal with label:',num2str(index),'----name:',label_name]); 
    label_data_path = [label_srPath, '/', label_name];%label��name��lowlight��name��һ���ġ�
    load(label_data_path)
    label_double = double(img);
    label_normalized_hsi = label_double ./ 2047;%max(max(max(ref)))��Ϊ���ҳ�ref�е����ֵ��Ȼ������������ֵ����һ��
    clear img;%%����imgΪmat�����ݵ�keyֵ
    
    %% obtian lowlight and label hyperspectral image
    [lowlight_height, lowlight_width, ll_band_num] = size(lowlight_normalized_hsi);
    [label_height, label_width, label_band_num] = size(label_normalized_hsi);
    %height, width, band_num = size(lowlight_normalized_hsi);
    %test_hsi_width
    height_offset = (lowlight_height - test_hsi_height)/2;
    width_offset = (lowlight_width - test_hsi_width)/2;
    lowlight = lowlight_normalized_hsi(height_offset:height_offset+test_hsi_height-1, width_offset:width_offset+test_hsi_width-1,:);
    
    height_offset = (label_height - test_hsi_height)/2;
    width_offset = (label_width - test_hsi_width)/2;
    label = label_normalized_hsi(height_offset:height_offset+test_hsi_height-1, width_offset:width_offset+test_hsi_width-1,:);


    save([savePath,'/',name], 'lowlight', 'label')

    clear lowlight_croped
    clear label_croped

end
