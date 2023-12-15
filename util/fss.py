# Open-DART
import os
import requests
import zipfile
import xml.etree.ElementTree as ET
import pandas as pd
from util.func import *
from util.fss import *


# API KEY 부르기

def get_api_key():
    api_key = '828a7a732e5ae7e09be707dabed363a29445d275'
    return api_key



# 고유 번호 csv 체크 및 저장
def save_corp_code():
    list_dir = os.listdir('./')
    if 'corp_code.csv' in list_dir:  # corp_code.csv가 있는지 확인
        pass
    else:
        corp_code_call_url = 'https://opendart.fss.or.kr/api/corpCode.xml'  # OPEN DART 회사 고유번호
        params = {
            'crtfc_key': get_api_key()  # 발급 필요
        }
        response = requests.get(corp_code_call_url, params=params)

        with open('./id.zip', 'wb') as fp:  # ZIP 파일로 저장
            fp.write(response.content)

        zf = zipfile.ZipFile('./id.zip')
        zf.extractall()  # ZIP 풀기

        xml_path = os.path.abspath('./CORPCODE.xml')

        tree = ET.parse(xml_path)
        root = tree.getroot()
        tags_list = root.findall('list')

        def convert(tag: ET.Element) -> dict:
            conv = {}
            for child in list(tag):
                conv[child.tag] = child.text

            return conv

        tags_list_dict = [convert(x) for x in tags_list]
        df = pd.DataFrame(tags_list_dict)

        df.to_csv('corp_code.csv', index=False)

# 보고서 번호(1, 2, 3, 4 분기)
def get_reprt_code(q_number: int):
    if q_number == 1:
        return '11013'
    elif q_number == 2:
        return '11012'
    elif q_number == 3:
        return '11014'
    elif q_number == 4:
        return '11011'
    else :
        return None


# 법인 고유 번호 불러오기
def get_corp_code(corp_name: str):

    save_corp_code()
    df = pd.read_csv('corp_code.csv')
    if corp_name in df['corp_name'].unique().tolist():
        print('Corp Code Found!')
        temp_return = str(df.loc[df['corp_name'] == corp_name, 'corp_code'].values[0]) #str
        additive_zero = '0' * (8-len(temp_return))
        temp_return = additive_zero + temp_return
        return temp_return #corp_code 반횐, 반환하는 corp_code 값이 문자열이면서, 8자리여야함 따라서, 앞에 숫자 00 붙여야 함
    else :
        return None


def get_highest_share(corp_name: str, bsns_year: int, q_number: int):

    api_key = get_api_key()
    temp_corp_code = get_corp_code(corp_name)
    temp_bsns_year = bsns_year
    temp_reprt_code = get_reprt_code(q_number)

    print('Find the report automatically.')

    # 최대주주등소유주식변동신고
    url = f'https://opendart.fss.or.kr/api/hyslrSttus.json?crtfc_key={api_key}&corp_code={temp_corp_code}&bsns_year={temp_bsns_year}&reprt_code={temp_reprt_code}'
    count = 5
    while not url_to_df(url)[0] : #
        print(f'{corp_name}\'{temp_bsns_year}Q{q_number} report has not yet been')
        if q_number != 1:
            q_number -= 1
        else : #q_number == 1
            q_number = 4
            bsns_year -= 1

        temp_bsns_year = bsns_year
        temp_reprt_code = get_reprt_code(q_number)

        url = f'https://opendart.fss.or.kr/api/hyslrSttus.json?crtfc_key={api_key}&corp_code={temp_corp_code}&bsns_year={temp_bsns_year}&reprt_code={temp_reprt_code}'
        count -= 1
        if count == 0: #최대 4번 조회
            break

    df = url_to_df(url)[1]


    df = df.iloc[:, 3:-1] # 일정한 정보는 제거, 조회 대상 회사명이 제대로 들어간 건지 확인하기 위해 회사 이름은 똑같이 출력되도록 함

    # 기존 주식 수(문자열) 값에 할당된 에 , 값 제거
    for col in df.columns[3:]:
        df[col] = df[col].str.replace(',', '', regex=True)
        

    # 주식수, 지분율 각각 정수, 실수화
    type_dict = {'bsis_posesn_stock_co': 'int', 'bsis_posesn_stock_qota_rt': "float", 'trmend_posesn_stock_co': 'int',
                 'trmend_posesn_stock_qota_rt': 'float'} 
    df = df.astype(type_dict)
    
    # 주식 수 기준으로 내림차순
    df.sort_values(by=['trmend_posesn_stock_co'], ascending=False, inplace=True)
    
    # 1행에 존재하는 합계 행 제거
    # 1. '계'를 인덱싱해서 제거하는 방식으로 접근해야 할 듯
    # 2. 우선주 제거도 고려
    df = df.iloc[1:, :]
    
    # 보기 헷갈리니까 인덱스 리셋
    df.reset_index(drop=True, inplace=True)

    return df


