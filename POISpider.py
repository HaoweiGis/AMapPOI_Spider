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
            "dc44a8ec8db3f9ac82344f9aa536e678",
            "ebd66ed6c7a36c42511f717170c10068",
        ]
        self.keyNum = 0
        title = open('POIData/title.txt', 'r').read()
        open(self.POIfile, 'w').write(title)

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

    #下载数据
    def DownHtml(self, Range, num=0):
        url = self.Url + Range + "&key=" + self.key[self.keyNum] + "&extensions=all&offset=20&page=" + str(num) + "&types=" + self.POIType
        request = requests.get(url=url, timeout=(5, 27))
        html = request.text
        request.close()
        jsonData = json.loads(html)
        if jsonData['status'] == '1':
            print(url)
        else:
            self.keyNum = self.keyNum + 1
            print(self.keyNum)
            html = self.DownHtml(Range, self.keyNum)
        return html

    def POIWrite(self, Range, count):
        Page = math.ceil(count / 20)
        print(count, Page)
        for num in range(1,Page+1):
            data = self.DownHtml(Range=Range, num=num)
            POIData = json.loads(data).get("pois")
            for POIDict in POIData:
                POIArr = list(POIDict.values())
                POIArr = [str(value).replace(',', '，') for value in POIArr]
                POILine = ','.join(POIArr) + '\n'
                open(self.POIfile, 'a', encoding='utf-8').write(POILine)


if __name__ == "__main__":
    POICode = sys.argv[-1]
    cut = Cut(POICode)
    #开始先创建矩形存储文件
    fileW = open(cut.filePath, "w")
    fileW.writelines("xmin,ymin,xmax,ymax\n")
    fileW.close()
    #开始分割中国区域
    rect = Rect(xmin=71.234018, ymin=17.725738, xmax=136.139681, ymax=55.28893)
    cut.CutChina(rect)

    print("程序完成结束")