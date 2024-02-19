有用的代码接口在src中
分别是
_utils.py,存放读取文件，读取图片，读取json信息等函数的通用函数
seg.py:传图并分割的原始函数
seg_interface.py:分割函数的接口api，可直接调用

detect:将分割图ocr识别并保存为json文件
get_info:将json文件中的txt项合并保存为txt文件，实现作文文本保存到txt文件中
