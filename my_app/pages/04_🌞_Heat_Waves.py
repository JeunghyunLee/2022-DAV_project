
import pandas as pd
import numpy as np
import datetime
import time
from utilities import to_map_df
import matplotlib.pyplot as plt
import time, json, datetime

import streamlit as st
import seaborn as sns
import plotly.express as px
from streamlit_option_menu import option_menu
# pip install streamlit-player
from streamlit_player import st_player

import pydeck as pdk
from urllib.error import URLError

import plotly.figure_factory as ff
import plotly.graph_objects as go

st.set_page_config(
    page_title= 'Korea Climate change Data', 
    page_icon = ':sunny:',
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        # 'Get Help': 'https://www.extremelycoolapp.com/help',
        # 'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# 2022 winter Data Sciencen and Visualization project. Contributors:  "
    }
)


tropical = pd.read_csv('total.csv')

# 가운데 정렬 - 소제목 설정
st.markdown(
        '''
    <h3 style=
    '
    text-align: center;
    color: green;
    font-family:apple;
    ' > Tropical Nights''', unsafe_allow_html=True)

# markdown text로 제목 
st.markdown("# 열대야일수")


# 펼쳐지는 페이지 설정 
with st.expander("See explanation"):
        st.write("""
        열대야일수는 밤최저기온이 25 ℃ 이상인 날로 정의합니다. 기온이 밤에도 25 ℃ 이하로 내려가지 않을 때에는 너무 더워서 사람이 잠들기 어렵기 때문에 더위를 나타내는 지표로 열대야를 사용합니다.
    """)
        st.image("https://t3.ftcdn.net/jpg/02/56/12/92/360_F_256129231_RHUe7uAQGPxUmUnFAtaB5pzYhPNCLCed.jpg")
    
filter1, filter2 = st.columns(2)

# 페이지 내에서 지역 multi select
with filter1 :
        region_filter = st.selectbox(
        "Choose regions", tropical['location'].unique().tolist(), 
    )
        
# 페이지 내에서 year 선택
with filter2 :
    year_slider = st.slider(
            'Select Year',
            1973, 2021, (1980))

# 사이드 바에서 지역 multiselect/year 설택
# with st.sidebar:
#     region_filter = st.selectbox("Select the City", pd.unique(df["지역"]))
#     year_slider = st.slider(
#         'Select Year',
#         1973, 2021, (1980))
#     st.write('Selected Year:', year_slider)


# 데이터 정보 요약 표현 가능한 metrics

st.write('### Region Statistics')
tropical_filtered = tropical[(tropical['location'] == region_filter) & (tropical['year'] == year_slider)]
tropical_filtered_cityonly = tropical[(tropical['location'] == region_filter)]

kpi1, kpi2, kpi3, kpi4 = st.columns(4)

kpi1.metric(
    label=f"You are now at",
    value=region_filter,
)
kpi2.metric(
    label=f"Average number of tropical nights⏳",
    value=round(
        tropical_filtered['data'].mean()
        ),
    # delta=round(df_filtered['avg'].mean()) - 10,
)


lowestyear = tropical_filtered_cityonly.sort_values(by = 'data', ascending = True)[['year', 'data']].iloc[0,:]


kpi3.metric(
    label="Coldest year 🥶",
    value= lowestyear[0],
    delta= 'num: '+ str(round(lowestyear[1], 1)),
    help = 'Year of lowest number of tropical nights'
)


highestyear = tropical_filtered_cityonly.sort_values(by = 'data', ascending = False)[['year', 'data']].iloc[0,:]

# st.write(highestyear)

kpi4.metric(
    label="Warmest year 🥵",
    value= highestyear[0],
    delta= 'num: '+ str(round(highestyear[1], 1)),
    help = 'Year of highest number of tropical nights'
)


# map
st.markdown('#')




@st.cache
def getmap(data,col='data'):
    if False:
        fig=px.choropleth_mapbox(data,
                                geojson=geojson,
                                locations='location',
                                color = col,
                                mapbox_style='carto-positron',
                                color_continuous_scale="Reds",
                                range_color=[0,40],
                                animation_frame='year',

                                center = {'lat':35.757981,'lon':127.661132},
                                zoom=5.5,
                                labels='data'
                                )

    else:
        fig=px.choropleth_mapbox(data,
                                geojson=geojson,
                                locations='location',
                                color = col,
                                mapbox_style='carto-positron',
                                color_continuous_scale="Reds",
                                range_color=[0,40],
                                # animation_frame='year',

                                center = {'lat':35.757981,'lon':127.661132},
                                zoom=5.5,
                                labels='data'
                                )
    fig.update_layout(margin={"r":0,"l":0,"t":0,"b":0})
    return fig

def animation(speed = 0.1):
    hist = pd.Series()
    histfig,hax = plt.subplots()
    for year,data in gb:
        hax.clear()
        mdf = to_map_df(data,datacol = ['data'])
        hist.loc[year] = df[(df['location']=='전국') & (df['year']== year)]['data'].iloc[0]
        # 지도 그리기
        mapfig=getmap(mdf)
        hist.plot(ax = hax, color='black')
        with label:
            st.text(year)
        with e1:
            c1,c2 = st.columns(2)
            with c1:
                st.plotly_chart(mapfig)
            with c2:
                st.pyplot(histfig)

        time.sleep(speed)

df = pd.read_csv('total.csv')

if __name__ == "__main__":
    # load all data
    res= df
    gb = res.groupby('year')
    years = list(res.year.values.astype(int))

    # load geojson
    geojson = json.load(open('korea_geojson2.geojson',encoding='utf-8'))
    ids=[]
    for x in geojson['features']:
        id = x['properties']['CTP_KOR_NM']
        x['id'] = id
        ids.append(id)
    ids = list(set(ids))


    with st.container():
        # year slider
        year = st.slider("year",1973,2022)
        temp = gb.get_group(year)

        # plot
        label = st.empty()
        e1 = st.empty()
        e2 = st.empty()


        #mdf = to_map_df(res.groupby(['year','location']).mean().reset_index(), datacol = ['avg','year'])
        mdf = to_map_df(temp,datacol=['data'])
        hist = gb.sum()['data'].loc[:year]

        # 지도 그리기
        histfig,hax = plt.subplots()
        mapfig = getmap(mdf,col='data')
        hist.plot(ax = hax,color = 'black')

        with label:
            st.text(year)
        with e1:
            c1,c2 = st.columns(2)
            with c1:
                st.plotly_chart(mapfig, use_container_width=True)
            with c2:
                st.pyplot(histfig)
    

        st.button("Play",on_click=animation)