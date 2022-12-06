import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from utilities import to_map_df, getmap, areas, years
import time
import streamlit as st
from sklearn.linear_model import LinearRegression
plt.style.use('ggplot')
rng = (0,25)

@st.cache
def loaddata():
    res = pd.DataFrame()
    for area in areas:
        df = pd.read_csv("data_tropical/%s.csv"%area)
        df = df.dropna()
        df['location']=area
        res = pd.concat([res,df])
    res=res.reset_index()
    return res


def animation(speed = 0.1):
    model=LinearRegression()
    hist = pd.Series()
    histfig,hax = plt.subplots()
    for year,data in gb:
        hax.clear()
        mdf = to_map_df(data,datacol = ['data'])
        hist.loc[year] = mdf.sum()['data']
        x=hist.index.values.reshape(-1,1)
        y=hist.values
        model.fit(x,y)
        a,b = model.coef_,model.intercept_
        # 지도 그리기
        mapfig=getmap(mdf, col='data', rng=rng)
        hist.plot(ax = hax, color='red',title='Yearly Sum')
        hax.plot(x,a*x+b,color='black')
        with label:
            st.text(year)
        with e1:
            c1,c2 = st.columns(2)
            with c1:
                st.plotly_chart(mapfig, use_container_width=True)
            with c2:
                st.pyplot(histfig)
                st.text("기울기: %.2f"%a)
        time.sleep(speed)



# load all data
res= loaddata()
gb = res.groupby('year')
# 상단 제목
st.markdown(
        '''## :night_with_stars: 열대야''')

# 펼쳐지는 페이지 설정
with st.expander("설명"):
     st.write("""
            **열대야일수**는 밤최저기온이 25 ℃ 이상인 날로 정의합니다. 기온이 밤에도 25 ℃ 이하로 내려가지 않을 때에는 너무 더워서 사람이 잠들기 어렵기 때문에 더위를 나타내는 지표로 열대야를 사용합니다.
        """)
     st.image("https://t3.ftcdn.net/jpg/02/56/12/92/360_F_256129231_RHUe7uAQGPxUmUnFAtaB5pzYhPNCLCed.jpg")

with st.container():
    # year slider
    year = st.slider("연도를 선택해 주세요",min(years),max(years), value=max(years))
    temp = gb.get_group(year)

    # plot
    label = st.empty()
    e1 = st.empty()
    e2 = st.empty()

    mdf = to_map_df(temp,datacol=['data'])
    hist = gb.sum()['data'].loc[:year]
    x=hist.index.values.reshape(-1,1)
    y=hist.values
    model=LinearRegression()
    model.fit(x,y)
    a,b = model.coef_,model.intercept_


    # 지도 그리기
    histfig,hax = plt.subplots()
    mapfig = getmap(mdf,col='data', rng=rng)
    hist.plot(ax = hax,color = 'red',title='Yearly Sum')
    hax.plot(x,a*x+b,color='black')

    with label:
        st.text(year)
    with e1:
        c1,c2 = st.columns(2)
        with c1:
            st.plotly_chart(mapfig, use_container_width=True)
        with c2:
            st.pyplot(histfig)
            st.text("기울기: %.2f"%a)

    st.button("Play",on_click=animation)


with st.container():
    st.markdown("""---""")
    s1,s2 = st.columns([1,4])
    with s1:
        region = st.selectbox('',areas, label_visibility='collapsed')
    with s2:
        st.write('### 지역의 열대야 통계')

    df = res[res['location'] == region]
 
    # 데이터 정보 요약 표현 가능한 metrics
    kpi2, kpi3, kpi4 = st.columns(3)
    kpi2.metric(
        label=f"열대야 평균 일수",
        value=round(
            df['data'].mean()
            ),
        # delta=round(df_filtered['avg'].mean()) - 10,
    )

    
    lowestyear = df.sort_values(by = 'data', ascending = True)[['year', 'data']].iloc[0,:]


    kpi3.metric(
        label="가장 적었던 해🥶",
        value= int(lowestyear[0]),
    )

    highestyear = df.sort_values(by = 'data', ascending = False)[['year', 'data']].iloc[0,:]
    kpi4.metric(
        label="가장 많았던 해🥵",
        value= int(highestyear[0]),
    )

    fig2 = px.line(df, x='year', y='data')    
    st.plotly_chart(fig2, use_container_width=True)


