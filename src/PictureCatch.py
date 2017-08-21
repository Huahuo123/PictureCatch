#coding=utf-8
#_author_ = 'wusehuahuo'
#_date_ = '2017.8.9'
#_This is application to download the pictures from anime-pictures.net.

#import modules
import sys
import urllib
import urllib.request
import os
import re
import time
import socket
import os.path
import shutil

#全局变量
#模式1
startPageMode1 = 0
endPageMode1 = 0
#模式2
keyWord = ""
startPageMode2 = 0
endPageMode2 = 0

#菜单
print ("-------------------------------------------------------------------")
print ("----------------------------   菜单   -----------------------------")
print ("-------------------------------------------------------------------")
print ("-                                                                 -")
print ("----------------------   模式1:按页抓取    -----------------------")
print ("-                                                                 -")
print ("----------------------   模式2:按关键词抓取    -------------------")
print ("-                                                                 -")
print ("-------------------------------------------------------------------\n")

#获取系统时间
timeStr = time.localtime(time.time())

#今日图站概况
#请求地址
urlToday = "https://anime-pictures.net/pictures/view_posts/0?lang=en"
#请求头
headersToday = {'Accept':'*/*', 
        'Accept-Language':'zh-CN',
        '':'','User-Agent':'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1)',
        'Connection':'Keep-Alive'}
#包装
def getTodayInfo(urlToday):
    urlTodayRequest = urllib.request.Request(urlToday,headers = headersToday)
    pageToday = urllib.request.urlopen(urlTodayRequest)
    htmlToday = pageToday.read()
    htmlCodeToday = htmlToday.decode('gbk')
    #正则截取规则
    reRulesToday = re.compile(r'(\d{6})\s{1}pictures',re.I|re.M|re.S)
    #匹配结果
    infoList = re.findall(reRulesToday,htmlCodeToday)
    return infoList

#显示当前时间
timeNow = time.strftime('%Y-%m-%d %H:%M:%S',timeStr) 
#图站图片数量
pictureNum = getTodayInfo(urlToday)
#图站页数
pageNum = str(round(int(pictureNum[0]) / 80))
print ("***************************今日图站概况****************************")
print ("**************    当前时间：" + timeNow + "    ****************" )
print ("**************    当前图站图片数量：" + pictureNum[0] + "         ****************" )
print ("**************    当前图站页面数量：" + pageNum + "页         ****************\n" )

#模式选择
while True:
	print ("请选择模式：1 | 2 (按1或2选择模式)\n")
	mode = input("选择模式：")
	if mode == "1":
		print ("您选择的模式是：按页抓取\n")
		break
	elif mode == "2":
		print ("您选择的模式是：按关键词抓取\n")
		break
	else:
		print ("抱歉没有这个选项哦！请您重新选择！\n")

#格式化系统时间
timeDate = time.strftime('%Y-%m-%d %H-%M-%S',timeStr)        

#创建当前工作目录
workDir = os.getcwd() + "\\当前目录"
if os.path.isdir(workDir):
    print ("当前目录已存在！\n")
else:
    print ("当前目录不存在！已创建\n")
    os.mkdir(workDir)

#搜索函数
def search(keyWords):
    if keyWords == "help()":
        if os.path.exists(r'C:/Program Files (x86)/Internet Explorer/iexplore.exe'):
            print ("还能怎么办，问百度呗！ 正在打开百度..........")
            os.system("start C:\\\"Program Files (x86)\"\\\"Internet Explorer\"\\iexplore.exe www.baidu.com")
        else:
            print ("IE浏览器都没有了！！！！")
#输入相应的参数-按页抓取
while True:
    if mode == "1":
        #创建当前模式目录
        mode1Dir = workDir + "\\按页抓取目录" + timeDate       
        os.mkdir(mode1Dir)
        #创建当前图片下载地址保存目录
        os.mkdir(mode1Dir + "\\图片地址目录")
        #创建当前图片下载目录
        os.mkdir(mode1Dir + "\\图片下载目录")
        print ("请输入要抓取的起始页：\n")
        startPageMode1 = input ("起始页= ")
        print ("\n")
        print ("请输入要抓取的末尾页：\n")
        endPageMode1 = input ("末尾页= ")
        if startPageMode1 <= endPageMode1:
            if int(endPageMode1) > pageNum:
                print ("输入页码超过图站页面数目了哦，请重新输入吧！\n")
                shutil.rmtree(mode1Dir)
                continue
            elif int(endPageMode1) - int(startPageMode1) > 20:
                print ("一次性抓取最好不要超过20页哦，请重新输入吧！\n")
                shutil.rmtree(mode1Dir)
                continue
            else:
                break
        else:
            print ("您的输入不合法哦！起始页应小于尾页哦，请重新输入吧！")
            shutil.rmtree(mode1Dir)
            continue
        
    #输入相应的参数-按关键词抓取
    if mode == "2":
        #创建当前模式目录
        mode2Dir = workDir + "\\按关键词抓取目录" + timeDate
        os.mkdir(mode2Dir)
        #创建当前图片下载地址保存目录
        os.mkdir(mode2Dir + "\\图片地址目录")
        #创建当前图片下载目录
        os.mkdir(mode2Dir + "\\图片下载目录")
        print ("请输入要抓取的关键词：\n")
        print ("支持多个关键词，请用“+”相连！请使用[ 英文 ]或[ 日文 ]关键词！！！")
        print ("不知道输入外文怎么办？输入：help()\n")
        keyWord = input ("关键词= ")
        if keyWord == "help()":
            search(keyWord)
            keyWord = input ("关键词= ")
            break
        else:
            break
