#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from io import BytesIO

import requests
import urllib3
from PIL import Image


class PixivDaily:

    # request url and params
    requestUrl = 'https://www.pixiv.net/ranking.php'
    param = {'mode': 'daily', 'content': 'illust'}

    # regex patterns
    pattern_url = re.compile(
        r'data-filter="thumbnail-filter lazy-image"data-src="(.+?\.jpg)"data-type')
    pattern_illust_id = re.compile(r'.+/(\d+)_p0', re.S)

    def __init__(self):
        pass

    # get pixiv html text
    def getHtml(self, url):
        response = requests.get(url, self.param)
        print('request url: ' + response.url)
        print('encoding: ' + response.encoding)
        return response.text

    # prepare download params
    def fix(self, html):
        path = re.findall(self.pattern_url, html)
        path_ids = [dict(
                        path = p,
                        id   = re.findall(self.pattern_illust_id, p)[0]
                    ) for p in path]
        return [dict(
                    illust_id  = p['id'],
                    referer    = "http://www.pixiv.net/member_illust.php?mode=manga_big&illust_id=" + p['id'] + "&page=0",
                    short_name = 'illust_id_' + p['id'],
                    url        = p['path'].replace('/c/240x480', '')
                ) for p in path_ids]

    def downloadPics(self, params, local_path):
        for param in params:
            url = param['url']
            referer = {'Referer': param['referer']}
            save_path = local_path + '\\' + param['short_name']
            res = requests.request('get', url, headers=referer)
            img = Image.open(BytesIO(res.content))
            img.save(save_path + '.jpg')
            res.close()


def run(local_path):
    spider = PixivDaily()
    html = spider.getHtml(PixivDaily.requestUrl)
    res = spider.fix(html)
    spider.downloadPics(res, local_path)


if __name__ == "__main__":
    run('E:\\FArtorias\\Pics')
