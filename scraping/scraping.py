#라이브러리
from bs4 import BeautifulSoup
import requests
import pandas as pd
from pandas import Series, DataFrame
import time
import re

def regexp(reg, val):
    p = re.compile(reg)
    m = p.search(str(val))
    return m
    
#URL 도쿄23구
url = 'https://www.shamaison.com/condition/search/list'
page = 1

#URL리스트
urls = []

#상세 URL리스트
detail_urls = []

address = [] #주소
walking_time = [] #근처역까지 시간
ages = [] #건축일
floor = [] #층
rent = [] #야칭
sep_toilet = [] #화장실 별도
area = [] #면적

#페이지네이션 전부 취득
while True:
    url_page = url + '?selectedPage=' + str(page) + '&image=01&view=2&PRF=13&MOV=0&childSort=0&CTY=13101%2C13102%2C13103%2C13104%2C13105%2C13106%2C13107%2C13108%2C13109%2C13110%2C13111%2C13112%2C13113%2C13114%2C13115%2C13116%2C13117%2C13118%2C13119%2C13120%2C13121%2C13122%2C13123&sort=1'
    page = page+1
    
    #데이터 취득
    result = requests.get(url_page)
    c = result.content
    
    #HTML 기반으로 객체 생성
    soup = BeautifulSoup(c)
    
    #페이지 수 취득
    body = soup.find("a",{'class':'navNotSelectedPage'})
    is_finish = soup.find_all("a",{'class':'navNotSelectedPage navBookend'})
    urls.append(url_page)
    
    if len(is_finish) is 1 and is_finish[0].text == 'Back':
        break


#디테일 주소까지 전부 추출
for url in urls:
    result = requests.get(url)
    c = result.content
    soup = BeautifulSoup(c)
    summary = soup.find_all("table",{'class':'listBoxDetail'})
    for i in range(len(summary)):
        cassetteitems = summary[i].find_all("a", href=True)
        for j in range(len(cassetteitems)):
            if '号室' in cassetteitems[j].text:
                detail_urls.append('https://www.shamaison.com' + cassetteitems[j]['href'])



#각 페이지에 대한 반복문
for url in detail_urls:
    #건물 정보
    result = requests.get(url)
    c = result.content
    soup = BeautifulSoup(c)
    summary = soup.find("div",{'class':'tableBoxA04 mt60'})
    td = summary.find_all("td")
    
    address.append( regexp("東京都(.*)区", td).group(1) if regexp("東京都(.*)区", td) else "기재없음" ) # 주소
    walking_time.append( regexp("徒歩([\d]*)分", td).group(1) if regexp("徒歩([\d]*)分", td) else "기재없음" ) # 역까지 거리
    ages.append( regexp("([\d]*)年", td).group(1) if regexp("([\d]*)年", td) else "기재없음" ) #건축일
    floor.append( regexp("([\d]*)階", td).group(1) if regexp("([\d]*)階", td) else "기재없음" ) #층수
    if regexp("([\d|\,]+)円", td):
        if regexp("([\d|\,]+)円", td).group(1).replace(',',"") != '':
            rent.append( regexp("([\d|\,]+)円", td).group(1).replace(',',"") ) #집세
        else:
            rent.append("기재없음")
    else:
        rent.append("기재없음")
    area.append( round(float(regexp("([\d|.]*)m\<sup", td).group(1))) if regexp("([\d|.]*)m\<sup", td) else "기재없음" ) # 면적
    sep_toilet.append( 1 if regexp("セパレイト", td) else 0 ) # 화장실 별도
   
        

#각 리스트를 시리즈화
address = Series(address)
walking_time = Series(walking_time)
age = Series(ages)
floor = Series(floor)
rent = Series(rent)
sep_toilet = Series(sep_toilet)
area = Series(area)

#각 시리즈를 데이터프레임화
fudou_df = pd.concat([address, walking_time, age, floor, rent, sep_toilet, area], axis=1)

#칼럼명
fudou_df.columns=['住所','徒歩','築年数','階', '賃料', 'トイレ別','専有面積']

#csv파일로 저장
fudou_df.to_csv('house.csv', sep = '\t',encoding='utf-8')   