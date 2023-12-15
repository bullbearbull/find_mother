import streamlit as st
import pandas as pd
import numpy as np
from util.func import *
from util.fss import *



@st.cache_data()
def get_df(nm:str):
    now_year, prior_q = get_current_yymmdd()
    corp_df = get_highest_share(nm, now_year, prior_q)

    return corp_df.iloc[:10, 1:]


st.title('지배구조')

corp_name = st.text_input('회사 이름', '삼성전자')
st.write("조회한 회사는", corp_name)


st.subheader(corp_name+"\'s 지배구조")
corp_df = get_df(corp_name)
# corp_df.columns = ['']
st.dataframe(corp_df)