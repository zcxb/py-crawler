#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod
import requests


class HtmlProvider:
    source = ''

    def __init__(self, source):
        self.source = source

    @abstractmethod
    def GetHtmlText(self):
        pass


class HtmlLocalProvider(HtmlProvider):
    def GetHtmlText(self):
        htmlfile = open(self.source, 'r', encoding='utf-8')
        htmlhandle = htmlfile.read()
        return htmlhandle


class HtmlWebProvider(HtmlProvider):
    def GetHtmlText(self):
        data = requests.get(url=self.source)
        return data.text
