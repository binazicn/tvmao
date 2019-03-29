#!/usr/bin/python
# coding: utf-8

import urllib3
import requests
import datetime
import time
import base64
import ssl
import json
# import http.cookiejar
from bs4 import BeautifulSoup  # 从bs4这个库中导入BeautifulSoup


def is_valid_date(strdate):
    try:
        if ":" in strdate:
            time.strptime(strdate, "%H:%M")
        else:
            return False
        return True
    except:
        return False


def sub_req(a, q, id):
    _keyStr = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=";

    str1 = "|" + q;
    v = base64.b64encode(str1.encode('utf-8'));

    str2 = id + "|" + a;
    w = base64.b64encode(str2.encode('utf-8'));

    str3 = time.strftime("%w");
    wday = (7 if (int(str3) == 0) else int(str3));
    # print(wday);
    F = _keyStr[wday * wday];

    return (F + str(w, 'utf-8') + str(v, 'utf-8'));


def get_program_info(link, sublink, week_day, epg_file_name):
    with open(epg_file_name, "a+") as f:

        str3 = time.strftime("%Y/%m/%d %A",
                             time.localtime(time.time() + (week_day - int(time.strftime("%w"))) * 24 * 3600));
        # str3 = datetime.date.today()+datetime.timedelta(days = (1-int(time.strftime("%w"))))

        f.write(str3)
        f.write("\n\n")

    f.close()

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0',
               'Connection': 'keep-alive', 'Cache-Control': 'no-cache'}
    website = '%s%s' % (link, sublink)
    r = requests.get(website, headers=headers)

    soup = BeautifulSoup(r.text, 'lxml')  # 使用BeautifulSoup解析这段代码
    # 获取节目列表
    list_program_div = soup.find(name='div', attrs={"class": "epg"}).find_all(name='span');
    with open(epg_file_name, "a+") as f:
        for tagprogram in list_program_div:
            # print(tagprogram)
            try:
                if is_valid_date(tagprogram.text):

                    f.write(tagprogram.text)
                    f.write("	")
                else:
                    if tagprogram.text != '正在播出':
                        f.write(tagprogram.text)
                        f.write("\n")

            except:
                continue
    f.close()

    list_first_form = soup.find(name='form');
    sublink = "/api/pg?p=" + sub_req(list_first_form["a"], list_first_form["q"], list_first_form.button["id"]);

    website = '%s%s' % (link, sublink);
    sub_r = requests.get(website);

    soup = BeautifulSoup(sub_r.json()[1], 'lxml')  # 使用BeautifulSoup解析这段代码
    list_program_div = soup.find_all(name='span');

    with open(epg_file_name, "a+") as f:
        for tagprogram in list_program_div:

            try:
                if is_valid_date(tagprogram.text):
                    f.write(tagprogram.text)
                    f.write("	")
                else:
                    if tagprogram.text != '正在播出':
                        f.write(tagprogram.text)
                        f.write("\n")

            except:
                continue
        f.write("\n\n")
    f.close()


def get_program(link, sublink, week_day, epg_file_name):
    get_program_info(link, sublink, week_day, epg_file_name);