#获取请求网页源代码
#定义一个getHtml()函数
def getHtml(url):
    urlRequest = urllib.request.Request(url,headers = headersToday)
    page = urllib.request.urlopen(urlRequest)
    htmlCode = page.read()
    return htmlCode

#正则表达式截取ID和分辨率函数
def getId(pageString):
    #定义索引
    index = 0
    #以gbk重新编码网页代码
    pageCode = pageString.decode('gbk')
    #通配符定义
    #图片id
    reRulesId = re.compile(r'common_preview_img_(\d+)',re.I|re.M|re.S)
    #图片分辨率
    reRulesPx = re.compile(r'Anime picture (\d+)x(\d+)',re.I|re.M|re.S)
    #图片格式
    reRulesExt = re.compile(r'cp.(...).webp',re.M)
    #结果列表
    idList = re.findall(reRulesId,pageCode)
    PxList = re.findall(reRulesPx,pageCode)
    ExtList = re.findall(reRulesExt,pageCode)
    #合并Id与分辨率
    resultList = []
    while index < len(idList):
        strTemp = ""
        strTemp = idList[index] + "-" + PxList[index][0] + "x" + PxList[index][1] + "*." + ExtList[index]
        resultList.append(strTemp)
        index += 1
    return resultList

#图片下载头部地址
addressHead = "https://anime-pictures.net/pictures/get_image/"

#下载进度回调函数
def schedule(blocknum,blocksize,totalsize):
    '''
    @回调函数
    @blocknum:已下载的数据块数量
    @blocksize:数据块大小
    @totalsize:下载文件大小
    '''
    per = 100.0 * blocknum * blocksize / totalsize
    if per > 100:
        per = 100
    
    if (int(per) / 10) in range(0,11):
        rate = '%.2f%%' % int(per)
        sys.stdout.write(rate)
        sys.stdout.flush()
    if per == 100:
        print ("完成！")

#检查下载图片是否损坏函数
def check(pictureName):
    #图片路径
    if mode == "1":
        pictureDirPath = workDir + "\\按页抓取目录" + timeDate + "\\图片下载目录\\" + pictureName + ".jpg"
    if mode == "2":
        pictureDirPath = workDir + "\\按关键词抓取目录" + timeDate + "\\图片下载目录\\" + pictureName + ".jpg"
    #图片大小(KB)
    filesize = os.path.getsize(pictureDirPath) / 1024
    if filesize < 100:
        isOk = False
    else:
        isOk = True
    return isOk

#下载图片函数
def downloadPicture(picturesUrlList,downloadPath):
    print ("正在下载图片........")
    indexPictureList = 0
    while indexPictureList < len(picturesUrlList):
        #定义图片名字
        pictureName = ""
        pictureName = "第" + str(indexPictureList) + "张"
        #定义图片路径
        picturePath = downloadPath + pictureName + ".jpg"
        #保存
        print ("正在下载" + pictureName + ":")
        #设置20S超时
        socket.setdefaulttimeout(20)
        urllib.request.urlretrieve(picturesUrlList[indexPictureList],picturePath,schedule)
        #检查下载图片是否损坏
        print ("正在检查图片........")
        if check(pictureName) == True:
            print ("图片完整！")
        else:
            print("图片损坏！正在重新下载..........")
            reDownloadPath = re.sub(".jpg",".png",picturesUrlList[indexPictureList])
            urllib.request.urlretrieve(reDownloadPath,picturePath,schedule)
        indexPictureList += 1
    print ("完成！共计：" + str(indexPictureList) + "张图片")

#图片下载地址存储函数
def saveDownloadUrl(filePath,content):
    print ("正在保存下载地址........")
    indexContent = 0
    fp = open(filePath,"w")
    while indexContent < len(content):
        fp.write(content[indexContent] + "\n")
        indexContent += 1
    fp.write("共计 " + str(indexContent) + " 张图片")
    fp.close()
    print ("完成！共计：" + str(indexContent) + "张图片")
    time.sleep(2)

#构造地址函数
def buildAddress(addressHeadTemp,EndList):
    downloadUrlList = []
    indexEndList = 0
    while indexEndList < len(EndList):
        addressTemp = ""
        addressTemp = addressHeadTemp + EndList[indexEndList]
        downloadUrlList.append(addressTemp)
        indexEndList += 1
    return downloadUrlList

#构造按页抓取地址
addressFirst = "https://anime-pictures.net/pictures/view_posts/"
addressEnd = "?lang=en"

