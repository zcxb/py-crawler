#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup

if __name__ == "__main__":
    target = 'https://www.v2ex.com/api/topics/latest.json'
    req = requests.get(url = target)
    print(req.text)