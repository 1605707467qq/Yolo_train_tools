import cv2 as cv
import os
import random,time
from multiprocessing import Process     # 多进程的类
dir = 'D:/wanglei/write/write/dataset/concat/files'
img_path=dir+"./images"
label_path=dir+"./labels"
save_path=dir+"./save"
if not os.path.isdir(save_path):
    os.makedirs(save_path)
img_list=os.listdir(img_path)
label_list=os.listdir(label_path)
'''
1. 20进程6名字长度，时间：1.5h+
'''
# 进程区间的个数
thread_num= 30

thread_list = [[int(i*(len(img_list)-1)/thread_num),
int(min(len(img_list)-1,(i+1)*(len(img_list)-1)/thread_num))]
for i in range(thread_num)]
thread_list[-1][1] = thread_list[-1][1] +1
print(thread_list)
class box_info:
    def __init__(self,labels,imgshape):
        if isinstance(labels,list):
            self.box_class=int(labels[0]);
            self.box=self.get_box(labels,imgshape)
        elif isinstance(labels,int):
            self.box_class = labels
            self.box = imgshape
    def getinfo(self,labels,imgshape):
        self.box_class = int(labels[0])
        self.box = self.get_box(labels, imgshape)
    def get_box(self,labels,imgshape):
        x1 = (float(labels[1]) - float(labels[3]) / 2.) * imgshape[1]
        y1 = (float(labels[2]) - float(labels[4]) / 2.) * imgshape[0]
        x2 = (float(labels[1]) + float(labels[3]) / 2.) * imgshape[1]
        y2 = (float(labels[2]) + float(labels[4]) / 2.) * imgshape[0]
        return [int(x1),int(y1),int(x2),int(y2)]
# A是图像的box，B是label的box
def in_or_out(A, B, box_size):
    # if A[2]<=B[0] or A[3]<=B[1] or A[0]>=B[2] or A[1]>=B[3]:
    #     return False,[]
# 上限错过去就不要了
    if A[2]<=B[0] or A[3]<=B[1] or A[0]>=B[2] or A[1]>=B[3] or B[1]<=A[1]:
        return False,[]
    else:
        x1=B[0] if B[0]>A[0] else A[0]
        y1=B[1] if B[1]>A[1] else A[1]
        x2 = B[2] if B[2] < A[2] else A[2]
        y2 = B[3] if B[3] < A[3] else A[3]

#计算box面积
        if  ((x2-x1)*(y2-y1))/((B[2]-B[0])*(B[3]-B[1]))>=0.2 or (x2-x1)*(y2-y1)>2400:
            w2=(x2-x1)/2
            h2 = (y2 - y1) / 2
            #回归yolo格式
            return True,[(x1-A[0]+w2) / box_size, (y1 - A[1] + h2) / box_size, (x2 - x1) / box_size, (y2 - y1) / box_size]
            # 回归两点格式
            # return True,[x1-A[0],y1-A[1],x2-A[0],y2-A[1]]
        else:
            return False, []
# lyx
def get_img_box(imgshape,box_w, stride):
    img_box_list=[]
    wnum=(imgshape[1]-box_w)//stride+1
    hnum = (imgshape[0] - box_w) // stride + 1
    for w in range(wnum+1):
        x=0
        y=0
        if w==wnum:
            x=imgshape[1]-box_w
        else:
            x=w*stride
        for h in range(hnum+1):
            if h == hnum:
                y = imgshape[0] - box_w
            else:
               y = h * stride
            img_box_list.append([x,y,x+box_w,y+box_w])
    return img_box_list
def cut_img(start,end):
    tic = time.time()
    img_list1 = img_list[start:end]
    box_size=1024
    for imgname in img_list1:
        print(imgname)
        if os.path.isfile(os.path.join(label_path,imgname[:-4]+".txt")):
            img_o=cv.imread(os.path.join(img_path,imgname))
            img = cv.resize(img_o, (0, 0), fx=1024/img_o.shape[1], fy=1024/img_o.shape[1])
            img_box_list = get_img_box(img.shape, 1024, 20)
            f = open(os.path.join(label_path,imgname[:-4]+".txt"))
            labels=f.readlines()
            f.close()
            box_list=[];
            for label in labels:
                label_box = label.split("\n")[0].split(" ")
                if len(label_box)==5:
                    if float(label_box[3])==0 or float(label_box[4])==0:
                        print("0")
                        continue
                    box=box_info(label_box,img.shape)
                    box_list.append(box)
                else:
                    continue
            for img_box in img_box_list:
                name="".join(random.sample(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9',], 6))
                cut_labels=[]
                for make_label in box_list:
                    have,box= in_or_out(img_box, make_label.box, box_size)
                    if have:
                        cut_labels.append(box_info(make_label.box_class,box))
                if len(cut_labels)>0:
                    image_clip = img[int(img_box[1]):(int(img_box[3])), int(img_box[0]):(int(img_box[2]))].copy()
                    f = open(os.path.join(save_path, name+ ".txt"),'w')
                    for cut_label in cut_labels:
                        # cv.rectangle(image_clip, (cut_label.box[0], cut_label.box[1]), (cut_label.box[2], cut_label.box[3]), (0, 255, 0), 1)
                        labei_info=str(cut_label.box_class)+" "+str(cut_label.box[0])+" "+str(cut_label.box[1])+" "+str(cut_label.box[2])+" "+str(cut_label.box[3])+"\n"
                        f.write(labei_info)
                    f.close()


                    cv.imwrite(os.path.join(save_path, name+ ".jpg"),image_clip)
                    #print(imgname,f"我是{name}子进程！",os.getpid())
        else:
            continue
        toc = time.time()
        shijian = toc-tic
    print('子进程',shijian)

tic = time.time()
# 35秒
#cut_img(0,len(img_list))
# [(0, 64), (64, 129), (129, 194)]
if __name__ == '__main__':
    process_list = []    # 存放开启的进程
    for i in range(thread_num):
        # 进程中的参数args表示调用对象的位置参数元组.注意：元组中只有一个元素时结尾要加","逗号
        p = Process(target=cut_img, args=(thread_list[i][0],thread_list[i][1]))
        p.start()
        process_list.append(p)
    for i in process_list:
        i.join()    # 阻塞每个子进程，主进程会等待所有子进程结束再结束主进程
    print("主进程结束！")
toc = time.time()
shijian = toc-tic
print('主进程',shijian)