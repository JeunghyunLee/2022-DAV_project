import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
from utilities import to_map_df
import time, json
import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_player import st_player
import pydeck as pdk
from urllib.error import URLError
import plotly.figure_factory as ff
import plotly.graph_objects as go
#--------------------------------------------------
#함수
plt.style.use('ggplot')

def open_df(name) :
    df = pd.read_csv(name + '.csv')

    #아니면 = 0, 폭염 = 1
    conditions = [(df['max'] >= 33), (df['max'] < 33)]
    choices = [1, 0]
    for idx, row in df.iterrows():
        df['temp'] = np.select(conditions, choices)

    year = []
    con_day = []
    num = 1
    for idx, row in df.iloc[1:].iterrows():
        if (df.loc[idx,'temp'] != 0) & (df.loc[idx-1,'temp'] != 0):
            num += 1
        if (df.loc[idx, 'temp'] == 0) & (num != 1):
            year.append(row[0][1:5])
            con_day.append(num)
            num = 1

    df2 = pd.DataFrame({'year':year, 'heatwave':con_day})
    df2 = df2.groupby('year')['heatwave'].sum().reset_index(name ='heatwave')

    h_dict = {}
    year = []
    for e in range(1973, 2023):
        year.append(e)
        h_dict[e] = 0
    for idx, row in df2.iterrows():
        h_dict[int(df2.loc[idx,'year'])] = df2.loc[idx, 'heatwave']

    df3 = pd.DataFrame()
    df3['year'] = h_dict.keys()
    df3['data'] = h_dict.values()
    df3['location'] = name

    return df3

@st.cache
def loaddata():
    location = ['서울경기', '강원영동', '강원영서', '경남', '경북', '전남', '전북', '충북', '충남', '제주']
    merged_df = pd.DataFrame()
    for e in location:
        merged_df = pd.concat([merged_df, open_df(e)], axis = 0)
    # merged_df.to_csv('merged_df.csv', index = False, encoding = 'utf-8-sig')

    return merged_df

#--------------------------------------------------
#함수
def getmap(data,col='data'):
    if 'year' in data.columns:
        fig=px.choropleth_mapbox(data,
                                 geojson=geojson,
                                 locations='location',
                                 color = col,
                                 mapbox_style='carto-positron',
                                 color_continuous_scale=[(0, "blue"), (1, "red")],
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
                                 color_continuous_scale=[(0, "blue"), (1, "red")],
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
        hist.loc[year] = mdf['data'].sum()
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

# merged_df = pd.read_csv('merged_df.csv')

#--------------------------------------------------

# Home을 제외한 Stats 선택시 페이지 최상단에 나오는 제목
st.markdown(
    '''
<h1 style='text-align: center;
color: grey;'
> Heatwave''', unsafe_allow_html=True)
# if __name__ == "__main__":
# load all data
res= loaddata()
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
            st.plotly_chart(mapfig)
        with c2:
            st.pyplot(histfig)

    st.button("Play",on_click=animation)



# markdown text로 제목
st.markdown("# 지역별 폭염 일수 그래프")

#---------------------------------------------
option = st.sidebar.selectbox(
    '아래에서 지역을 선택하세요.',
    ('서울경기', '강원영동', '강원영서', '충북', "충남", "경북", "경남", "전북", "전남", "제주"))

st.subheader(f'{option} 지역의 평균 폭염 일수(1973년~2022년)')
fig = plt.figure(figsize = (35, 15))
plt.bar(x = range(1973, 2023), height = 'data', data = res[res['location']==option])
plt.xticks(np.arange(1973, 2023, step=1))
plt.xlabel('Year', fontsize=18)
plt.ylabel('Heatwave', fontsize=18)
# plt.show()
st.pyplot(fig)