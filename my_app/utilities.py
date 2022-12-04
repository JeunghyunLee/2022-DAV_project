import pandas as pd
import numpy as np
import time, json, datetime

import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
from streamlit_option_menu import option_menu
# pip install streamlit-player
from streamlit_player import st_player

import pydeck as pdk
from urllib.error import URLError

import plotly.figure_factory as ff
import plotly.graph_objects as go

# plt.style.use('ggplot')
path = 'C:/Users/chaelin/DAVproj/2022-DAV_project-main/2022-DAV_project-main/data_temperature/'
mapping={
    '강원도':['강원도'],
    '강원영동':['강원도'],
    '경남':['경상남도', '울산광역시', '부산광역시'],
    '경북':['경상북도', '대구광역시'],
    '서울경기':['서울특별시', '경기도', '인천특별시'],
    '전남': ['전라남도','광주광역시'],
    '전북': ['전라북도'],
    '제주': ['제주특별자치도'],
    '충남': ['충청남도', '세종특별자치시', '대전광역시'],
    '충북':['충청북도']
}

def loaddata():
    areas = ['강원영동','강원영서','경남','경북',
            '서울경기','전남','전북','충남','충북','제주']
    res = pd.DataFrame()
    for area in areas:
        df = pd.read_csv(path + "%s.csv"%area)
        df = df.dropna()
        df['date'] = df.date.apply(lambda x: pd.Timestamp(x))
        df['year'] = df.date.apply(lambda x: x.year)
        temp = df.groupby('year').mean()[['avg']]
        temp['location'] = area
        res = pd.concat([res,temp])
    res=res.reset_index()
    return res

def getmap(data,col='avg'):
    fig=px.choropleth_mapbox(data,
        geojson=geojson,
        locations='location',
        color = col,
        mapbox_style='carto-positron',
        color_continuous_scale=[(0, "blue"), (1, "red")],
        range_color=[9,20],
        # animation_frame='year',
        center = {'lat':35.757981,'lon':127.661132},
        zoom=5.5,
        labels='data',
        opacity=0.8,
    )
    fig.update_layout(margin={"r":0,"l":0,"t":0,"b":0})
    return fig

def animation(speed = 0.1):
    plt.close()
    hist = pd.Series()
    histfig,hax = plt.subplots()
    for year,temp in gb:
        hax.clear()
        mdf = to_map_df(temp,datacol = 'avg')
        hist.loc[year] = mdf['avg'].mean()
        # 지도 그리기
        mapfig=getmap(mdf)
        hist.plot(ax = hax, color='black')
        with label:
            st.text(year)
        with e1:
            c1,c2 = st.columns(2)
            with c1:
                mapfig=getmap(mdf)
                st.plotly_chart(mapfig, use_container_width = True)
            with c2:
                hist.plot(ax = hax, color='black')
                st.pyplot(histfig)

        time.sleep(speed)


def to_map_df(df,idcol='location',datacol='data'):
    res = pd.DataFrame(columns = [idcol,datacol])
    for i in range(len(df)):
        key,value = df[[idcol,datacol]].iloc[i] 
        if key in mapping:
            for item in mapping[key]:
                res.loc[len(res)] = [item,value]
    return res
