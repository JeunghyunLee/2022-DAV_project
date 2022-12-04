import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import time
from utilities import to_map_df, getmap, areas, years
plt.style.use('ggplot')

st.markdown(
        '''### :umbrella_with_rain_drops: Precipitation Overview''')

with st.sidebar:
    region = st.selectbox("Select the City", areas)

c = "rainfall"
r1=10
r2=10
rng=(500,2000)


@st.cache
def load_rain_data():
    res = pd.DataFrame()
    for area in areas:
        df = pd.read_csv("data_rain/%s.csv"%area)
        df = df.dropna()
        df['date'] = df.date.apply(lambda x: pd.Timestamp(x))
        df['year'] = df.date.apply(lambda x: x.year)
        df['month'] = df.date.apply(lambda x:x.month)
        df['season'] = 4
        df.loc[(df.month>=3)&(df.month<=5),'season'] = 1
        df.loc[(df.month>=6)&(df.month<=8),'season'] = 2
        df.loc[(df.month>=9)&(df.month<=11),'season'] = 3
        df['location'] = area
        res = pd.concat([res,df])
    res=res.reset_index()
    return res



def getStandardBand(data,r1,r2):
    standard = data.rolling(r1).mean().shift(-1).fillna(method='ffill')
    standard = standard[standard.index%10==0]
    standard=standard.reindex(data.index,method='ffill')

    upper = data.rolling(r2).quantile(0.9).shift(-1).fillna(method='ffill')
    lower = data.rolling(r2).quantile(0.1).shift(-1).fillna(method='ffill')
    upper = upper[upper.index%10==0]
    upper=upper.reindex(data.index,method='ffill')
    lower = lower[lower.index%10==0]
    lower=lower.reindex(data.index,method='ffill')

    return standard,upper,lower

def standardBand(data,r1=30,r2=30,color='blue'):
    fig,ax = plt.subplots()
    standard,upper,lower = getStandardBand(data,r1,r2)
    data.plot(color=color,linestyle='dotted')
    standard.plot(color='black')
    ax.fill_between(standard.index,upper,lower,color=color,alpha=0.2)
    return fig,ax


def rain_animation(gb, c, rng, speed=0.1):
    histfig,hax = plt.subplots()
    hist = pd.Series(dtype=float)
    for year,temp in gb:   
        hax.clear()
        mdf = to_map_df(temp,datacol=[c])
        hist.loc[year] = mdf[c].std()
    
        mapfig=getmap(mdf,col=c,rng=rng)
        hist.plot(ax=hax, color='blue')
        with e1:
            st.text(year)
        with e2:
            c1,c2 = st.columns(2)
            with c1:
                st.plotly_chart(mapfig,use_container_width=True)
            with c2:
                st.text("도별 표준편차")
                st.pyplot(histfig)
        time.sleep(speed)


raindata = load_rain_data()

# Animation
aggregate = raindata.groupby(['year','location']).sum()[[c]].reset_index()
histfig,hax = plt.subplots()
gb = aggregate.groupby('year')
with st.container():
    year = st.slider("Select Year",min(years),max(years),value=max(years))
    e1 = st.empty()
    e2 = st.empty()
    temp = gb.get_group(year)    
    mdf = to_map_df(temp, datacol=[c])
    hist = gb.std()[c].loc[:year]
    
    mapfig=getmap(mdf,col=c,rng=rng)
    hist.plot(ax=hax,color='blue')
    with e1:
        st.text(year)
    with e2:
        c1,c2 = st.columns(2)
        with c1:
            st.plotly_chart(mapfig,use_container_width=True)
        with c2:
            st.text("도별 표준편차")
            st.pyplot(histfig)
    st.button("Play",on_click=rain_animation,args=(gb,c,(500,2000)))

st.markdown("""---""")
st.write('### Region Statistics of {}'.format(region))
with st.container():
    # load data and preprocessing labels
    df = raindata[raindata.location==region]
    seasonal = df.groupby(['year','season']).sum()[c].loc[years[1]:years[-1]]
    spring = seasonal.loc[:,1]
    summer = seasonal.loc[:,2]
    fall = seasonal.loc[:,3]
    winter = seasonal.loc[:,4]


    fig,ax = plt.subplots()
    spring.plot(kind='bar',ax=ax,color='green')
    summer.plot(kind='bar',ax=ax,bottom=spring,color='red')
    fall.plot(kind='bar',ax=ax,bottom=spring+summer,color='orange')
    winter.plot(kind='bar',ax=ax,bottom=spring+summer+fall,color='blue')        
    st.pyplot(fig)

    c1,c2 = st.columns(2)
    c3,c4 = st.columns(2)
    with c1:
        fig,ax = standardBand(spring,color='green',r1=r1,r2=r2)
        st.text("봄 강수량")
        st.pyplot(fig)
    with c2:         
        fig,ax = standardBand(summer,color='red',r1=r1,r2=r2)
        st.text("여름 강수량")
        st.pyplot(fig)
    with c3:
        fig,ax = standardBand(fall,color='orange',r1=r1,r2=r2)
        st.text("가을 강수량")
        st.pyplot(fig)
    with c4:    
        fig,ax = standardBand(winter,color='blue',r1=r1,r2=r2)
        st.text("겨울 강수량")
        st.pyplot(fig)
