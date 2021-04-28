#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup

from enum import Enum


class RegionLevel(Enum):
    Province = 1
    City = 2
    County = 3


class SecondType(Enum):
    Summary = 1  # 直辖市所辖市辖区，县的汇总码 [01, 02]
    City = 2  # 市 [01, 20], [51, 70]
    Area = 3  # 地区，自治州，盟 [21, 50]
    DiSummary = 4  # 省（自治区）直辖县级行政区划汇总码 [90]

    @staticmethod
    def GetType(code):
        n = int(code)
        if n == 1 or n == 2:
            return SecondType.Summary
        elif (n > 2 and n <= 20) or (n > 50 and n <= 70):
            return SecondType.City
        elif n > 20 and n <= 50:
            return SecondType.Area
        elif n == 90:
            return SecondType.DiSummary
        else:
            pass


class ThirdType(Enum):
    Summary = 5  # 市辖区汇总码 [01]
    Division = 6  # 市辖区，地区（自治州，盟）辖县级市，市辖特区，省（自治区）直辖县级行政区划中的县级市 [01, 20]
    County = 7  # 县，自治县，旗，自治旗，林区，地区辖特区 [21, 80]
    DirectCounty = 8  # 省（自治区）辖县级市 [81, 99]

    @staticmethod
    def GetType(code):
        n = int(code)
        if n == 1:
            return ThirdType.Summary
        elif n > 1 and n <= 20:
            return ThirdType.Division
        elif n > 20 and n <= 80:
            return ThirdType.County
        elif n > 80 and n <= 99:
            return ThirdType.DirectCounty
        else:
            pass


class Region:
    Code = ''
    Name = ''
    Level = 0
    Parent = None

    def toString(self):
        return ','.join(self.Code, self.Code, self.Level.name + ("" if self.Parent == None else ", Parent: " + self.Parent.Name))

    def __init__(self, code, name, l):
        self.Code = code
        self.Name = name
        self.Level = l

    def __str__(self):
        return self.toString()


if __name__ == "__main__":
    # target = 'http://www.mca.gov.cn/article/sj/xzqh/2020/2020/202101041104.html'
    # data = requests.get(url=target)
    # soup = BeautifulSoup(data.text)

    path = './data/202101041104.html'
    htmlfile = open(path, 'r', encoding='utf-8')
    htmlhandle = htmlfile.read()
    soup = BeautifulSoup(htmlhandle, 'html.parser')

    table = soup.find('table')
    items = table.findAll(name='tr', attrs={'height': '19'})

    curr_province = None
    curr_city = None

    resultList = []

    for i in range(0, len(items)):
        item = items[i]
        codename = item.findAll(name='td', attrs={'class': 'xl7032423'})
        if len(codename) == 0:
            codename = item.findAll(
                name='td', attrs={'class': 'xl7132423'})

        code = codename[0].get_text()
        name = codename[1].get_text()

        firstcode = code[:2]

        secondType = SecondType.GetType(code[2:4])
        thirdType = ThirdType.GetType(code[-2:])

        region = None
        if name.startswith('\xa0\xa0'):
            name = name.lstrip()
            region = Region(code, name, RegionLevel.County)
            region.Parent = curr_city if curr_city != None else curr_province

        elif name.startswith('\xa0'):
            name = name.lstrip()
            region = Region(code, name, RegionLevel.City)
            curr_city = region
            curr_city.Parent = curr_province
        else:
            region = Region(code, name, RegionLevel.Province)
            curr_province = region
            curr_city = None
        seq = (code,
               name,
               (region.Parent.Code if region.Parent != None else ''),
               (region.Parent.Name if region.Parent != None else ''),
               str(region.Level.value),
               str(secondType.value) if secondType != None else '',
               str(thirdType.value) if thirdType != None else '')
        s = ','.join(seq)
        resultList.append(s)

    f = open('data.csv', 'w', encoding='utf-8')
    f.write('id,code,name,p_code,p_name,level,level2_type,level3_type\r')
    id = 0
    for line in resultList:
        id = id + 1
        f.write(str(id)+','+line+'\r')
    f.close()
