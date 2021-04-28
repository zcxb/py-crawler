#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import configparser

from bs4 import BeautifulSoup

from HtmlProvider import HtmlLocalProvider, HtmlWebProvider
from Region import *

conf = configparser.ConfigParser()


def getHtmlText():
    htmlProvider = ''
    htmlText = ''

    sourceType = conf.getint('DataSource', 'Type')
    if (sourceType == 1):
        htmlProvider = HtmlLocalProvider(
            conf.get('DataSource', 'LocalTarget'))
        htmlText = htmlProvider.GetHtmlText()
    elif (sourceType == 2):
        htmlProvider = HtmlWebProvider(
            conf.get('DataSource', 'WebTarget'))
        htmlText = htmlProvider.GetHtmlText()

    return htmlText


def selectItems(htmlText):
    soup = soup = BeautifulSoup(htmlText, 'html.parser')
    table = soup.find('table')
    items = table.findAll(name='tr', attrs={'height': '19'})
    return items


def analizeItems(items):
    class1 = conf.get('ItemSelector', 'Class1')
    class2 = conf.get('ItemSelector', 'Class2')

    curr_province = None
    curr_city = None

    resultList = []

    for i in range(0, len(items)):
        item = items[i]
        codename = item.findAll(name='td', attrs={'class': class1})
        if len(codename) == 0:
            codename = item.findAll(
                name='td', attrs={'class': class2})

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

    return resultList


def main():
    conf.read('config.ini')

    htmlText = getHtmlText()
    items = selectItems(htmlText)

    results = analizeItems(items)

    f = open('data.csv', 'w', encoding='utf-8')
    # f.write('id,code,name,p_code,p_name,level,level2_type,level3_type\r')
    id = 0
    for line in results:
        id = id + 1
        f.write(str(id)+','+line+'\r')
    f.close()


if __name__ == "__main__":
    main()
