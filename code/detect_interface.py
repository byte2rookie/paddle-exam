import detect
from detect import Gdetect
import json
import os
import cv2 as cv
import numpy as np

import _utils
from PIL import Image
from paddleocr import PaddleOCR, draw_ocr
##本接口可以实现将初次裁剪的图片进行文本的检测，并提取到对应的文件夹下
class detect_interface:

    def detect(first_processed_path,tar_path):
        ## args:
        ## first_processed_path  初次处理的文件夹地址
        ## tar_path              json文件存放的地址


        detect.Gdetect.detect_img(first_processed_path,tar_path)
        print(f"srouce is {first_processed_path}")
        print(f"json files saved in {tar_path}")

## example:
    if __name__=="__init__":
        first_processed_path="D:\\大创\\考试相关数据集\\exam_result\\first_img"
        final_processed_path="D:\\大创\\考试相关数据集\\exam_result\\json_files"
        detect(first_processed_path,final_processed_path)
