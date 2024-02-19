import os.path

import _utils
import detect
import json
#获取json中的所有txt信息，拼接到一起汇总为txt文件
class GetInfo:
    def read_all_txts(json_path,target_path):
            ##args:
            ##json_path:存放第二次处理的json文件的文件夹地址
            ##target_path:存放最终识别出的学生文本的txt文件的存放地址



            #获取所有json的路径
            json_dirc=_utils.read_all_json_files(json_path)
            # 存储所有的 txt 项信息
            all_txts = []

            # 读取每个 JSON 文件并解析其中的 txt 项信息
            for file in json_dirc:
                with open(file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    for item in data:
                        for txts in item:
                            all_txts.append(txts["text"])

                # 将 txt 项信息写入新的 TXT 文件中
                if os.path.isdir(target_path) == False:
                    os.mkdir(target_path)
                txt_file_path=os.path.join(target_path,f"combined_text.txt")
                with open(txt_file_path, "w", encoding="utf-8") as f:
                    for txt in all_txts:
                        f.write(txt + "\n")



##example
    if __name__=="__main__":
        src_path="D:\\大创\\考试相关数据集\\exam_result\\json_files"
        target_path="D:\\大创\\考试相关数据集\\exam_result\\txt_files"
        read_all_txts(src_path,target_path)