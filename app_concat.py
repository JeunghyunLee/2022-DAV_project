import os
import csv
import time
import json
import folium
import flickrapi

import streamlit as st
import pandas as pd
import altair as alt 
import numpy as np
import matplotlib.pyplot as plt

import xgboost as xgb
import plotly.express as px

from folium.plugins import HeatMap
from folium.features import DivIcon
from streamlit_folium import folium_static, st_folium


#### ------------------------------------
### DATA
def load_data(data_type):
    # get files in the folder
    PATH_DATA = f'./data_{data_type}'
    data_raw = os.listdir(PATH_DATA)
    data_files = sorted([file for file in data_raw if 
                         file.endswith(".csv")])
    district_ls = ['서울경기', '강원영동', '강원영서', '경남', '전남', '전북', '충북', '충남', '제주']
    column_names = ['지역', '연도', '월', '평균열대야일수']
    df_tropicalnight = pd.DataFrame(columns = column_names)

    for file in data_files:
        file_ = pd.read_csv(f'{PATH_DATA}/{file}', 
                            names=column_names, skiprows=[0])
        file_['지역'] = file.split('.')[0]      # specify the district
        df_tropicalnight = pd.concat([df_tropicalnight,file_], axis  = 0)
    return df_tropicalnight

df_tropicalnight = load_data('tropicalnight')




#### ------------------------------------
### STREAMLIT
# First choose which area to display
st.sidebar.markdown("# 지역 선택 📍")
option = st.sidebar.selectbox(
    '아래에서 지역을 선택하세요.',
    ('서울경기', '강원영동', '강원영서', '충북', "충남", "경북", "경남", "전북", "전남", "제주"))

st.sidebar.markdown("# 데이터 선택 📍")
if st.sidebar.checkbox('열대야'):
    st.subheader('평균 열대야 일수')
    st.subheader(f'{option} 지역의 월별 평균 열대야일 수(1973년~2022년)')
    # st.subheader('1973년 ~ 2022년 월별 평균열대야일수')

    # Interactive widgets in Streamlit
    taxi_mode = st.selectbox("월", ("6월", "7월", "8월", "9월"))
    year = st.slider("연도", 1973, 2022)
    st.write(year, "년")

    # Map
    # geodata = json.load(open('stanford-dk009rq9138-geojson.json', 'r',encoding='utf-8'))
    geodata = json.load(open('korea_geojson2.geojson', 'r',encoding='utf-8'))
    map = folium.Map(location=[36,127], zoom_start=7, 
                     scrollWheelZoom = False, 
                     tiles='CartoDB positron')

    # df_tropicalnight_group = df_tropicalnight.groupby(['지역', '연도'])['평균열대야일수'].sum().to_frame().reset_index()
    df_tropicalnight_group = df_tropicalnight.groupby(['지역', '연도']).sum()

    m = folium.Map(location=[35.8, 128.071503], zoom_start=7,)

    ch = px.choropleth(
        # geo_data = geodata,
        # name='choropleth',
        # data = df_tropicalnight,
        # columns=['지역', '평균열대야일수'], 
        df_tropicalnight,
        geojson = geodata, 
        featureidkey="properties.CTP_KOR_NM",
        locations='지역',
        color = '평균열대야일수',
        color_continuous_scale=px.colors.sequential.Redor,
        
        # key_on='feature.properties.CTP_KOR_NM',  
        # fill_color='YlGn',
        # fill_opacity=0.7,
        # line_opacity=1,  
        # line_weight=1.5,
        # line_color='#000',
        # legend_name='시도별 열대야 일수').add_to(m)
    )
    # ch.geojson.add_to(map)
    ch.update_geos(fitbounds='locations',visible=False)
    ch.update_layout(margin={"r":0,"l":0,"t":0,"b":0})
    ch

    st_map = st_folium(map, width=500, height=660)

    # 위도경도 매핑
    locs = {
        '서울경기': (36.7, 127.07), # 인천, 세종 포함
        '경남': (35.19, 129.05), 
        '경북':  (35.8, 129), # 울산, 대구 포함
        '충남': (36.69, 126),
        '전남':  (34.819400, 126.893113),
        '전북':  (35.86, 126.85),
        '강원영서': (37.88, 128),
        '충북': (37.19, 127.50),
        '제주':   (33.62, 126.11),
    }


    for key, value in locs.items():
        folium.map.Marker(
            # 위경도 위치
            [value[0], value[1]],  

            # DivIcon 을 사용
            # html 태그를 이용해서 text를 올릴 수 있음
            icon=DivIcon(
                # icon px 사이즈
                icon_size=(0, 0),
                # icon 좌 상단 위치 설정
                icon_anchor=(0, 0),

                # html 형식으로 text 추가
                # div 태그 안에 style 형식 추가
                html='<div\
                        style="\
                            font-size: 0.8rem;\
                            color: black;\
                            background-color:rgba(255, 255, 255, 0.2);\
                            width:85px;\
                            text-align:center;\
                            margin:0px;\
                        "><b>'
                + key + ': ' + str(df_tropicalnight_group.loc[(key, year), '평균열대야일수'])
                + "<br/><span style='color:red; margin: 0px;'>평균열대야일수: "
                # + str(sido_.loc[(key, '여자'), '인구수']) + '</span>'
                # + "<br/><span style='color: blue; margin: 0px;'>남성: "
                # + str(sido_.loc[(key, '남자'), '인구수']) + '</span>'
                # + '</b></div>',
            )).add_to(m)

    if st.sidebar.checkbox('Show Dataframe'):
        st.subheader('This is my dataset:')
        st.write(df_tropicalnight)


    # Draw a line chart
    line_chart = alt.Chart(df_tropicalnight).mark_line(interpolate='basis').encode(
        alt.X('연도', title='연도'),
        alt.Y('평균열대야일수', title='평균 열대야 일수'),
        color = '월'
    ).properties(
        title = f'{option}'
    )
    # st.altair_chart(line_chart)
    st.write(line_chart)

