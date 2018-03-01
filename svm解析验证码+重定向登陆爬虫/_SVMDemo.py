import os  
import sys  
import random  
import os.path  
from PIL import Image, ImageEnhance, ImageFilter  
from svmutil import *  
  
##记录像素点的值，描述特征，采用遍历每个像素点统计黑色点的数量  
def GetFeature(imgCropImg, nImgHeight, nImgWidth):  
    PixelCountList = []  
    for y in range(nImgHeight):  
        CountX = 0  
        for x in range(nImgWidth):  
            if imgCropImg.getpixel((x, y)) == 0:  
                CountX += 1  
        PixelCountList.append(CountX)  
    for x in range(nImgWidth):  
        CountY = 0  
        for y in range(nImgHeight):  
            if imgCropImg.getpixel((x, y)) == 0:  
                CountY += 1  
        PixelCountList.append(CountY)  
    return PixelCountList  
  
##输出向量数据  
def OutPutVectorData(strID, strMaterialDir, strOutPath):  
    for ParentPath, DirNames, FileNames in os.walk(strMaterialDir):  
        with open(strOutPath, 'a') as fpFea:  
            for fp in FileNames:  
                #图片文件路径信息  
                strFullPath = os.path.join(ParentPath, fp)  
  
                #打开图片  
                imgOriImg = Image.open(strFullPath)  
  
                #生成特征值  
                FeatureList = GetFeature(imgOriImg, 15, 13)  
  
                strFeature = strID + ' '  
                nCount = 1  
                for i in FeatureList:  
                    strFeature = '%s%d:%d ' % (strFeature, nCount, i)  
                    nCount += 1  
                fpFea.write(strFeature + '\n')  
                fpFea.flush()  
        fpFea.close()  
  
#训练SVM模型  
def TrainSvmModel(strProblemPath, strModelPath):  
    Y, X = svm_read_problem(strProblemPath)  
    Model = svm_train(Y, X)  
    svm_save_model(strModelPath, Model)  
  
#SVM模型测试  
def SvmModelTest(strProblemPath, strModelPath):  
    TestY, TestX = svm_read_problem(strProblemPath)  
    Model = svm_load_model(strModelPath)  
    #返回识别结果  
    pLabel, pAcc, pVal = svm_predict(TestY, TestX, Model)  
    return pLabel  
  
  
##输出测试向量数据  
def OutPutTestVectorData(strID, strDir, strOutPath):  
    fileList = []  
    for parentPath, strDir, fileName in os.walk(strDir):  
        fileList = fileName  
    with open(strOutPath, 'a') as fpFea:  
        for fp in fileList:  
            #图片文件路径信息  
            strFullPath = os.path.join(parentPath, fp)  
  
            #打开图片  
            imgOriImg = Image.open(strFullPath)  
  
            #生成特征值  
            FeatureList = GetFeature(imgOriImg, 15, 12)  
  
            strFeature = strID + ' '  
            nCount = 1  
            for i in FeatureList:  
                strFeature = '%s%d:%d ' % (strFeature, nCount, i)  
                nCount += 1  
            fpFea.write(strFeature + '\n')  
            fpFea.flush()  
        fpFea.close()  
  
  
def main():  
# 1.循环输出向量文件  
    for i in range(0, 10):  
        strID = '%d' % i  
        OutPutVectorData(strID, 'D:/1/step3/' + strID, 'D:/1/step4/Vector.txt')  
  
# 2.调用函数训练SVM模型  
    TrainSvmModel('D:/1/step4/Vector.txt', 'D:/1/step5/Model.txt')  
# 3.调用函数识别结果  
    pLabel = SvmModelTest('D:/1/step6/Vector.txt', 'D:/1/step5/Model.txt')  
    for i in pLabel:  
        print('%d' % i)  
if __name__ == '__main__':  
    main()  
