# conding:utf-8
import os
import time
from multiprocessing import Process
# train_dir = input("请输入要整理的文件夹：")
train_dir = '/home/mengxianchi/train_img/AK_CLW/data/files'
file_types = []
file_list = []

# 遍历文件夹，排除文件夹，建立为文件
for i in os.listdir(train_dir):  # 遍历整个文件夹
    path = os.path.join(train_dir, i)
    if os.path.isfile(path):  # 判断是否为一个文件，排除文件夹
        file_list.append(i)
#print(file_list)

# 全部后缀整理为file_types
for data_name in file_list:
    file_types.append(os.path.splitext(data_name)[1][1:])  # 目录下所有文件的后缀
# 使用集合来去重
file_types = list(set(file_types))
# 列表生成式
file_types = ["其他文件" if x == "" else x for x in file_types]
try:
    file_list.remove("ini")
except ValueError as e:
    print("本文件夹不存在超链接，无需删除")

print(file_types)

# 在原定的目录下，创建同名文件夹
new_dir = train_dir 
if os.path.exists(new_dir) == 0:
    os.mkdir(new_dir)
for file_type in file_types:
    # 以文件类型创建同名的文件夹
    if os.path.exists(new_dir + "/" + file_type):
        print(file_type + "文件夹已存在")
    else:
        os.mkdir(new_dir + "/" + file_type)
def zheng_li(start,end):
    tic = time.time()
    file_list1=file_list[start:end]
    for file_type in file_types:
        for file_name in file_list1:
            # 判断当前文件是不是该文件类型
            if file_name.endswith("." + file_type):
                try:
                    os.rename(train_dir + "/" + file_name, new_dir + "/" + file_type + "/" + file_name)
                except PermissionError as e:
                    print(train_dir + "/" + file_name + "正在使用")

    for data_name in file_list1:
        if os.path.splitext(data_name)[1][1:] == "":
            try:
                os.rename(train_dir + "/" + data_name, new_dir + "/" + "其他文件" + "/" + data_name)
            except PermissionError as e:
                print(train_dir + "/" + data_name + "正在使用")
    toc = time.time()
    shijian = toc-tic
    print('子进程',shijian)
thread_num= 20
thread_list = [[int(i*(len(file_list)-1)/thread_num),
int(min(len(file_list)-1,(i+1)*(len(file_list)-1)/thread_num))]
for i in range(thread_num)]
thread_list[-1][1] = thread_list[-1][1] +1
print(thread_list)
if __name__ == '__main__':


    tic = time.time()
    process_list = []    # 存放开启的进程
    for i in range(thread_num):
        # 进程中的参数args表示调用对象的位置参数元组.注意：元组中只有一个元素时结尾要加","逗号
        p = Process(target=zheng_li, args=(thread_list[i][0],thread_list[i][1]))
        p.start()
        process_list.append(p)
    for i in process_list:
        i.join()    # 阻塞每个子进程，主进程会等待所有子进程结束再结束主进程
    print("主进程结束！")
    toc = time.time()
    shijian = toc-tic
    print('主进程',shijian)

    if os.path.exists(train_dir+'/jpg'):
        os.renames(train_dir+'/jpg',train_dir+'/images')
    if os.path.exists(train_dir+'/txt'):
        os.renames(train_dir+'/txt',train_dir+'/labels')
    print(train_dir + "文件夹文件归档完毕")