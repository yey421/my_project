import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
from flask import Flask, render_template, jsonify, request
import datetime
import re
import json


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}


def get_sokbo():
    url = 'https://news.naver.com/'
    data = requests.get(url, headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')
    results = soup.select('#today_main_news > div.hdline_news > ul > li')
    default = 'news.naver.com/'
    print('헤드라인 뉴스')
    for i in results:
        a_tag = i.select_one('div.hdline_article_tit > a')
        hyper_link = default+a_tag['href']
        if a_tag is not None:
            title = a_tag.text
            title = title.strip()
            print(title)
    result2 = soup.select('#section_politics > div.com_list > div > ul > li')
    print('정치')
    for i in result2:
        a_tag = i.select_one('a > strong')
        if a_tag is not None:
            title = a_tag.text
            title = title.strip()
            print(title)
    result3 = soup.select('#section_economy > div.com_list > div > ul > li')
    print('경제')
    for i in result3:
        a_tag = i.select_one('a > strong')
        if a_tag is not None:
            title = a_tag.text
            title = title.strip()
            print(title)
    result4 = soup.select('#section_society > div.com_list > div > ul > li')
    print('사회')
    for i in result3:
        a_tag = i.select_one('a > strong')
        if a_tag is not None:
            title = a_tag.text
            title = title.strip()
            print(title)
    result3 = soup.select('#section_it > div.com_list > div > ul > li')
    print('IT')
    for i in result3:
        a_tag = i.select_one('a > strong')
        if a_tag is not None:
            title = a_tag.text
            title = title.strip()
            print(title)

def get_num_cor():
    url = 'https://search.naver.com/search.naver?sm=top_hty&fbm=1&ie=utf8&query=코로나+'
    data = requests.get(url, headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')
    num = soup.select('#_cs_production_type > div:nth-child(6) > div.status_info > ul > li.info_01')
    for i in num:
        s = i.text.split(' ')
    return s
    # print('오늘 '+ s[1] + ' : ' + s[-2])



#get_sokbo()
s = get_num_cor()
print(s)