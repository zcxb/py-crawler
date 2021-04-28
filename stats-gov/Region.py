#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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
