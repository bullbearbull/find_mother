import os
import requests
import zipfile
import xml.etree.ElementTree as ET
import pandas as pd
from datetime import datetime

def url_to_df(json_url: str):
    # print(json_url)
    response = requests.get(json_url)
    # print(response.status_code)
    if response.status_code != 200:
        print("Error Occur, When URL Request ")
        return False, None
    else :
        print('Successfully retrieved')
        temp = response.json()
        try :
            temp = pd.DataFrame(temp['list'])  # json에서 list키로 한번 인덱싱하고 DF로 해줘야함
            return True, temp

        except :
            return False, None



# 현재 연, 월, 일 정보 반환

def get_current_yymmdd():
    now_year = datetime.now().year
    now_month = datetime.now().month

    if now_month > 9:  # 10~12월의 직전 분기 3
        prior_q = 3
    elif now_month > 6:  # 7~9월의 직전 분기 2
        prior_q = 2
    elif now_month > 3:  # 이하 상동
        prior_q = 1
    else :
        prior_q = 4
    return now_year, prior_q
