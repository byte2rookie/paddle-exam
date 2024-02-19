from seg import SegImg

class seg_interface:
    def forward(src_path,target_path,mode,kernal_size=(5,5)):
        ##############################################################
        #############################################################
        ## args
        ## src_path:原始图片所在的文件夹   target_path:存放切片的文件夹
        ## mode:设置识别的模式，包括normal模式，artical模式，deep模式
        ## normal对应普通的非作文题     artical对应作文题     deep 对应初次切片的再分割
        ##kernal_size对应的高斯核，为一个二元tuple，元素必须为相同的奇数
        #############################################################
        #############################################################
        ## 最后效果:
        ## 在target_path的目录下新建一个first_img文件夹，并在其中依次放入处理后的试卷图片





        img_sets = SegImg.image_loader(src_path)
        for src_img in img_sets:
            #图片处理
            proc_img = SegImg.gaussian_blur_and_threshold(src_img, args=mode,ksize=kernal_size)
            # 获取所有矩形信息并找到最大的矩形
            pos, recs = SegImg.get_rectangle_plots(proc_img)
            large_rec = SegImg.find_large_rectangles(recs, mode=mode)

            #获取了处理后的图片效果
            # prc_img = SegImg.draw_rectangle(large_rec, src_img)
            SegImg.crop_and_save_rectangles(src_img, target_path, large_rec)
            #在target_path的目录下新建一个first_img文件夹，并在其中依次放入处理后的试卷图片

# 使用方法示范
    if __name__=="__main__":
        src_path="D:\\大创\\考试相关数据集\\exams"
        tar_path="D:\\大创\\考试相关数据集\\exam_result"
        forward(src_path,tar_path,mode="artical")