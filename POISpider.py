# /*
#  * @Author: Muhaowei
#  * @Date: 2018-08-21 15:44:41
#  * @LastEditors: Muhaowei
#  * @LastEditTime: 2018-08-21 15:44:41
#  * @Description:
#  */
import requests, sys
import os
import time
import json
import math
import re


#矩形框
class Rect:
    def __init__(self, xmin, ymin, xmax, ymax):
        self.xmin = xmin
        self.ymin = ymin
        self.xmax = xmax
        self.ymax = ymax


class Cut:
    def __init__(self, POIType):
        self.POIType = POIType
        self.filePath = "MapPOI/" + POIType.replace('|', '&') + "_Range.txt"
        self.Url = "http://restapi.amap.com/v3/place/polygon?polygon="
        self.POIfile = "POIData/" + POIType.replace('|', '&') + ".txt"
        self.key = [
            "e1c74a1e2f6a8756552f0d508ee81885",
            "d8cea7350e1fdf682d165c698683fd12",
            "9658cb3e125f5f5c74cd624d23363f90",
            "75f04f38a81d2e68a8e362ab42c4055f",
            "dc44a8ec8db3f9ac82344f9aa536e678",
            "0e987256ddddf37b97d75059f9f8a398",
            "abade8caab769816481aa0e431000eeb",
            "ebd66ed6c7a36c42511f717170c10068",
            "d87d4aadb1fd0a6871c3843e1e20d5b2",
            "2f1ec17c11ca72ea7d27e02be8fff2d9",
            "4df2d12b66bb93ac523659d4b9a2f428",
            "f9dd0a3d819ff898be26fdff8bbc38b7",
            #xiaoen
            "6437ff2a98cad2273652ec5854dd3c04",
            "e541ae93677e658ae8beed863d3ea753",
            "967a226a235a653d665b5ca7c2278860",
            "ead3d505a19efdcd0a272bf55e00cf0e",
            "3bdcf0ffd5539b41336b3c0b0555ee2e",
            #chelei
            "abade8caab769816481aa0e431000eeb",
            "2740f0abff76179deb3b95cd6b39943a",
            "14ee8f50f5b4a4fe08edfc3d1dac481f",
            "987a2654d69ad23ffa822f9fd9dc0278",
            "0ec973eaba283558c382bb344ace69d5",
            "9658cb3e125f5f5c74cd624d23363f90",
            "75f04f38a81d2e68a8e362ab42c4055f",
            "8e24ed648ec8d31f1c2b6928df79cd6f",
            "82657cbe51b3f3dbae64a03e9ead87eb",
            "d829ba03622b43f5e1fc5243b5d16bec",
        ]
        self.keyNum = 0
        title = open('POIData/title.txt', 'r').read()
        open(self.POIfile, 'w').write(title)

    #下载数据
    def ReqHtml(self, Range, url):
        request = requests.get(url=url, timeout=(5, 27))
        html = request.text
        request.close()
        # print(url)
        # print(html)
        jsonData = json.loads(html)
        if jsonData['status'] == '1':
            print(url + ' keynum' + str(self.keyNum))
        else:
            self.keyNum = self.keyNum + 1
            print(self.keyNum)
            url = re.sub(r'&key=.*&extensions',
                         '&key=' + self.key[self.keyNum] + '&extensions', url)
            html = self.ReqHtml(Range, url)
            print(html)
        return html

    def DownHtml(self, Range, num=0):
        print(self.keyNum)
        url = self.Url + Range + "&key=" + self.key[self.
                                                    keyNum] + "&extensions=all&offset=20&page=" + str(
                                                        num
                                                    ) + "&types=" + self.POIType
        print(url)
        try:
            html = self.ReqHtml(Range, url)
        except:
            time.sleep(60)  # 休眠1秒
            html = self.ReqHtml(Range, url)
        return html

    def POIWrite(self, Range, count):
        Page = math.ceil(count / 20)
        print(count, Page)
        for num in range(1, Page + 1):
            data = self.DownHtml(Range=Range, num=num)
            POIData = json.loads(data).get("pois")
            for POIDict in POIData:
                POIArr = list(POIDict.values())
                POIArr = [str(value).replace(',', '，') for value in POIArr]
                POILine = ','.join(POIArr) + '\n'
                open(self.POIfile, 'a', encoding='utf-8').write(POILine)

    #切分地块
    def CutChina(self, rect):
        Range = str(rect.xmin) + "," + str(rect.ymin) + "," + str(
            rect.xmax) + "," + str(rect.ymax)
        data = self.DownHtml(Range=Range)
        # print(data)
        jsonData = json.loads(data)
        count = int(jsonData['count'])
        if count < 500:
            file = open(self.filePath, "a")
            file.writelines(
                str(rect.xmin) + "," + str(rect.ymin) + "," + str(rect.xmax) +
                "," + str(rect.ymax) + "," + str(count) + "\n")
            file.close()
            self.POIWrite(Range, count)
            print("写入数据")
        else:
            middleX = (rect.xmin + rect.xmax) / 2
            middleY = (rect.ymin + rect.ymax) / 2
            rect1 = Rect(
                xmin=rect.xmin, ymin=rect.ymin, xmax=middleX, ymax=middleY)
            rect2 = Rect(
                xmin=middleX, ymin=rect.ymin, xmax=rect.xmax, ymax=middleY)
            rect3 = Rect(
                xmin=rect.xmin, ymin=middleY, xmax=middleX, ymax=rect.ymax)
            rect4 = Rect(
                xmin=middleX, ymin=middleY, xmax=rect.xmax, ymax=rect.ymax)
            #使用递归调用
            time.sleep(1)  # 休眠1秒
            self.CutChina(rect=rect1)
            time.sleep(1)  # 休眠1秒
            self.CutChina(rect=rect2)
            time.sleep(1)  # 休眠1秒
            self.CutChina(rect=rect3)
            time.sleep(1)  # 休眠1秒
            self.CutChina(rect=rect4)


if __name__ == "__main__":  #python POISpider.py 71.234018,17.725738,136.139681,55.28893 06
    #避免堆栈溢出
    # sys.setrecursionlimit(1000000)

    POICode = sys.argv[-1]

    # 输入需要的范围
    # RangeArr = sys.argv[-2].split(',')
    # RangeArr = [float(i) for i in RangeArr]

    cut = Cut(POICode)
    #开始先创建矩形存储文件
    fileW = open(cut.filePath, "w")
    fileW.writelines("xmin,ymin,xmax,ymax\n")
    fileW.close()

    rect = Rect(71.234018, 17.725738, 136.139681, 55.28893)
    # rect = Rect(xmin=RangeArr[0], ymin=RangeArr[1]+(RangeArr[3]-RangeArr[1])/2, xmax=RangeArr[2], ymax=RangeArr[3])

    #开始分割中国区域
    cut.CutChina(rect)

    print("程序完成结束")