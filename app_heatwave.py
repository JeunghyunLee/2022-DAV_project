import json
import folium
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
from utilities import to_map_df

merged_df = pd.read_csv('merged_df.csv')

#-----------------------------------------------
st.subheader('전국 평균 폭염 일수')
year = st.slider("연도", 1973, 2022)
st.write(year, "년")

#-----------------------------------------------
# Map
data = json.load(open('korea_geojson2.geojson',encoding='utf-8'))
ids=[]
for x in data['features']:
    id = x['properties']['CTP_KOR_NM']
    x['id'] = id
    ids.append(id)
ids = list(set(ids))

filter_df = merged_df[merged_df['year'] == year]
mdf = to_map_df(filter_df)

# 지도 그리기
map = folium.Map(location=[36,127], zoom_start=7,
                 scrollWheelZoom = False,
                 tiles='CartoDB positron')
fig=px.choropleth_mapbox(mdf,
                         geojson=data,
                         locations='location',
                         color = 'data',
                         mapbox_style='carto-positron',
                         color_continuous_scale=px.colors.sequential.Redor,
                         center = {'lat':35.757981,'lon':127.661132},
                         zoom=5.5,
                         labels='data'
                         )
fig.update_geos(fitbounds='locations',visible=False)
fig.update_layout(margin={"r":0,"l":0,"t":0,"b":0})
st.plotly_chart(fig)

#---------------------------------------------
st.sidebar.markdown("# 지역 선택 📍")
option = st.sidebar.selectbox(
    '아래에서 지역을 선택하세요.',
    ('서울경기', '강원영동', '강원영서', '충북', "충남", "경북", "경남", "전북", "전남", "제주"))

st.sidebar.markdown("# 데이터 선택 📍")
if st.sidebar.checkbox('폭염'):
    st.subheader(f'{option} 지역의 평균 폭염 일수(1973년~2022년)')
    fig = plt.figure(figsize = (35, 15))
    plt.bar(x = range(1973, 2023), height = 'data', data = merged_df[merged_df['location']==option])
    plt.xticks(np.arange(1973, 2023, step=1))
    plt.xlabel('Year', fontsize=18)
    plt.ylabel('Heatwave', fontsize=18)
    # plt.show()
    st.pyplot(fig)
