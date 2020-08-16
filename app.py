import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
from flask import Flask, render_template, jsonify, request
import datetime
import re
import json

app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.project

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
# 아래 빈 칸('')을 채워보세요
# http://api.openweathermap.org/data/2.5/weather?q=seoul&appid=8d1ead38edadb80507571247b37862bb
cities = ['Busan', 'Daegu', 'Incheon', 'Gwangju', 'Daejeon', 'Sejong', 'Seoul', 'Ulsan']
apikey = '8d1ead38edadb80507571247b37862bb'

def renew_weather():
    try:
        db.city.drop()
    except:
        pass
    for city in cities:
        url = 'http://api.openweathermap.org/data/2.5/weather?q='+ city +'&appid='+apikey
        data = requests.get(url,headers=headers)
        weather_data = data.json()
        temp = weather_data['main']['temp']
        temp = temp - 273.15
        temp = float('%.1f'% temp)
        x = weather_data['weather'][0]['icon']
        img_addr = "https://openweathermap.org/img/wn/" + x + "@2x.png"
        main = weather_data['weather'][0]['main']
        description = weather_data['weather'][0]['description']
        doc = {
            'city' : city,
            'temp' : temp,
            'img_addr' : img_addr,
            'main' : main,
            'description' : description
        }
        # print(doc)
        db.city.insert_one(doc)

def renew_team():
    try:
        db.team.drop()
    except:
        pass

    url = 'https://sports.news.naver.com/wfootball/record/index.nhn'
    data = requests.get(url, headers=headers)

    html = data.text
    s = re.search(r'var wfootballTeamRecord = (.*);', html, re.S)
    a = s.group(1)

    b = a.split('\n')
    sorted_teamRecord = b[2].strip()
    c = sorted_teamRecord[18:-1]
    d = json.loads(c)
    for i in range(len(d['regularTeamRecordList'])):
        rank = d['regularTeamRecordList'][i]['rank']
        team = d['regularTeamRecordList'][i]['teamName']
        pts = d['regularTeamRecordList'][i]['gainPoint']
        gamecount = d['regularTeamRecordList'][i]['gameCount']
        goalgap = d['regularTeamRecordList'][i]['goalGap']

        doc = {
            'rank' : rank,
            'team' : team,
            'pts' : pts,
            'gamecount' : gamecount,
            'goalgap' : goalgap
        }
        # print(doc)
        db.team.insert_one(doc)

def get_sokbo():
    try:
        db.news.drop()
    except:
        pass
    url = 'https://news.naver.com/'
    data = requests.get(url, headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')
    results = soup.select('#today_main_news > div.hdline_news > ul > li')
    default = 'news.naver.com/'
    for i in results:
        a_tag = i.select_one('div.hdline_article_tit > a')
        hyper_link = default + a_tag['href']
        if a_tag is not None:
            title = a_tag.text
            title = title.strip()
            doc = {
                'headline' : title
            }
            db.news.insert_one(doc)
    # result2 = soup.select('#section_politics > div.com_list > div > ul > li')
    # for i in result2:
    #     a_tag = i.select_one('a > strong')
    #     if a_tag is not None:
    #         title = a_tag.text
    #         title = title.strip()
    #         print(title)
    #         doc = {
    #             'politic news' : title
    #         }
    #         db.news.insert_one(doc)
    # result3 = soup.select('#section_economy > div.com_list > div > ul > li')
    # for i in result3:
    #     a_tag = i.select_one('a > strong')
    #     if a_tag is not None:
    #         title = a_tag.text
    #         title = title.strip()
    #         doc = {
    #             'econ_news' : title
    #         }
    #         db.news.insert_one(doc)
    # result4 = soup.select('#section_society > div.com_list > div > ul > li')
    # print('사회')
    # for i in result3:
    #     a_tag = i.select_one('a > strong')
    #     if a_tag is not None:
    #         title = a_tag.text
    #         title = title.strip()
    #         doc = {
    #             'society_news': title
    #         }
    #         db.news.insert_one(doc)
    # result3 = soup.select('#section_it > div.com_list > div > ul > li')
    # print('IT')
    # for i in result3:
    #     a_tag = i.select_one('a > strong')
    #     if a_tag is not None:
    #         title = a_tag.text
    #         title = title.strip()
    #         doc = {
    #             'IT_news': title
    #         }
    #         db.news.insert_one(doc)

def get_num_cor():
    url = 'https://search.naver.com/search.naver?sm=top_hty&fbm=1&ie=utf8&query=코로나+'
    data = requests.get(url, headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')
    num = soup.select('#_cs_production_type > div:nth-child(6) > div.status_info > ul > li.info_01')
    for i in num:
        s = i.text.split(' ')
    result = '오늘 ' + s[1] + ' : ' + s[-2]
    return num
    # main_content


# HTML 화면 보여주기
@app.route('/')
def home():
    return render_template('index.html')


# API 역할을 하는 부분
@app.route('/api/list', methods=['GET'])
def show_city():
    # 1. db에서 mystar 목록 전체를 검색합니다. ID는 제외하고 like 가 많은 순으로 정렬합니다.
    # 참고) find({},{'_id':False}), sort()를 활용하면 굿!
    city = list(db.city.find({}, {'_id': False}))
    # 2. 성공하면 success 메시지와 함께 stars_list 목록을 클라이언트에 전달합니다.
    return jsonify({'result': 'success', 'city_list': city})

# API 역할을 하는 부분
@app.route('/api/list/direct', methods=['GET'])
def show_city_direct():
    renew_weather()
    city = list(db.city.find({}, {'_id': False}))
    now = datetime.datetime.now()
    renew_time = now.strftime('%m월 %d일 %H시 %M분')
    return jsonify({'result': 'success', 'city_list': city,'renew_time':renew_time})

# API 역할을 하는 부분
@app.route('/api/list/team', methods=['GET'])
def show_team():
    # 1. db에서 mystar 목록 전체를 검색합니다. ID는 제외하고 like 가 많은 순으로 정렬합니다.
    # 참고) find({},{'_id':False}), sort()를 활용하면 굿!
    team = list(db.team.find({}, {'_id': False}))
    # 2. 성공하면 success 메시지와 함께 stars_list 목록을 클라이언트에 전달합니다.
    return jsonify({'result': 'success', 'team_list': team})

# API 역할을 하는 부분
@app.route('/api/list/team/direct', methods=['GET'])
def show_team_direct():
    renew_team()
    team = list(db.team.find({}, {'_id': False}))
    now = datetime.datetime.now()
    renew_time = now.strftime('%m월 %d일 %H시 %M분')
    return jsonify({'result': 'success', 'team_list': team,'renew_time':renew_time})

@app.route('/api/list/news', methods=['GET'])
def show_news():
    get_sokbo()
    news = list(db.news.find({},{'_id': False}))
    num = get_num_cor()
    return jsonify({'result':'success','news_list': news})

@app.route('/api/list/news/direct', methods=['GET'])
def show_news_direct():
    get_sokbo()
    news = list(db.news.find({}, {'_id': False}))
    now = datetime.datetime.now()
    renew_time = now.strftime('%m월 %d일 %H시 %M분')
    num = get_num_cor()
    return jsonify({'result': 'success', 'team_list': news, 'renew_time': renew_time , 'num' : num})
if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)