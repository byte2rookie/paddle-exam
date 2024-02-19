import cv2 as cv
import os
from PIL import Image
import numpy as np

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

##获取文件夹下所有的json文件

def read_all_json_files(target_folder):
    # 存储所有的 JSON 文件路径
    json_files = []

    # 遍历目标文件夹中的所有文件
    for file in os.listdir(target_folder):
        # 拼接文件的完整路径
        file_path = os.path.join(target_folder, file)
        # 判断文件是否为 JSON 文件
        if file.endswith('.json'):
            json_files.append(file_path)
    return json_files

