import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
from utilities import to_map_df, getmap, areas, years
import time
import streamlit as st
plt.style.use('ggplot')
path="data_temperature/"
rng = (0,25)

st.markdown(
        '''## :sun_with_face: 폭염''')

with st.sidebar:
    region = st.selectbox("도시를 선택해주세요", areas)

def open_df(name) :
    df = pd.read_csv(path+name + '.csv')
    print(df.date.iloc[0])
    df['year'] = df['date'].apply(lambda x: pd.Timestamp(x.strip()).year)
    df['data'] = 0
    df.loc[df['max']>=33,'data'] = 1
    df['data'] = df['data'].astype(float)
    res = df.groupby('year').sum()[['data']].reset_index()
    res['location'] = name
    return res


@st.cache
def loaddata():
    merged_df = pd.DataFrame()
    for e in areas:
        merged_df = pd.concat([merged_df, open_df(e)], axis = 0)
    return merged_df



def animation(speed = 0.1):
    hist = pd.Series()
    histfig,hax = plt.subplots()
    for year,data in gb:
        hax.clear()
        mdf = to_map_df(data,datacol = ['data'])
        hist.loc[year] = mdf['data'].sum()
        # 지도 그리기
        mapfig=getmap(mdf,col='data', rng=rng)
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



#--------------------------------------------------


# load all data
res= loaddata()
gb = res.groupby('year')

with st.container():
    # year slider
    year = st.slider("연도를 선택하세요",min(years),max(years),value=max(years))
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
st.write('### {} 지역의 지역별 통계'.format(region))
with st.container():
    st.subheader(f'{region} 지역의 평균 폭염 일수(1973년~2022년)')
    fig=px.bar(res[res.location==region],x='year',y='data')
    st.plotly_chart(fig)
    
