#coding=utf-8
import os  
import os.path  
from PIL import Image, ImageEnhance, ImageFilter  
import random  
  
#二值化处理  
#strImgPath 图片路径  
def BinaryzationImg(strImgPath):  
    #打开图片  
    imgOriImg = Image.open(strImgPath)  
  
    #增加对比度  
    pocEnhance = ImageEnhance.Contrast(imgOriImg)  
    #增加255%对比度  
    imgOriImg = pocEnhance.enhance(2.55)  
  
    #锐化  
    pocEnhance = ImageEnhance.Sharpness(imgOriImg)  
    #锐化200%  
    imgOriImg = pocEnhance.enhance(2.0)  
  
    #增加亮度  
    pocEnhance = ImageEnhance.Brightness(imgOriImg)  
    #增加200%  
    imgOriImg = pocEnhance.enhance(2.0)  
  
    #添加滤镜效果  
    imgGryImg = imgOriImg.convert('L').filter(ImageFilter.DETAIL)  
  
    #二值化处理  
    imgBinImg = imgGryImg.convert('1')  
  
    return imgBinImg  
  
#去除噪点  
def ClearNoise(imgBinImg):  
    for x in range(1, (imgBinImg.size[0]-1)):  
        for y in range(1,(imgBinImg.size[1] - 1)):  
        #一个点为黑色，周围8个点为白色，则此点为噪点，设置为白色  
            if imgBinImg.getpixel((x, y)) == 0 \
                and imgBinImg.getpixel(((x - 1), (y + 1))) == 255 \
                and imgBinImg.getpixel(((x - 1), y)) == 255 \
                and imgBinImg.getpixel(((x - 1), (y - 1))) == 255 \
                and imgBinImg.getpixel(((x + 1), (y + 1))) == 255 \
                and imgBinImg.getpixel(((x + 1), y)) == 255 \
                and imgBinImg.getpixel(((x + 1), (y - 1))) == 255 \
                and imgBinImg.getpixel((x, (y + 1))) == 255 \
                and imgBinImg.getpixel((x, (y - 1))) == 255:  
                imgBinImg.putpixel([x, y], 255)  
  
    return imgBinImg  
  
#切割图片  
def GetCropImgs(imgClrImg):  
    ImgList = []  
    for i in range(4):  
        x = 2.5 + i * 12 
        y = 3  
        SubImg = imgClrImg.crop((x, y, x + 12, y + 15))  
        ImgList.append(SubImg)  
    return ImgList  
  
  
#调用部分  
def main():  
    g_Count = 0  
    strStep1Dir = 'D:/1/step1/'  
    strStep2Dir = 'D:/1/step2/'  
    for ParentPath, DirName, FileNames in os.walk(strStep1Dir):  
        for i in FileNames:  
            #图片文件路径信息  
            strFullPath = os.path.join(ParentPath, i)  
            imgBinImg = BinaryzationImg(strFullPath)  
            imgClrImg = ClearNoise(imgBinImg)  
            ImgList = GetCropImgs(imgClrImg)  
            for img in ImgList:  
                strImgName = "%04d%04d.png" % (g_Count, random.randint(0, 9999))  
                strImgPath = os.path.join(strStep2Dir, strImgName)  
                img.save(strImgPath)  
                g_Count += 1  
  
    print("OK！")  
  
if __name__ == '__mian__':  
    main()  