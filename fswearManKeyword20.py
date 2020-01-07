# 네이버쇼핑 베스트 100 남성의류 인기검색어 순위(1~20위)
# 남성의류 인기검색어
# 일간 인기검색어해당 일자 기준 클릭이 발생한 검색어의 클릭량을 반영한 순위

import requests
import bs4
import json
import csv
import pandas as pd
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
    url = "https://search.shopping.naver.com/best100v2/detail/kwd.nhn?catId=" + keywordValue + "&kwdType=KWD"
    html = requests.get(url)
    bs_obj = bs4.BeautifulSoup(html.text, "html.parser")
    return bs_obj

# date 가져오기
def getDate(bs_obj):
    # 날짜
    div_srch_date = bs_obj.find("div", id="calendarDate")
    inputtag_srch_date = div_srch_date.find("input", id="date")
    srch_date = inputtag_srch_date.get("value")
    return srch_date

# 검색어 리스트 가져오기
def getLists(bs_obj):
    popular_brand_area_div = bs_obj.find("div", {"class":"popular_brand_area"})
    popular_srch_lst = popular_brand_area_div.find("ul", {"class":"ranking_list"})
    srch_lists = popular_srch_lst.findAll("li")
    return srch_lists

# json 형식으로 정리하고 폴더를 생성해서 csv파일로 저장
def jsonToCsv(srch_lists, srch_date, keyword):
    # JSON 형식 출력코드
    json_result_lists = [getSrchList(lis) for lis in srch_lists ]
    result_json = json.dumps(json_result_lists, ensure_ascii=False, indent="\t")    

    # JSON 파일로 저장
    #f = open("ManKeyword20.json", 'w', encoding='utf-8')
    #f.write(result_json)
    #f.close()

    # JSON 파일 CSV파일로 저장
    result_dic = json.loads(result_json)
    result_df = pd.DataFrame(result_dic, columns=['순위', '검색어', 'vary'])
    createFolder("./keyword20/" + srch_date + "_keyword20")
    result_df.to_csv("./keyword20/" + srch_date + "_keyword20/" + keyword + 'ManKwd20.csv')

# 20위까지의 순위에서 rank, keyword, vary 추출하는 함수
def getSrchList(li):
    srch_rank = li.find("em").text

    span_srch_keyword = li.find("span", {"class":"txt"})
    atag_srch_keyword = span_srch_keyword.find("a")
    srch_keyword = atag_srch_keyword.get("title")

    span_srch_vary = li.find("span", {"class":"vary"})
    srch_vary = span_srch_vary.text.strip('\n')

    return {"순위":srch_rank, "검색어":srch_keyword, "vary":srch_vary}    

# 각 url catId 딕셔너리
keywords = {"기본" : 50000169, "니트_스웨터" : 50000831, "티셔츠" : 50000830, "셔츠_남방" : 50000833, 
            "카디건" : 50000832, "점퍼" : 50000837, "재킷" : 50000838, "코트" : 50000839,
            "청바지" : 50000835, "바지" : 50000836, "조끼" : 50000834, "정장세트" : 50000840,
            "트레이닝복" : 50000841, "한복" : 50000842, "유니폼_단체복" : 50000843, 
            "레인코트" : 50000844, "코디세트" : 50006328}

for k, v in keywords.items():
    keyword = k
    keywordValue = str(v)

    bs_obj = getBsObject(keywordValue)
    srch_date = getDate(bs_obj)
    srch_lists = getLists(bs_obj)
    jsonToCsv(srch_lists, srch_date, keyword)
    