import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from utilities import to_map_df
import time, json
import streamlit as st
plt.style.use('ggplot')

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
        hist.loc[year] = mdf['data'].mean()
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

merged_df = pd.read_csv('merged_df.csv')

if __name__ == "__main__":
    # load all data
    res= merged_df
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