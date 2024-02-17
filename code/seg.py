#本文件用来将试卷分割为不同的图片形式，返回
#分割思路，利用opencv来把图片预处理，然后输出对应学生每个题目板块的图片到对应学生的文件夹下，并且新建一个txt文件保存学生信息
import cv2 as cv
import os
from PIL import Image
import numpy as np
class SegImg:
    def __init__(self,src_path,target_path):
        self.img_path=src_path   #原始答题卡图像路径
        self.target_path=target_path   #处理后图像存放路径

    ##首先定义一个读取文件夹图片的加载器，从指定的src_path读取图片，生成一个img的generator

    def image_loader(img_path):
        """
        Load images from a specified folder path.

        Args:
        - src_path (str): The path to the folder containing images.

        Yields:
        - img (PIL.Image.Image): Image loaded using PIL.
        """
        # Ensure the source path is valid
        if not os.path.isdir(img_path):
            raise ValueError("Invalid source path. Please provide a valid directory path.")

        # Iterate over files in the directory
        for filename in os.listdir(img_path):
            file_path = os.path.join(img_path, filename)
            # Check if the file is an image file
            if os.path.isfile(file_path) and any(file_path.endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.bmp']):
                try:
                    # Open image using PIL
                    img = Image.open(file_path)
                    yield img
                except Exception as e:
                    print(f"Error loading image {file_path}: {e}")

## 读取单张图片并返回
    def get_img(img_generator):
        try:
            img = next(img_generator)
            return img
        except StopIteration:
            pass

    # # Example usage:
    # if __name__ == "__main__":
    #     src_path = "D:\\大创\\考试相关数据集\\各类答题卡\\高中"
    #     img_sets = image_loader(src_path)
    #     get_img(img_sets)

## 答题卡图片预处理,二值化+去噪（正则化图像）
    def gaussian_blur_and_threshold(image):
        #读入的PIL的img转为array处理
        img_array = np.array(image)

        # 使用高斯滤波去噪,采用1,1卷积核可以尽可能保留更多信息
        blurred = cv.GaussianBlur(img_array, (1,1), 0)

        # 将图像转换为灰度图
        gray = cv.cvtColor(blurred, cv.COLOR_BGR2GRAY)

        # 对图像进行二值化
        _, thresholded = cv.threshold(gray, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)

        #将array转回img
        thresholded=Image.fromarray(thresholded)
        return thresholded

##获取矩形扫描，获取矩形
    def get_rectangle(img):
        # 讲读入的PIL的img转为array处理
        img_array = np.array(img)
        # 进行轮廓检测

        contours, _ = cv.findContours(img_array, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

        # 遍历所有轮廓
        for contour in contours:
            # 获取轮廓的矩形边界框
            x, y, w, h = cv.boundingRect(contour)
            # 绘制矩形边界框
            cv.rectangle(img_array, (x, y), (x + w, y + h), (0, 255, 0), 2)
            # 计算文本位置
            text_position = (x + int(w / 2), y + int(h / 2))
            # 绘制文本
            cv.putText(img_array, "rectangle", text_position, cv.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
            # 将array转回img
        rec_img= Image.fromarray(img_array)
        return rec_img
 #Example usage:
    if __name__ == "__main__":
        src_path = "D:\\大创\\考试相关数据集\\各类答题卡\\高中"
        img_sets = image_loader(src_path)
        src_img=get_img(img_sets)
        src_img.show()
        proc_img=gaussian_blur_and_threshold(src_img)
        proc_img=get_rectangle(proc_img)
        proc_img.show()