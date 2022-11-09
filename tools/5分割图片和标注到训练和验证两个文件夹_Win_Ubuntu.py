import os
import random
import time
from multiprocessing import Process
#scp -P 1234 dataset.zip mengxianchi@198.168.1.10:/home/mengxianchi/train_img/concat/dataset2
dir = '/home/mengxianchi/train_img/AK_CLW/data/files'
if not os.path.exists(dir+'/dataset'):
    os.mkdir(dir+'/dataset')
    os.mkdir(dir+'/dataset/train')
    os.mkdir(dir+'/dataset/train/images')
    os.mkdir(dir+'/dataset/train/labels')
    os.mkdir(dir+'/dataset/val')
    os.mkdir(dir+'/dataset/val/images')
    os.mkdir(dir+'/dataset/val/labels')
images_dir = dir + '/images'
labels_dir = dir + '/labels'
trainfiles = os.listdir(images_dir)
num_train = len(trainfiles)
print( "num_train: " + str(num_train) )
index_list = list(range(num_train))
#print(index_list)


# 最好放在训练通用文件夹下
train_image_Dir = dir + '/dataset/train/images'
valid_image_Dir = dir + '/dataset/val/images'
train_label_Dir = dir + '/dataset/train/labels'
valid_label_Dir = dir + '/dataset/val/labels'
def fen_ge(start,end):
    num = 0
    tic = time.time()
    index_list1 = index_list[start:end]
    random.shuffle(index_list1)
    for i in index_list1:
        fileName = images_dir+'/'+trainfiles[i]
        labelName = labels_dir+'/'+trainfiles[i][:-3]+'txt'
        train_images = train_image_Dir+'/'+trainfiles[i]
        train_labels = train_label_Dir+'/'+trainfiles[i][:-3]+'txt'
        val_images = valid_image_Dir+'/'+trainfiles[i]
        val_labels = valid_label_Dir+'/'+trainfiles[i][:-3]+'txt'
        try:        
            if num < (end-start)*0.9:
                os.renames(fileName, train_images)
                os.renames(labelName,train_labels)
            else:
                os.renames(fileName, val_images)
                os.renames(labelName, val_labels)
        except ValueError as e:
            print("没找到")
        num += 1
        print(num)	
    toc = time.time()
    shijian = toc-tic
    print('子进程',shijian)
thread_num= 30
thread_list = [[int(i*(len(index_list)-1)/thread_num),
int(min(len(index_list)-1,(i+1)*(len(index_list)-1)/thread_num))] 
for i in range(thread_num)]
thread_list[-1][1] = thread_list[-1][1] +1
print(thread_list)


if __name__ == '__main__':
    tic = time.time()
    process_list = []    # 存放开启的进程
    for i in range(thread_num):
        # 进程中的参数args表示调用对象的位置参数元组.注意：元组中只有一个元素时结尾要加","逗号
        p = Process(target=fen_ge, args=(thread_list[i][0],thread_list[i][1]))
        p.start()
        process_list.append(p)
    for i in process_list:
        i.join()    # 阻塞每个子进程，主进程会等待所有子进程结束再结束主进程
    print("主进程结束！")
    toc = time.time()
    shijian = toc-tic
    print('主进程',shijian)




print("操作已完成")