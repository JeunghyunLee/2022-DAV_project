import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from utilities import to_map_df, getmap
import time
import streamlit as st
plt.style.use('ggplot')
path="data_temperature/"
rng = (0,25)

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
    location = ['서울경기', '강원영동', '강원영서', '경남', '경북', '전남', '전북', '충북', '충남', '제주']
    merged_df = pd.DataFrame()
    for e in location:
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
                st.plotly_chart(mapfig)
            with c2:
                st.pyplot(histfig)

        time.sleep(speed)



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


with st.container():
    # year slider
    year = st.slider("year",1973,2022,value=2022)
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