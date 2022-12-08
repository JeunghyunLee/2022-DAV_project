import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px
import pandas as pd
from sklearn.linear_model import LinearRegression
import time
from utilities import to_map_df, getmap, areas, years
plt.style.use('ggplot')

st.markdown(
        '''## :umbrella_with_rain_drops: 강수량''')
# 펼쳐지는 페이지 설정
with st.expander("설명"):
     st.write("""
            **강수량**의 장기적인 변화 추세로 최근 30년은 과거 30년에 비해, 연 강수량이 135.4㎜ 증가하였고, 강수일수는 21.2일 감소하였습니다. 집중호우와 같은 극한 강수 발생일수도 증가하는 추세에 있습니다. 
        """)

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
        df['season'] = '겨울'
        df.loc[(df.month>=3)&(df.month<=5),'season'] = '봄'
        df.loc[(df.month>=6)&(df.month<=8),'season'] = '여름'
        df.loc[(df.month>=9)&(df.month<=11),'season'] = '가을'
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
    model=LinearRegression()
    histfig,hax = plt.subplots()
    hist = pd.Series(dtype=float)
    for year,temp in gb:   
        hax.clear()
        mdf = to_map_df(temp,datacol=[c])
        hist.loc[year] = mdf[c].var()
        x=hist.index.values.reshape(-1,1)
        y=hist.values
        model.fit(x,y)
        a,b = model.coef_,model.intercept_
    
        mapfig=getmap(mdf,col=c,rng=rng)
        hist.plot(ax=hax, color='blue', title = "Yearly Variance")
        hax.plot(x,a*x+b,color='black')
        with e1:
            st.text(year)
        with e2:
            c1,c2 = st.columns(2)
            with c1:
                st.plotly_chart(mapfig,use_container_width=True)
            with c2:
                st.pyplot(histfig)
                st.text("기울기: %.2f"%a)
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
    hist = gb.var()[c].loc[:year]
    x=hist.index.values.reshape(-1,1)
    y=hist.values
    model=LinearRegression()
    model.fit(x,y)
    a,b = model.coef_,model.intercept_

    mapfig=getmap(mdf,col=c,rng=rng)
    hist.plot(ax=hax,color='blue',title = "Yearly Variance")
    hax.plot(x,a*x+b,color='black')
    with e1:
        st.text(year)
    with e2:
        c1,c2 = st.columns(2)
        with c1:
            st.plotly_chart(mapfig,use_container_width=True)
        with c2:
            st.pyplot(histfig)
            st.text("기울기: %.2f"%a)
    st.button("Play",on_click=rain_animation,args=(gb,c,(500,2000)))


with st.container():
    st.markdown("""---""")
    s1,s2 = st.columns([1,4])
    with s1:
        region = st.selectbox('',areas, label_visibility='collapsed')
    with s2:
        st.write('### 지역의 강수량 통계')

    t1, t2, t3 = st.columns(3)
    t4,t5,t6 = st.columns(3)
    # 선택한 지역, 연도 filter
    temp = raindata[raindata.location==region]
    
    tt = temp[temp.season=='여름'].groupby(['year']).sum()[c].loc[years[1]:]
    summeravg=round(tt.mean())
    maxsummer = tt.idxmax()
    minsummer = tt.idxmin()

    ## 강수일수
    temp['israin'] = temp[c]>0.1

    yearsum = temp.groupby('year').sum()[c].loc[years[1]:]
    avgyear = round(yearsum.mean())
    maxyear = yearsum.idxmax()
    minyear = yearsum.idxmin()
    
    t1.metric(
        label=f"연평균 강수량",
        value=str(avgyear) + 'mm'
        )

    t2.metric(
        label="가장 촉촉한 해",
        value= int(maxyear),
        )

    t3.metric(
        label="가장 건조한 해",
        value= int(minyear)
        )
    t4.metric(label = "여름 평균 강수량",value=str(summeravg)+"mm")
    t5.metric(label="가장 비가 많이 내린 여름", value = int(maxsummer))
    t6.metric(label="가장 비가 덜 내린 여름", value=int(minsummer))


    df = raindata[raindata.location==region]
    seasonal = df.groupby(['year','season']).sum()[c].loc[years[1]:].reset_index()
    ys = yearsum.reset_index()
    ys.columns=['year','total']
    seasonal=seasonal.merge(ys,on='year')
    counts = temp.groupby(['year','season']).sum()['israin'].reset_index()
    counts.columns=['year','season','강수일수']
    print(counts)
    seasonal=seasonal.merge(counts,on=['year','season'])
    seasonal['percent'] = seasonal[c]/seasonal['total']
    seasonal['percent'] = seasonal['percent'].apply(lambda x: round(x,2))
    fig = px.bar(seasonal, x='year', y=c,color='season',category_orders={'season':['봄','여름','가을','겨울']}, hover_data=['percent','강수일수'])
    st.plotly_chart(fig)

