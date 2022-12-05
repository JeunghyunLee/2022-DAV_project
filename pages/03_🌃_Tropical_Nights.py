import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from utilities import to_map_df, getmap, areas, years
import time
import streamlit as st
plt.style.use('ggplot')
rng = (0,25)
with st.sidebar:
    region = st.selectbox("도시를 선택해주세요", areas)


def animation(speed = 0.1):
    hist = pd.Series()
    histfig,hax = plt.subplots()
    for year,data in gb:
        hax.clear()
        mdf = to_map_df(data,datacol = ['data'])
        hist.loc[year] = df[(df['location']=='전국') & (df['year']== year)]['data'].iloc[0]
        # 지도 그리기
        mapfig=getmap(mdf, col='data', rng=rng)
        hist.plot(ax = hax, color='black')
        with label:
            st.text(year)
        with e1:
            c1,c2 = st.columns(2)
            with c1:
                st.plotly_chart(mapfig, use_container_width=True)
            with c2:
                st.pyplot(histfig)
        time.sleep(speed)



# load all data
res= pd.read_csv('data_tropical/total.csv')
gb = res.groupby('year')

# 상단 제목
st.markdown(
        '''### :night_with_stars: 열대야''')

with st.container():
    # year slider
    year = st.slider("Select Year",min(years),max(years), value=max(years))
    temp = gb.get_group(year)

    # plot
    label = st.empty()
    e1 = st.empty()
    e2 = st.empty()

    mdf = to_map_df(temp,datacol=['data'])
    hist = gb.sum()['data'].loc[:year]

    # 지도 그리기
    histfig,hax = plt.subplots()
    mapfig = getmap(mdf,col='data', rng=rng)
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



st.markdown("""---""")
st.markdown(
        ''':bulb: 화면 좌측의 탭에서 지역을 선택해 주세요.''')
st.write('### {} 지역의 열대야 통계'.format(region))
with st.container():
    df2 = pd.read_csv('data_tropical/total3.csv')

    ## region_selectbox
    df2 = df2[df2['지역'] == region]
    df2.drop(['Unnamed: 0'], axis = 1, inplace = True)

    ## line_chart animation
    fig2 = px.line(df2, x='연도', y='연합계', color='지역')    
    st.plotly_chart(fig2, use_container_width=True)


