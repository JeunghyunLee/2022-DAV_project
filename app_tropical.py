import streamlit as st
import pandas as pd
import altair as alt 
import numpy as np

import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import xgboost as xgb
import time
import plotly.express as px

df = pd.read_csv('total.csv')

## region_selectbox
region_options = df['지역'].unique().tolist()
region = st.selectbox('Which region would you like to see?', region_options, 0)
df = df[df['지역'] == region]
df.drop(['Unnamed: 0'], axis = 1, inplace = True)
df.drop(['Unnamed: 0.1'], axis = 1, inplace = True)

## line_chart animation
lines = alt.Chart(df).mark_line().encode(
    x=alt.X('연도', title='연도'),
    y=alt.Y('연합계', title='연합계'),
    color = '지역'
).properties(
    width=600,
    height=450
)

def plot_animation(df):
    lines = alt.Chart(df).mark_line().encode(
       x=alt.X('연도', axis=alt.Axis(title='연도')),
       y=alt.Y('연합계',axis=alt.Axis(title='연합계')),
     ).properties(
    width=600,
    height=450
)
    return lines


N = df.shape[0] # number of elements in the dataframe
burst = 6       # number of elements (months) to add to the plot
size = burst     # size of the current dataset

line_plot = st.altair_chart(lines)
start_btn = st.button('Start')

if start_btn:
   for i in range(1,N):
      step_df = df.iloc[0:size]
      lines = plot_animation(step_df)
      line_plot = line_plot.altair_chart(lines)
      size = i + burst
      if size >= N: 
         size = N - 1
      time.sleep(0.1)


st.markdown('#')
st.markdown('#')



## region_multiselectbox
df2 = pd.read_csv('total3.csv')
region_options = df2['지역'].unique().tolist()
region = st.multiselect('Which region would you like to see?', region_options, ['강원도'])
df2 = df2[df2['지역'].isin(region)]


# map_animation 
# 지역 선택 -> 연도별 색깔 변화
map = folium.Map(location=[36,127], zoom_start=7, scrollWheelZoom = False, tiles='CartoDB positron')

choropleth = folium.Choropleth(
    geo_data='stanford-dk009rq9138-geojson.json',
    data = df2,
    columns=('지역', '연합계') ,
    key_on='feature.properties.nl_name_1'
)
choropleth.geojson.add_to(map)

st_map = st_folium(map, width=500, height=660)

      
if st.checkbox('Show Dataframe'):
    st.subheader('This is my dataset:')
    st.write(df)