#模式1处理模块
#转换页码为int
pageNumStart = int(startPageMode1)
pageNumEnd = int(endPageMode1)
if mode == "1":
    #是否下载图片判断标志
    isDownloadMode1 = True
    choice = ""
    while pageNumStart <= pageNumEnd:
        #请求地址
        addressMode1 = addressFirst + str(pageNumStart) + addressEnd
        #当前处理页码
        pageName = "第" + str(pageNumStart) + "页"
        print ("正在处理" + pageName + addressMode1)
        #请求页面
        stringMode1 = getHtml(addressMode1)
        #获得id与分辨率列表
        addressEndList = getId(stringMode1)
        #获得下载地址列表
        downloadList = buildAddress(addressHead,addressEndList)
        #保存文件路径
        filePathDownload = workDir + "\\按页抓取目录" + timeDate + "\\图片地址目录\\" + pageName + ".txt"
        #存储
        saveDownloadUrl(filePathDownload,downloadList)
        #提示是否下载图片
        if isDownloadMode1 == True:
            choice = input ("您是否要下载所有图片？(y/n)")
            isDownloadMode1 = False
        if choice == "y":
            #下载图片路径
            picturePathDownload = workDir + "\\按页抓取目录" + timeDate + "\\图片下载目录\\"
            #下载图片
            downloadPicture(downloadList,picturePathDownload)
        elif choice == "n":
            print ("不下载图片！")
        else:
            print ("不支持的选项，默认不下载图片！")
        #状态
        print ("完成！")
        pageNumStart = pageNumStart + 1

#模式2处理模块
#输入页面检查函数
def checkInputPage(startPage,endPage,pageNum):
    if startPage <= endPage:
        if int(endPageMode1) > pageNum:
            print ("输入页码超过图站页面数目了哦，请重新输入吧！\n")
            return False
        elif int(endPageMode1) - int(startPageMode1) > 20:
            print ("一次性抓取最好不要超过20页哦，请重新输入吧！\n")
            return False
        else:
            return True
    else:
        print ("您的输入不合法哦！起始页应小于尾页哦，请重新输入吧！")
        return False
#头地址
addressHeadMode2 = "https://anime-pictures.net/pictures/view_posts/0?search_tag="
#末尾参数
addressEndMode2 = "&order_by=date&ldate=0&lang=en"
if mode == "2":
    #是否下载图片判断标志
    isDownloadMode2 = True
    choiceMode2 = ""
    #提示输入的关键词
    print ("您输入的关键词是： " + keyWord  + "\n")
    #请求地址
    addressMode2 = addressHeadMode2 + keyWord + addressEndMode2
    #请求页面
    stringMode2 = getHtml(addressMode2)
    #获取搜索结果信息
    htmlCodeMode2 = stringMode2.decode('gbk')
    #正则截取规则
    reRulesMode2 = re.compile(r'(\d+)\s{1}pictures<br>',re.I|re.M|re.S)
    #匹配结果
    infoListMode2 = re.findall(reRulesMode2,htmlCodeMode2)
    #显示搜索结果图片数量
    print ("关于: " + keyWord + "的图片共有： " + infoListMode2[0] + "张")
    #显示搜索结果页面数量
    pictureNumMode2 = round(int(infoListMode2[0]) / 80)
    print ("搜索结果页面共有： " + str(pictureNumMode2) + "页\n")
    #下载图片提示
    while True:
        print ("请输入要抓取的页面")
        startPageMode2 = input ("起始页= ")
        endPageMode2 = input ("末尾页= ")
        #检查输入页面参数
        flag = checkInputPage(startPageMode2,endPageMode2,pictureNumMode2)
        if flag == False:
            continue
        else:
            break
    #转换页码为int
    pageNumStartMode2 = int(startPageMode2)
    pageNumEndMode2 = int(endPageMode2)
    #下载图片
    while pageNumStartMode2 <= pageNumEndMode2 :
        #当前处理页码
        pageNameMode2 = "第" + str(pageNumStartMode2) + "页"
        print ("正在处理" + pageNameMode2)
        #获得id与分辨率列表
        addressEndListMode2 = getId(stringMode2)
        #获得下载地址列表
        downloadListMode2 = buildAddress(addressHead,addressEndListMode2)
        #保存文件路径
        filePathDownloadMode2 = workDir + "\\按关键词抓取目录" + timeDate + "\\图片地址目录\\" + pageNameMode2 + ".txt"
        #存储
        saveDownloadUrl(filePathDownloadMode2,downloadListMode2)
        #提示是否下载图片
        if isDownloadMode2 == True:
            choiceMode2 = input ("您是否要下载所有图片？(y/n)")
            isDownloadMode2 = False
        if choiceMode2 == "y":
            #下载图片路径
            picturePathDownloadMode2 = workDir + "\\按关键词抓取目录" + timeDate + "\\图片下载目录\\"
            #下载图片
            downloadPicture(downloadListMode2,picturePathDownloadMode2)
        elif choiceMode2 == "n":
            print ("不下载图片！")
        else:
            print ("不支持的选项，默认不下载图片！")
        #状态
        print ("完成！")
        pageNumStartMode2 = pageNumStartMode2  + 1