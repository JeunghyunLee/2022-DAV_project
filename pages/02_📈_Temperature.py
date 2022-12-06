import pandas as pd
import time
from utilities import to_map_df, getmap, areas, years
import matplotlib.pyplot as plt
import time
import streamlit as st
import plotly.express as px
rng=(0,20)
path = 'data_temperature/'

st.set_page_config(
    page_title= 'Temperature', 
    page_icon = ':sunny:',
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': "# 2022 winter Data Sciencen and Visualization project. Contributors:  "
    }
)
with st.sidebar:
    region = st.selectbox("Select the City", areas)
    
@st.cache
def loaddata():
    res = pd.DataFrame()
    for area in areas:
        df = pd.read_csv(path + "%s.csv"%area)
        df = df.dropna()
        df['date'] = df.date.apply(lambda x: pd.Timestamp(x))
        df['year'] = df.date.apply(lambda x: x.year)
        df['month'] = df.date.apply(lambda x: x.month)
        df['season'] = '겨울'
        df.loc[(df.month>=3)&(df.month<=5),'season'] = '봄'
        df.loc[(df.month>=6)&(df.month<=8),'season'] = '여름'
        df.loc[(df.month>=9)&(df.month<=11),'season'] = '가을'

        df['location'] = area
        res = pd.concat([res,df])
    res=res.reset_index()
    return res

def animation(speed = 0.01):
    hist = pd.Series()
    histfig,hax = plt.subplots()
    for year,temp in gb:
        hax.clear()
        mdf = to_map_df(temp,datacol = ['avg'])
        hist.loc[year] = mdf['avg'].mean()
        # 지도 그리기
        mapfig=getmap(mdf, col='avg',rng=rng)
        hist.plot(ax = hax, color='black', title="Yearly Average")
        
        with label:
            st.text(year)
            st.write(year)
        with e1:
            c1,c2 = st.columns(2)
            with c1:
                mapfig=getmap(mdf,col='avg',rng=(9,20))
                st.plotly_chart(mapfig, use_container_width = True)
            with c2:
                st.pyplot(histfig)
        time.sleep(speed)



# load all data
df=loaddata()

# 상단 제목
st.markdown(
        '''## :thermometer: 기온''')
with st.container():
    res = df.groupby(['year','location']).mean()[['avg']].reset_index()
    gb = res.groupby('year')
    
    with st.container():
        # year slider
        year = st.slider('연도를 선택해 주세요',min(years),max(years), value=max(years))
        temp = gb.get_group(year)
        # plot
        label = st.empty()
        e1 = st.empty()

        mdf = to_map_df(temp,datacol = ['avg'])
        hist = gb.mean()['avg'].loc[:year]
        
        # 지도 그리기
        histfig,hax = plt.subplots()
        with label:
            st.text(year)
        with e1:
            c1,c2 = st.columns(2)
            with c1:
                mapfig = getmap(mdf, col='avg',rng=rng)
                st.plotly_chart(mapfig, use_container_width = True)
            with c2:
                hist.plot(ax = hax,color = 'black', title = "Yearly Average")
                st.pyplot(histfig)
        button = st.button("Play",on_click=animation)


with st.container():
    st.markdown("""---""")
    st.write('### {} 지역의 기온 통계'.format(region))
    kpi2, kpi3, kpi4 = st.columns(3)

    # 선택한 지역, 연도 filter
    df_filtered = df[(df['location'] == region) ]

    wintermean = df_filtered[df_filtered.season=='겨울']['avg'].mean()
    summermean = df_filtered[df_filtered.season=='여름']['avg'].mean()
    
    kpi2.metric(
        label=f"겨울과 여름 평균 기온",
        value=str(round(wintermean))+'°C, '+str(round(summermean))+'°C'
        )


    summeravg = df_filtered[df_filtered.season=='여름'].groupby('year').mean()
    highestyear = summeravg['max'].idxmax()
    winteravg = df_filtered[df_filtered.season=='겨울'].groupby('year').mean()
    lowestyear = winteravg['min'].idxmin()
    kpi3.metric(
        label="가장 더웠던 해 🥵",
        value= int(highestyear),
        # delta= 'goes up to '+ str(round(highestyear[1], 1)),
        help = 'By average of summer max temp'
    )

    kpi4.metric(
        label="가장 추웠던 해 🥶",
        value= int(lowestyear),
        # delta= 'goes down to' + str(round(lowestyear[1], 1)),
        help = 'By average of winter min temp'
    )


densityyear = df_filtered.groupby(by = ['year']).mean().reset_index()[['year', 'max']]
densityyear = densityyear.transpose()
densityyear.columns = range(1973, 2023)
# st.write(densityyear)
densityyear.drop(labels ='year', axis = 0, inplace = True )

with st.container():
    st.markdown("### {} 지역의 평균 최고기온".format(region))
    fig_year = px.imshow(densityyear, color_continuous_scale='reds')
    fig_year.update_yaxes(showticklabels=False)
    fig_year.update_layout(
        legend=dict(orientation="h"  ), 
        yaxis_title="Average of Maximum Temperature", 
        margin=dict(l=20, r=20, t=20, b=10)
    
    )

    st.plotly_chart(fig_year,use_container_width = True )

