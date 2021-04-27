#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup

from enum import Enum


class RegionType(Enum):
    Province = 1
    City = 2
    County = 3


class Region:
    Code = ''
    Name = ''
    Type = 0
    Parent = None

    def toString(self):
        return self.Name + " [" + self.Code + "] " + self.Type.name + ("" if self.Parent == None else ", Parent: " + self.Parent.Name)

    def __init__(self, code, name, t):
        self.Code = code
        self.Name = name
        self.Type = t

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

        region = None
        if name.startswith('\xa0\xa0'):
            name = name.replace('\xa0\xa0', '')
            region = Region(code, name, RegionType.County)
            region.Parent = curr_city

        elif name.startswith('\xa0'):
            name = name.replace('\xa0', '')
            region = Region(code, name, RegionType.City)
            curr_city = region
            curr_city.Parent = curr_province
        else:
            region = Region(code, name, RegionType.Province)
            curr_province = region
            curr_city = None

        resultList.append(''+region.toString())
        
    f = open('data.csv', 'w', encoding='utf-8')
    for line in resultList:
        f.write(line+'\r')
    f.close()

