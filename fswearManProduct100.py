# 네이버쇼핑 베스트 100 남성의류 인기상품 순위(1~100위)
# 최근 2일/7일 기준 네이버쇼핑을 통한 판매실적과 상품클릭수를 반영하여 매일 업데이트

# 맥과의 호환을 위해 urllib.request대신 requests를 사용, 속도면에서도 requests가 유리
#import urllib.request
import requests
import bs4
import json
import csv
import pandas as pd
from datetime import datetime
import os

# 폴더 생성
def createFolder(dir):
    try:
        if not os.path.exists(dir):
            os.makedirs(dir)
    except OSError:
        print("Error: Creating directory. " + dir)

# htmlParser
def getBsObject(keywordValue):
    url = "https://search.shopping.naver.com/best100v2/detail/prod.nhn?catId=" + keywordValue
    html = requests.get(url)
    bs_obj = bs4.BeautifulSoup(html.text, "html.parser")
    return bs_obj

# 상품 리스트 가져오기
def getProductLists(bs_obj):
    div_srgoods = bs_obj.find("div", id="productListArea")
    ul_srgoods = div_srgoods.find("ul", {"class":"type_normal"})
    srgoods_lists = ul_srgoods.findAll("li")
    return srgoods_lists

# json 형식으로 정리하고 폴더를 생성해서 csv파일로 저장
def jsonToCsv(goods_lists, keyword, now):
    json_result_lists = [getSrchList(lis) for lis in goods_lists ]
    result_json = json.dumps(json_result_lists, ensure_ascii=False, indent="\t")    

    # JSON 파일로 저장
    #f = open("ManPrd100.json", 'w', encoding='utf-8')
    #f.write(result_json)
    #f.close()

    # JSON 파일 CSV파일로 저장
    result_dic = json.loads(result_json)
    result_df = pd.DataFrame(result_dic, columns=['순위', '상품명', '가격'])
    
    result_df.to_csv("./product100/" + now + "_best100/" + keyword + 'ManPrd100.csv')

# 100위까지의 순위에서 rank, keyword, vary 추출하는 함수
def getSrchList(lis):
    
    # 순위검색코드
    div_rnk = lis.find("div", {"class":"best_rnk"})
    rnk = div_rnk.text.strip('\n')[5:]

    # 상품이름검색코드 - 상품명이 길 경우 생략되는 단어가 생김 밑의 검색코드2로 대체
    #p_prdname = lis.find("p", {"class":"cont"})
    #prdname = p_prdname.find("a").text

    # 상품이름검색코드2 - title 속성으로 값 가져오는 코드
    div_prdname = lis.find("div", {"class":"thumb_area"})
    prdname = div_prdname.find("a").get("title")

    # 상품가격검색코드
    div_price = lis.find("div", {"class":"price"})
    price = div_price.find("strong").text

    return {"순위":rnk, "상품명":prdname, "가격":price}
        
# 각 url catId 딕셔너리
keywords = {"기본" : 50000169, "니트_스웨터" : 50000831, "티셔츠" : 50000830, "셔츠_남방" : 50000833, 
            "카디건" : 50000832, "점퍼" : 50000837, "재킷" : 50000838, "코트" : 50000839,
            "청바지" : 50000835, "바지" : 50000836, "조끼" : 50000834, "정장세트" : 50000840,
            "트레이닝복" : 50000841, "한복" : 50000842, "유니폼_단체복" : 50000843, 
            "레인코트" : 50000844, "코디세트" : 50006328}
#keys = keywords.keys()
#values = keywords.values()

# 날짜
now = datetime.now().strftime("%Y.%m.%d")

# 폴더 생성
createFolder("./product100/" + now + "_best100")

for k, v in keywords.items():
    keyword = k
    keywordValue = str(v)

    bs_obj = getBsObject(keywordValue)
    goods_lists = getProductLists(bs_obj)
    jsonToCsv(goods_lists, keyword, now)
    


