import requests
import _PicDealWith  
import os  
import random  
import _SVMDemo  
import time
import re

headers={
'Host': 'www.zhifuxt.com:8280',
'Connection': 'keep-alive',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36',
'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
'Referer': 'http://www.zhifuxt.com:8280/prm/',
'Accept-Encoding': 'gzip, deflate',
'Accept-Language': 'zh-CN,zh;q=0.9'
}
# i =random.randint(1,999999)
# print(i)
url='http://www.zhifuxt.com:8280/prm/auth/genCaptcha.do?dt=1519812842113'

ss=requests.session()
html = ss.post(url,headers=headers)
# #写出图片
with open('D:/1/test/yzm.png','wb') as f:
    f.write(html.content)
	
	
	##测试  
g_Count = 0  
strDirPath = 'D:/1/test/'  
strFileName = 'yzm.png'  
#1.图片文件路径信息  
strFullPath = os.path.join(strDirPath, strFileName)  
#2.对图片进行处理  
#2.1二值化处理  
imgBinImg = _PicDealWith.BinaryzationImg(strFullPath)  
#2.2去除噪点  
imgClrImg = _PicDealWith.ClearNoise(imgBinImg)  
#2.3切割图片  
ImgList = _PicDealWith.GetCropImgs(imgClrImg)  
#2.3循环写入文件  
for img in ImgList:  
    strImgName = "%04d%04d.png" % (g_Count, random.randint(0, 9999))  
    strImgPath = os.path.join(strDirPath, strImgName)  
    img.save(strImgPath)  
    g_Count += 1  
  
print("OK")  
  
os.remove(strFullPath)  
  
#3.生成向量文件  
_SVMDemo.OutPutTestVectorData('0', 'D:/1/test/', 'D:/1/test/Vector.txt')  
  
#4.利用之前的模型文件进行识别测试  
pLabel = _SVMDemo.SvmModelTest('D:/1/test/Vector.txt', 'D:/1/step5/Model.txt')  
# for i in pLabel:  
#     print('%d' % i, end = '')  
# print(pLabel)
import shutil  
shutil.rmtree('D:/1/test') 
time.sleep(1)
os.mkdir('D:\\1\\test')


yzm=''.join(map(str,map(int,pLabel)))
header2={
    'Accept':'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding':'gzip, deflate',
    'Accept-Language':'zh-CN,zh;q=0.9',
    'Connection':'keep-alive',
    'Content-Length':'74',
    'Content-Type':'application/x-www-form-urlencoded',
    'Host':'www.zhifuxt.com:8280',
    'Origin':'http://www.zhifuxt.com:8280',
    'Referer':'http://www.zhifuxt.com:8280/prm/',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36',
    'X-Requested-With':'XMLHttpRequest'
}
form={'agentId':'8180102895',
'userId':'yixinjr',
'userPwd':'111111',
'captcha':yzm,
'reqType':'ajax'}

html1=ss.post('http://www.zhifuxt.com:8280/prm/auth/login.do',data=form,headers=header2)
result=ss.get ('http://www.zhifuxt.com:8280/prm/auth/mainPanel.do', cookies = html1.cookies)
header3={
'Accept':'application/json, text/javascript, */*; q=0.01',
'Accept-Encoding':'gzip, deflate',
'Accept-Language':'zh-CN,zh;q=0.9',
'Connection':'keep-alive',
'Content-Length':'27',
'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
'Host':'www.zhifuxt.com:8280',
'Origin':'http://www.zhifuxt.com:8280',
'Referer':'http://www.zhifuxt.com:8280/prm/auth/mainPanel.do',
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36',
'X-Requested-With':'XMLHttpRequest',
}
form1={'_random':'0.10016563519140287'}

result1=ss.get ('http://www.zhifuxt.com:8280/prm/mpomng/report/cday.do', cookies = result.cookies)

result2=(result1.content).decode('utf8')

amt=(re.findall(u'(?<=hisdayTran\":\")[0-9]*(?=\")',result2))[0]
amt=int(amt)/100

print(amt)