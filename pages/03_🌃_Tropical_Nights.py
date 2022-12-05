import pandas as pd
import matplotlib.pyplot as plt
from utilities import to_map_df, getmap, areas, years
import time
import streamlit as st
import altair as alt 
import plotly.express as px

# markdown text로 제목 
st.markdown("# 🌃 열대야")
    
    
# 펼쳐지는 페이지 설정 
with st.expander("설명"):
     st.write("""
            열대야일수는 밤최저기온이 25 ℃ 이상인 날로 정의합니다. 기온이 밤에도 25 ℃ 이하로 내려가지 않을 때에는 너무 더워서 사람이 잠들기 어렵기 때문에 더위를 나타내는 지표로 열대야를 사용합니다.
        """)
     st.image("https://t3.ftcdn.net/jpg/02/56/12/92/360_F_256129231_RHUe7uAQGPxUmUnFAtaB5pzYhPNCLCed.jpg")



plt.style.use('ggplot')
rng = (0,25)
with st.sidebar:
    region = st.selectbox("Select the City", areas)


def plot_animation(df):
    lines = alt.Chart(df).mark_line().encode(
       x=alt.X('year', axis=alt.Axis(title='year')),
       y=alt.Y('data',axis=alt.Axis(title='data')),
     ).properties(width=600,height=450)
    return lines

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


with st.container():
    # year slider
    year = st.slider("연도를 선택해 주세요",min(years),max(years), value=max(years))
    temp = gb.get_group(year)
    st.markdown(
        ''':bulb: 아래의 Play 버튼을 눌러 연도별로 변화하는 열대야 일수를 확인할 수 있습니다.''')

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




with st.container():
    st.markdown("""---""")
    st.markdown(
        ''':bulb: 화면 좌측의 탭에서 지역을 선택해 주세요.''')
    df = pd.read_csv('data_tropical/total.csv')
    st.write('### {} 지역의 열대야 통계'.format(region))


    ## region_selectbox
    df = df[df['location'] == region]
    df.drop(['Unnamed: 0'], axis = 1, inplace = True)

 
    # 데이터 정보 요약 표현 가능한 metrics
    tropical_filtered = df[(df['location'] == region)]

    kpi1, kpi2, kpi3, kpi4 = st.columns(4)

    kpi1.metric(
        label=f"현재",
        value="2022년",
    )
    kpi2.metric(
        label=f"열대야 평균 일수",
        value=round(
            tropical_filtered['data'].mean()
            ),
        # delta=round(df_filtered['avg'].mean()) - 10,
    )

    
    lowestyear = tropical_filtered.sort_values(by = 'data', ascending = True)[['year', 'data']].iloc[0,:]


    kpi4.metric(
        label="열대야 일수가 가장 적었던 해 🥶",
        value= lowestyear[0],
        delta= 'num: '+ str(round(lowestyear[1], 1)),
        help = 'Year of lowest number of tropical nights'
    )


    highestyear = tropical_filtered.sort_values(by = 'data', ascending = False)[['year', 'data']].iloc[0,:]

    # st.write(highestyear)

    kpi3.metric(
        label="열대야 일수가 가장 많았던 해🥵",
        value= highestyear[0],
        delta= 'num: '+ str(round(highestyear[1], 1)),
        help = 'Year of highest number of tropical nights'
    )



    ## line_chart 
    with st.container():
        st.markdown("### {} 지역의 연도별 열대야 일수".format(region))
        fig2 = px.line(df, x='year', y='data', color='location')
        fig2.update_layout(yaxis_range=[0,30])

       
 
    
    st.plotly_chart(fig2, use_container_width=True)



