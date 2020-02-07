import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient  # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)

client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbsparta  # 'dbsparta'라는 이름의 db를 만듭니다.

# URL을 읽어서 HTML를 받아오고,
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://comic.naver.com/webtoon/weekday.nhn', headers=headers)

# HTML을 BeautifulSoup이라는 라이브러리를 활용해 검색하기 용이한 상태로 만듦
soup = BeautifulSoup(data.text, 'html.parser')

# select를 이용해서, tr들을 불러오기
webtoons = soup.select('#content > div.list_area.daily_all')

# movies (tr들) 의 반복문을 돌리기
#rank = 1

for week_webtoon in webtoons:
    mon = soup.select('div:nth-child(1)')
    tue = soup.select('div:nth-child(2)')
    wed = soup.select('div:nth-child(3)')
    thr = soup.select('div:nth-child(4)')
    fri = soup.select('div:nth-child(5)')
    sat = soup.select('div:nth-child(6)')
    sun = soup.select('div:nth-child(7)')

    week_data = {
        'mon': mon,
        'tue': tue,
        'wed': wed,
        'thr': thr,
        'fri': fri,
        'sat': sat,
        'sun': sun
    }
#content > div.list_area.daily_all > div:nth-child(1) > div > ul > li:nth-child(1) > a
for day_webtoon in week_data:
    title = day_webtoon.select_one('div > ul > li:nth-child(1) > a')

    db.webtoons.insert_one(title)
    #rank += 1