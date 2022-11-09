# -*- coding:utf-8 -*-
'''此函数的功能是递归将指定文件夹下的指定后缀的文件复制到目标路径下'''

import os
import shutil
cnt =0 
def searchDirFile(rootDir,saveDir):
    global cnt
    prename = '0000000'
    for dir_or_file in os.listdir(rootDir):
        filePath = os.path.join(rootDir, dir_or_file)
        # 判断是否为文件
        if os.path.isfile(filePath):
            # 如果是文件再判断是否以.jpg结尾，不是则跳过本次循环
            if os.path.basename(filePath).endswith('.xml'):
                cnt += 1
                print('imgBox fileName is '+ os.path.basename(filePath))
                # 拷贝jpg文件到自己想要保存的目录下
                shutil.copyfile(filePath,os.path.join(saveDir,os.path.basename(filePath)))
                shutil.copyfile(filePath[:-4] + '.jpg', os.path.join(saveDir, os.path.basename(filePath[:-4] + '.jpg')))
                os.rename(os.path.join(saveDir,os.path.basename(filePath)),os.path.join(saveDir,prename[:len(prename)-len(str(cnt))]+str(cnt)+'.xml'))
                os.rename(os.path.join(saveDir, os.path.basename(filePath[:-4] + '.jpg')),os.path.join(saveDir,prename[:len(prename)-len(str(cnt))]+str(cnt)+'.jpg'))

            else:
                continue
        # 如果是个dir，则再次调用此函数，传入当前目录，递归处理。
        elif os.path.isdir(filePath): 
            searchDirFile(filePath,saveDir)
        else:print('not file and dir '+os.path.basename(filePath))
    print('done')

if __name__ == '__main__':
    rootDir='/home/mengxianchi/train_img/AK_CLW/data/zip'

    saveDir=os.path.abspath(os.path.join(rootDir, ".."))
    saveDir = saveDir+ '/files'
    if not os.path.exists(saveDir):
        os.mkdir(saveDir)

    searchDirFile(rootDir,saveDir)