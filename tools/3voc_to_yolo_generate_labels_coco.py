import xml.etree.ElementTree as ET
import pickle
import os
import random
from os import listdir, getcwd
from os.path import join
 
def convert(size, box):
    # size=(width, height)  b=(xmin, xmax, ymin, ymax)
    # x_center = (xmax+xmin)/2        y_center = (ymax+ymin)/2
    # x = x_center / width            y = y_center / height
    # w = (xmax-xmin) / width         h = (ymax-ymin) / height
    dw = 1. / size[0]
    dh = 1. / size[1]
    x_center = (box[0]+box[1])/2.0 -1
    y_center = (box[2]+box[3])/2.0 -1
    x = x_center *dw
    y = y_center *dh
 
    w = (box[1] - box[0]) *dw
    h = (box[3] - box[2]) *dh
 
    # print(x, y, w, h)
    return (x,y,w,h)
 
def convert_annotation(xml_files_path, save_txt_files_path, classes):  
    xml_files = os.listdir(xml_files_path)
    # print(xml_files)
    for xml_name in xml_files:
        # print(xml_name)
        xml_file = xml_files_path + '/'+xml_name
        out_txt_path = save_txt_files_path+ '/'+ xml_name.split('.')[0] + '.txt'
        out_txt_f = open(out_txt_path, 'w')
        tree=ET.parse(xml_file)
        root = tree.getroot()
        size = root.find('size')
        w = int(size.find('width').text)
        h = int(size.find('height').text)
 
        for obj in root.iter('object'):
            difficult = obj.find('difficult').text
            cls = obj.find('name').text
            if cls not in classes or int(difficult) == 1:
                continue
            cls_id = classes.index(cls)
            xmlbox = obj.find('bndbox')
            b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
            # b=(xmin, xmax, ymin, ymax)
            # print(w, h, b)
            bb = convert((w,h), b)
            out_txt_f.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')
    print('XML -> txt has done!')
 
def split_train_val(abswd):
    labelwd = abswd
    basic_path = abswd
    xmlfilepath = basic_path+ '/'+'labels'
    imgpath = basic_path+ '/'+ 'images'
    txtsavepath = basic_path+ '/'+'ImageSets'+ '/'+'Main'
    total_xml_total = os.listdir(imgpath)
    total_xml = []
    for xml_name in total_xml_total:
        if os.path.splitext(xml_name)[-1] == ".jpg":
            total_xml.append(xml_name)

    num = len(total_xml)
    list_index = range(num)
    list_index = list(list_index)
    random.shuffle(list_index)
    list_index = list(list_index)
    if not os.path.exists(labelwd + '/labels'):
        os.mkdir(labelwd + '/labels')
    # if not os.path.exists(labelwd + '/train.txt'):
    #     os.mkdir(labelwd + '/train.txt')
    # if not os.path.exists(labelwd + '/val.txt'):
    #     os.mkdir(labelwd + '/val.txt')
    # file_trainval = open(labelwd + '/trainval.txt', 'w+')
    # #file_test = open(labelwd + '/test.txt', 'w+')
    # file_train = open(labelwd + '/train.txt', 'w+')
    # file_val = open(labelwd + '/val.txt', 'w+')
    # ismun =num * 0.05
    # for i in list_index:
    #     name = labelwd + '/images/' + total_xml[i][:] + '\n'
    #     file_trainval.write(name)
    #     if i < ismun:
    #         file_val.write(name)
    #     else:
    #         file_train.write(name)

    # file_trainval.close()
    # file_train.close()
    # file_val.close()
    # # file_test.close()
    print('split data -> train & val has done')


if __name__ == "__main__":
    # 把forklift_pallet的voc的xml标签文件转化为yolo的txt标签文件,并且划分数据集
    '''使用此函数前需要修改下面的四个参数'''
    abswd = '/home/mengxianchi/train_img/AK_CLW/data/files'
    # 1、voc格式的xml标签文件路径
    xml_files1 = abswd + '/xml'
    # 2、转化为yolo格式的txt标签文件存储路径
    save_txt_files1 = abswd + '/labels'
    if not os.path.exists(save_txt_files1):
        os.mkdir(save_txt_files1)
    # 3、需要转化的类别
    classes = ['AK','CLW']#注意：这里根据自己的类别名称及种类自行更改
 
    convert_annotation(xml_files1, save_txt_files1, classes)

    # 4、划分数据集:数据集的绝对路径

    split_train_val(abswd)

