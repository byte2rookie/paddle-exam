#本类的作用是实现将分割好的图片的内容通过paddleocr 生成一段json文件 其中包含原始的文段信息，原始的文字信息，整理后的信息
import json
import os
import cv2 as cv
import numpy as np

import _utils
from PIL import Image
from paddleocr import PaddleOCR, draw_ocr
class detect_interface:


    # Paddleocr目前支持的多语言语种可以通过修改lang参数进行切换
    # 例如`ch`, `en`, `fr`, `german`, `korean`, `japan`
    def detect_img(img_path,target_path):
        ## args:
        ## first_processed_path  初次处理的文件夹地址
        ## tar_path              json文件存放的地址
        ##实现的效果：
        ##读取第一次处理的文件夹目录下的图片，生成每个图片对应的识别的json文件并依次保存



        ocr = PaddleOCR(use_angle_cls=True, lang="ch")  # need to run only once to download and load model into memory

        img_sets= _utils.image_loader(img_path)
        if os.path.isdir(target_path) is False:
            os.mkdir(target_path)
        for i,img in enumerate(img_sets):
            img=np.array(img)
            result = ocr.ocr(img, cls=True)
            line_data=[]
            output_data=[]
            for idx in range(len(result)):
                res = result[idx]
                for line in res:
                    print(line)

            # 显示结果

            result = result[0]
            img=Image.fromarray(img)


            boxes = [line[0] for line in result]
            txts = [line[1][0] for line in result]
            scores = [line[1][1] for line in result]
            # im_show = draw_ocr(img, boxes, txts, scores, font_path='./fonts/simfang.ttf')
            # im_show=Image.fromarray(im_show)
            # im_show.show()

            #识别的图片信息
            for box, txt, score in zip(boxes, txts, scores):
                line_data.append({"box": box, "text": txt, "score": score})

            output_data.append(line_data)
            output_file = f"output_{i}.json"

            output_file=os.path.join(target_path,output_file)
            with open(output_file, "w",encoding='utf-8') as f:
                json.dump(output_data, f, indent=4, ensure_ascii=False)



#example
    if __name__ == "__main__":
        img_path = "D:\\大创\\考试相关数据集\\exam_result\\first_img"
        target_path="D:\\大创\\考试相关数据集\\exam_result\\json_files"
        detect_img(img_path,target_path)
