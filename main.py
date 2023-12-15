import os
import requests
import zipfile
import pandas as pd

from util.fss import *
from util.func import *
import argparse
import time


if __name__ == '__main__':
    # 현재 시점에서 가장 최근의
    now_year, prior_q = get_current_yymmdd()


    arg_parser = argparse.ArgumentParser()

    arg_parser.add_argument('--corp_name', type=str)
    arg_parser.add_argument('--bsns_year', type=int, default=now_year)
    arg_parser.add_argument('--bsns_q', type=int, default=prior_q)

    args = arg_parser.parse_args()

    if args.corp_name is None:
        args.corp_name = input('Enter Corp name: ')

    # 결산 보고서를 불러오고
    df = get_highest_share(args.corp_name, args.bsns_year, args.bsns_q)
    # 우선 여기까지 체크
    print(df.iloc[:10, :])

    # 해당 결산 보고서 이후의 지분 거래 공시들을 반영한 정보를 반환
