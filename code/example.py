import os

import src
from src import seg
from src.seg_interface import forward



from src.detect import detect_img
from src.get_info import read_all_txts

if __name__=="__main__":


#STEP1:切割


    #给出图片存放路径和结果存放路径
    src_path="./img/eg_img"
    target_path="./img/result"

    #forward函数用来对图片进行切割
    forward(src_path=src_path, target_path=target_path, mode="artical")
    print("seg_imgs saved in {}".format(target_path))
#等待执行结束
#会自动创建一个first_img存放格式为croped_imgxxx的文件夹

#STEP2:读取图片并生成json信息
    first_imgs_path=target_path+"/first_img"
    json_path="./img/result/jsons"
    detect_img(first_imgs_path,json_path)

#STEP3:读取json文件然后生成对应的tokens的txt文件
    txt_path=target_path+"/txts"
    read_all_txts(json_path,txt_path)

# 在这里导入 views.py 中的 ask 函数
from src.views import ask

# 调用 ask 函数
ask_result = ask(None)  # 传入一个虚拟的 request 对象，因为 ask 函数可能依赖于 request 对象

# 输出文心一言的回答
print(ask_result)

