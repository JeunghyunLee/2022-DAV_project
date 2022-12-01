import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import time
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium


def preprocess(fn):
    df = pd.read_csv(fn)
    df = df.dropna()
    df['date'] = df.date.apply(lambda x: pd.Timestamp(x))
    df['year'] = df.date.apply(lambda x: x.year)
    df['month'] = df.date.apply(lambda x:x.month)
    df['monthday'] = df.month*100 + df.date.apply(lambda x:x.day)
    df['season'] = 4
    df.loc[(df.month>=3)&(df.month<=5),'season'] = 1
    df.loc[(df.month>=6)&(df.month<=8),'season'] = 2
    df.loc[(df.month>=9)&(df.month<=11),'season'] = 3
    return df


def standardBand(data,r1=30,r2=30,color='blue'):
    fig,ax = plt.subplots()
        
    standard = data.rolling(r1).mean().shift(-1).fillna(method='ffill')
    standard = standard[standard.index%10==0]
    standard=standard.reindex(data.index,method='ffill')

    upper = data.rolling(r2).quantile(0.9).shift(-1).fillna(method='ffill')
    lower = data.rolling(r2).quantile(0.1).shift(-1).fillna(method='ffill')
    upper = upper[upper.index%10==0]
    upper=upper.reindex(data.index,method='ffill')
    lower = lower[lower.index%10==0]
    lower=lower.reindex(data.index,method='ffill')
    data.plot(color=color,linestyle='dotted')
    standard.plot(color='black')
    ax.fill_between(standard.index,upper,lower,color=color,alpha=0.2)
    return fig,ax


def animation(animated, namespace,year, years):
    for i in range(year,max(years)):
        with animated:
            ax3.clear()
            ax4.clear()
            c1,c2 = st.columns(2)
            with c1:
                st.text("일일 강수량")
                (gb[i].reset_index()[c]).plot(ax=ax3,xlim=[0,370],ylim=[0,250])
                st.pyplot(fig3)
            with c2:
                st.text("월별 강수량")
                gb[i].groupby('month').sum()[c].plot(ax=ax4,xlim=[0,13],ylim=[0,900])
                st.pyplot(fig4)
            time.sleep(0.1)
        with namespace:
            st.text(i)


c = "rainfall"
years = list(range(1974,2023,1))
menu = ["서울경기","강원영동","강원영서","경남","경북","전남","전북","충남","충북","제주","전국"]
r1=10
r2=10

area = st.selectbox("지역",menu)

# load data and preprocessing labels
fn = "data_rain/%s.csv"%area
df = preprocess(fn)
gb = dict(list(df.groupby('year')))



# Yearly sum
yearlysum=df.groupby('year').sum()[c]
fig,ax = standardBand(yearlysum,r1=r1,r2=r2)
st.text("연 총 강수량")
st.pyplot(fig)


# seasonal analysis
seasonal = df.groupby(['year','season']).sum()[c]
c1,c2 = st.columns(2)
c3,c4 = st.columns(2)
with c1:
    data = seasonal.loc[:,1]
    fig,ax = standardBand(data,color='green',r1=r1,r2=r2)
    st.text("봄 강수량")
    st.pyplot(fig)
with c2:
    data = seasonal.loc[:,2]
    fig,ax = standardBand(data,color='red',r1=r1,r2=r2)
    st.text("여름 강수량")
    ax.cla()
    summer_p = seasonal.loc[:,2] / yearlysum
    ax.plot(summer_p)

    st.pyplot(fig)
with c3:
    data = seasonal.loc[:,3]
    fig,ax = standardBand(data,color='orange',r1=r1,r2=r2)
    st.text("가을 강수량")
    st.pyplot(fig)
with c4:
    data = seasonal.loc[:,4]
    fig,ax = standardBand(data,color='blue',r1=r1,r2=r2)
    winter_p = seasonal.loc[:,4] / yearlysum
    ax.cla()
    ax.plot(winter_p)
    st.text("겨울 강수량")
    st.pyplot(fig)

# Animation
fig3,ax3 = plt.subplots()
fig4,ax4 = plt.subplots()
year = st.slider("year",min(years),max(years))
with st.container():
    animated = st.empty()
    namespace = st.empty()
    with animated:
        ax3.clear()
        ax4.clear()
        c1,c2 = st.columns(2)
        with c1:
            st.text("일일 강수량")
            (gb[year].reset_index()[c]).plot(ax=ax3,xlim=[0,370],ylim=[0,250])
            st.pyplot(fig3)
        with c2:
            st.text("월별 강수량")
            gb[year].groupby('month').sum()[c].plot(ax=ax4,xlim=[0,13],ylim=[0,900])
            st.pyplot(fig4)
    with namespace:
        st.text(year)
    st.button("Play",on_click=animation,args=(animated,namespace,year,years))