####
### Rainfall part (just migrated)
if st.sidebar.checkbox('강수량'):
    st.subheader(f'{option} 지역의 연평균 강수량(1973년~2022년)')
    def preprocess(fn):
        df = pd.read_csv(fn)
        df = df.dropna()
        df['date'] = df.date.apply(lambda x: pd.Timestamp(x))
        df['year'] = df.date.apply(lambda x: x.year)
        df['month'] = df.date.apply(lambda x:x.month)
        df['monthday'] = df.month*100 + df.date.apply(lambda x:x.day)
        df['season'] = 4
        df.loc[(df.month>=3)&(df.month<=5),'season'] = 1
        df.loc[(df.month>=6)&(df.month<=8),'season'] = 2
        df.loc[(df.month>=9)&(df.month<=11),'season'] = 3
        return df


    def standardBand(data,range=30,color='blue'):
        fig,ax = plt.subplots()

        standard = data.rolling(range).mean().shift(-1).fillna(method='ffill')
        upper = data.rolling(range).quantile(0.9).shift(-1).fillna(method='ffill')
        lower = data.rolling(range).quantile(0.1).shift(-1).fillna(method='ffill')
        data.plot(color=color,linestyle='dotted')
        standard.plot(color='black')
        ax.fill_between(standard.index,upper,lower,color=color,alpha=0.2)
        return fig,ax


    def animation(animated, namespace,year, years, option):
        for i in range(year,max(years)):
            with animated:
                ax3.clear()
                ax4.clear()
                c1,c2 = st.columns(2)
                with c1:
                    st.text(f'{option} 지역의 일일 강수량(1973년~2022년)')
                    (gb[i].reset_index()[c]).plot(ax=ax3,xlim=[0,370],ylim=[0,250])
                    st.pyplot(fig3)
                with c2:
                    st.text(f'{option} 지역의 월별 강수량(1973년~2022년)')
                    gb[i].groupby('month').sum()[c].plot(ax=ax4,xlim=[0,13],ylim=[0,900])
                    st.pyplot(fig4)
                time.sleep(0.1)
            with namespace:
                st.text(i)


    c = "rainfall"
    years = list(range(1974,2023,1))

    # load data and preprocessing labels
    fn = "data_rain/%s.csv"%option
    df = preprocess(fn)
    gb = dict(list(df.groupby('year')))



    # Yearly sum
    yearlysum=df.groupby('year').sum()[c]
    fig,ax = standardBand(yearlysum)
    st.text(f'{option} 지역의 연 강수량(1973년~2022년)')
    st.pyplot(fig)


    # seasonal analysis
    seasonal = df.groupby(['year','season']).sum()[c]
    c1,c2 = st.columns(2)
    c3,c4 = st.columns(2)
    with c1:
        data = seasonal.loc[:,1]
        fig,ax = standardBand(data,color='green')
        st.text(f'{option} 지역의 봄철 강수량(1973년~2022년)')
        st.pyplot(fig)
    with c2:
        data = seasonal.loc[:,2]
        fig,ax = standardBand(data,color='red')
        st.text(f'{option} 지역의 여름철 강수량(1973년~2022년)')
        st.pyplot(fig)
    with c3:
        data = seasonal.loc[:,3]
        fig,ax = standardBand(data,color='orange')
        st.text(f'{option} 지역의 가을철 강수량(1973년~2022년)')
        st.pyplot(fig)
    with c4:
        data = seasonal.loc[:,4]
        fig,ax = standardBand(data,color='blue')
        st.text(f'{option} 지역의 겨울철 강수량(1973년~2022년)')
        st.pyplot(fig)

    # Animation
    fig3,ax3 = plt.subplots()
    fig4,ax4 = plt.subplots()
    year = st.slider("year",min(years),max(years))
    with st.container():
        animated = st.empty()
        namespace = st.empty()
        with animated:
            ax3.clear()
            ax4.clear()
            c1,c2 = st.columns(2)
            with c1:
                st.text("일일 강수량")
                (gb[year].reset_index()[c]).plot(ax=ax3,xlim=[0,370],ylim=[0,250])
                st.pyplot(fig3)
            with c2:
                st.text("월별 강수량")
                gb[year].groupby('month').sum()[c].plot(ax=ax4,xlim=[0,13],ylim=[0,900])
                st.pyplot(fig4)
        with namespace:
            st.text(year)
        st.button("Play",on_click=animation,args=(animated,namespace,year,years, option))

### Temperature (just migrated)


        
# Progress bar
latest_iteration = st.empty()
bar = st.progress(0)
for i in range(100):
    # Update the progress bar with each iteration.
    latest_iteration.text(f'Iteration {i+1}')
    bar.progress(i + 1)
    time.sleep(0.01)
