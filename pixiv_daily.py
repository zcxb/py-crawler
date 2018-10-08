#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import re
import urllib3


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
        path_raw = re.findall(self.pattern_url, html)
        return [{
                    'illust_id': re.findall(self.pattern_illust_id, path)[0],
                    'referer': "http://www.pixiv.net/member_illust.php?mode=manga_big&illust_id=" + re.findall(self.pattern_illust_id, path)[0] + "&page=0",
                    'url': path.replace('/c/240x480', '')
                } for path in path_raw]

    def downloadPics(self, list):
        pass

# main
def run():
    spider = PixivDaily()
    html = spider.getHtml(PixivDaily.requestUrl)
    res = spider.fix(html)
    pass


if __name__ == "__main__":
    run()
