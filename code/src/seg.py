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
    def gaussian_blur_and_threshold(image,args="normal",ksize=(5,5)):
        #读入的PIL的img转为array处理
        img_array = np.array(image)

        # 使用高斯滤波去噪,采用1,1卷积核可以尽可能保留更多信息
        blurred = cv.GaussianBlur(img_array, ksize, 0)


        # 将图像转换为灰度图
        gray = cv.cvtColor(blurred, cv.COLOR_BGR2GRAY)
        #进行canny算子进行边缘锐化
        normalargs=(110,220)
        articalarg = (240, 255)
        arg = normalargs
        if args=="artical":
            arg=articalarg


        thresholded=cv.Canny(gray,arg[0],arg[1])
        # # 对图像进行二值化
        # _, thresholded = cv.threshold(gray, 160, 255, cv.THRESH_BINARY)

        #将array转回img
        thresholded=Image.fromarray(thresholded)
        return thresholded


#对读入的img进行深层次的切割
    # def deepen_seg(img):



    def find_max_rectangle(rectangles):
        max_area = 0
        max_rectangle = None
        max_pos=[]
        # 遍历所有轮廓

        for rectangle in rectangles:
            # 获取轮廓的矩形边界框
            x, y, w, h = cv.boundingRect(rectangle)
            # 计算矩形的面积
            area = w * h
            # 更新最大矩形信息
            if area > max_area:
                max_area = area
                max_rectangle = rectangle
                max_pos=[[x,y,w,h]]

        return max_rectangle,max_pos

#获取大于一定大小的所有矩形
    def find_large_rectangles(rectangles,mode="artical"):
        large_rectangles = []
        if mode =="artical":
            min_width=800
            min_height=600
        if mode =="normal":
            min_width=200
            min_height=50
        if mode =="deep":
            min_width=200
            min_height=10
        # 遍历所有矩形
        for rect in rectangles:
            x, y, w, h = cv.boundingRect(rect)
            # 检查矩形的宽度和高度是否都大于指定的大小
            if w > min_width and h > min_height:
                large_rectangles.append([x,y,w,h])

        return large_rectangles

    ##获取矩形扫描，获取矩形
    def get_rectangle_plots(img):

        # 讲读入的PIL的img转为array处理
        img_array = np.array(img)
        # 进行轮廓检测
        contours, _ = cv.findContours(img_array, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        plots=[]
        # 遍历所有轮廓
        for contour in contours:
            # 获取轮廓的矩形边界框
            x, y, w, h = cv.boundingRect(contour)
            plots.append([x,y,w,h])


            # 将array转回img
        rec_img= Image.fromarray(img_array)
        return plots,contours

    def draw_rectangle(pos, img):
        # 读取图片
        img_array = np.array(img)

        # 读取坐标并绘制矩形
        for i, (x, y, w, h) in enumerate(pos):
            # 绘制矩形框
            cv.rectangle(img_array, (x, y), (x + w, y + h), (0, 255, 255), 3)

            # 添加红色文字标记
            text = str(i + 1)
            font = cv.FONT_HERSHEY_SIMPLEX
            font_scale = 1
            font_thickness = 2
            text_size, _ = cv.getTextSize(text, font, font_scale, font_thickness)
            text_origin = (x + w - text_size[0], y + text_size[1])
            cv.putText(img_array, text, text_origin, font, font_scale, (0, 0, 255), font_thickness, cv.LINE_AA)

        rec_img = Image.fromarray(img_array)
        return rec_img




#对识别出的矩形按照从左上到右下的方式进行排序
    def sort_rectangles(rectangles):
        # 按照左上角的 x 坐标进行排序
        sorted_rectangles = sorted(rectangles, key=lambda rect: (rect[0], rect[1]))
        return sorted_rectangles

    #裁剪后保存
    def crop_and_save_rectangles(src_img,target_path, rectangles):


        target_path=os.path.join(target_path,"first_img")
        if not os.path.exists(target_path):
            os.makedirs(target_path)

        # 依次裁剪并保存矩形
        crops=[]
        for i, (x, y, w, h) in enumerate(rectangles, start=1):
            # 裁剪图像
            img_array = np.array(src_img)
            cropped_img = img_array[y:y + h, x:x + w]
            cropped_img_area=w*h
            #计算原图的面积
            src_img_area=img_array.shape[0]*img_array.shape[1]


            if cropped_img_area/src_img_area <0.7:
                # 保存裁剪后的图像,且该图像必须小于原图的70%（防止切片失败）
                # 裁剪后的所有的图的坐标也要比对，删除相邻相似的嵌套矩形的情况

                r_path=os.path.join(target_path,f"croped_img_{i}.jpg")

                cv.imencode('.jpg', cropped_img)[1].tofile(r_path)




#封装为一个大的接口



 #Example usage:
    if __name__ == "__main__":
        src_path = "D:\\大创\\考试相关数据集\\各类答题卡\\8"

        img_sets = image_loader(src_path)
        src_img=get_img(img_sets)
        src_img.show()

        proc_img=gaussian_blur_and_threshold(src_img,args="artical")
        proc_img.show()
        #获取所有矩形信息并找到最大的矩形
        pos,recs=get_rectangle_plots(proc_img)
        # max_rec,max_pos=find_max_rectangle(recs)
        large_rec=find_large_rectangles(recs,mode="artical")
        prc_img=draw_rectangle(large_rec,src_img)
        prc_img.show()

        target_path="D:\\大创\\考试相关数据集\\results\\2"
        crop_and_save_rectangles(src_img,target_path,large_rec)
        #效果实现了对答题卡的不同矩形的分割

        ##实验：对切割后的图形再次切割
        src_path2="D:\\大创\\考试相关数据集\\results\\2"
        img_sets = image_loader(src_path2)
        src_img2 = get_img(img_sets)
        src_img.show()
        proc_img = gaussian_blur_and_threshold(src_img2, args="artical")
        proc_img.show()
        # 获取所有矩形信息并找到最大的矩形
        pos, recs = get_rectangle_plots(proc_img)
        # max_rec,max_pos=find_max_rectangle(recs)
        large_rec = find_large_rectangles(recs, mode="artical")
        prc_img = draw_rectangle(large_rec, src_img2)
        prc_img.show()

        target_path = "D:\\大创\\考试相关数据集\\results\\2\\1"
        crop_and_save_rectangles(src_img2, target_path, large_rec)
        ##再次切割后可以实现对不同模块的解耦
        ##然后使用paddleocr表单识别功能即可


        # #继续对result目录下的每张都进行继续分割
        # src_path2="D:\\大创\\考试相关数据集\\results"
        # img_sets2 = image_loader(src_path)
        # for img in img_sets2:
        #     img.show()
        #     proc_img = gaussian_blur_and_threshold(img)
        #     # 获取所有矩形信息并找到最大的矩形
        #     pos, recs = get_rectangle_plots(proc_img)
        #     # max_rec,max_pos=find_max_rectangle(recs)
        #     large_rec = find_large_rectangles(recs, 50, 50)
        #     prc_img = draw_rectangle(large_rec, img)
        #     prc_img.show()
        #
        #     target_path = "D:\\大创\\考试相关数据集\\results\\finals"
        #     crop_and_save_rectangles(src_img, target_path, large_rec)
        #



        #然后再分别保存每个矩形的图形到本地中
        #利用paddleocr的表单识别功能对每张图片提取文字信息

#TODO 接下来针对作文题和其他题的参数进行一个不同的制定，作文题采用一套参数，普通采用另一参数