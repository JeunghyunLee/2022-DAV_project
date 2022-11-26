import streamlit as st
import pandas as pd
import altair as alt 
import numpy as np


import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium
import matplotlib.pyplot as plt
import xgboost as xgb
import time

# Add a placeholder 진행 상황 바
latest_iteration = st.empty()
bar = st.progress(0)
for i in range(100):
    # Update the progress bar with each iteration.
    latest_iteration.text(f'Iteration {i+1}')
    bar.progress(i + 1)
    time.sleep(0.01)

st.write('# TropicalNight_seoulgyeonggi')

st.subheader('1973년 ~ 2022년 월별 평균열대야일수')


# load data
df = pd.read_csv('data_tropicalnight/서울경기.csv')
df.drop(columns='Unnamed: 0', inplace = True)
df.insert(0, '지역', 'Gyeonggi-do')
df1 = df[(df['월']=='6월') | (df['월']=='7월') | (df['월']=='8월') | (df['월']=='9월')]
df1

line_chart = alt.Chart(df1).mark_line(interpolate='basis').encode(
    alt.X('연도', title='연도'),
    alt.Y('평균열대야일수', title='평균열대야일수'),
    color = '월'
).properties(
    title = '서울경기'
)

st.altair_chart(line_chart)


# Interactive widgets in Streamlit
taxi_mode = st.selectbox("월", ("6월", "7월", "8월", "9월"))
year = st.slider("연도", 1973, 2022, (1973, 2022))


# 지역을 고르는 select box
option = st.sidebar.selectbox(
    '어떤 지역을 고르시겠습니까?',
    ('서울경기', '강원영동', '강원영서', '충북', "충남", "경북", "경남", "전북", "전남", "제주"))


# 지도 그림

import json
geodata = json.load(open('stanford-dk009rq9138-geojson.json', 'r',encoding='utf-8'))

map = folium.Map(location=[36,127], zoom_start=7, scrollWheelZoom = False, tiles='CartoDB positron')

choropleth = folium.Choropleth(
    geo_data=geodata,
    data = df,
    columns=('지역', '평균열대야일수') ,
    key_on='feature.properties.name_1'
)
choropleth.geojson.add_to(map)

st_map = st_folium(map, width=500, height=660)





if st.checkbox('Show Dataframe'):
    st.subheader('This is my dataset:')
    st.write(df)



