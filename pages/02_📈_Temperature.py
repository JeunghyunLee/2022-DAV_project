import pandas as pd
import time
from utilities import to_map_df, getmap
import matplotlib.pyplot as plt
import time
import streamlit as st
import plotly.express as px
from streamlit_player import st_player


st.set_page_config(
    page_title= 'Temperature', 
    page_icon = ':sunny:',
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        # 'Get Help': 'https://www.extremelycoolapp.com/help',
        # 'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# 2022 winter Data Sciencen and Visualization project. Contributors:  "
    }
)

# Load files
path = 'data_temperature/'
names = ['강원영동', '강원영서', '경남', '경북',
        '서울경기', '전남', '전북', '제주', '충남', '충북']

df = pd.DataFrame()
for name in names :
    temp = pd.read_csv(path +str(name) + '.csv')
    temp['지역'] = name
    df = pd.concat([df, temp], axis = 0)

df = df.dropna()
df['monthday'] = df['date'].apply(lambda x: x[-5:])
df['date'] = df['date'].apply(lambda x: x[1:])
df['date'] = pd.to_datetime(df['date'], format = '%Y-%m-%d')
df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.month
df['day'] = df['date'].dt.day
# df = df[df['year']!= 2022]

# 상단 제목
st.markdown(
        '''### :thermometer: Temperature''')

# 사이드바
with st.sidebar:
    region_filter = st.selectbox("Select the City", pd.unique(df["지역"]))
    # year_region = st.slider(
    #     'Select Year',
    #     1973, 2022, (1980))
    # st.write('Selected Year for regional statistics:', year_region)

st.write('### Geographical Statistics')

@st.cache
def loaddata():
    areas = ['강원영동','강원영서','경남','경북','서울경기','전남','전북','충남','충북','제주']
    res = pd.DataFrame()
    for area in areas:
        df = pd.read_csv(path + "%s.csv"%area)
        df = df.dropna()
        df['date'] = df.date.apply(lambda x: pd.Timestamp(x))
        df['year'] = df.date.apply(lambda x: x.year)
        temp = df.groupby('year').mean()[['avg']]
        temp['location'] = area
        res = pd.concat([res,temp])
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
        mapfig=getmap(mdf, col='avg',rng=(9,20))
        hist.plot(ax = hax, color='black')
        
        with label:
            st.text(year)
            st.write(year)
        with e1:
            c1,c2 = st.columns(2)
            with c1:
                mapfig=getmap(mdf,col='avg',rng=(9,20))
                st.plotly_chart(mapfig, use_container_width = True)
            with c2:
                hist.plot(ax = hax, color='black')
                plt.title("Average Temperature")
                st.pyplot(histfig)
        time.sleep(speed)

with st.container():
    # load all data
    res=loaddata()
    gb = res.groupby('year')
    years = list(res.year.values.astype(int))


    with st.container():
        # year slider
        year = st.slider('Select Year',1973,2022, (2022))
        st.write('Selected Year:', year)
        temp = gb.get_group(year)

        # plot
        label = st.empty()
        e1 = st.empty()
        e2 = st.empty()

        mdf = to_map_df(temp,datacol = ['avg'])
        hist = gb.mean()['avg'].loc[:year]
        

        # 지도 그리기
        histfig,hax = plt.subplots()
        

        with label:
            st.text(year)
        with e1.container():
            c1,c2 = st.columns(2)
            with c1:
                mapfig = getmap(mdf, col='avg',rng=(9,20))
                st.plotly_chart(mapfig, use_container_width = True)
                
            with c2:
                hist.plot(ax = hax,color = 'black')
                plt.title("Average Temperature")
                st.pyplot(histfig)
                
    
        button = st.button("Play",on_click=animation)
        with label:
            st.text(year)
            # year = 2022
        with e1.container():
            c1,c2 = st.columns(2)
            with c1:
                mapfig = getmap(mdf, col='avg',rng=(9,20))
                st.plotly_chart(mapfig, use_container_width = True)
                
            with c2:
                hist.plot(ax = hax,color = 'black')
                plt.title("Average Temperature")
                st.pyplot(histfig)

st.markdown("""---""")
st.write('### Region Statistics _ {}'.format(region_filter))
with st.container():
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)

    # 선택한 지역, 연도 filter
    df_filtered = df[(df['지역'] == region_filter) ]
    df_filtered_cityonly = df[(df['지역'] == region_filter)]

    kpi1.metric(
        label=f"now at",
        value=str(year)+'년',
    )

    kpi2.metric(
        label=f"Summer, Winter average temperature",
        value=str(round(
            df_filtered[df_filtered['month'].isin([12, 1, 2])]
            ['avg'].mean()
            )) + '°C,  ' +  str(round(
            df_filtered[df_filtered['month'].isin([6, 7, 8])]
            ['avg'].mean()
            )) + '°C'
    )


    highestyear = df_filtered_cityonly[(df_filtered_cityonly['month'].isin([6, 7, 8]))].groupby(by = 'year').mean().reset_index()
    highestyear = highestyear.sort_values(by = 'max', ascending = False)[['year', 'max']].iloc[0, :]
    # st.write(highestyear)

    kpi3.metric(
        label="Warmest year 🥵",
        value= int(highestyear[0]),
        # delta= 'goes up to '+ str(round(highestyear[1], 1)),
        help = 'By average of summer max temp'
    )

    lowestyear = df_filtered_cityonly[(df_filtered_cityonly['month'].isin([12, 1, 2]))].groupby(by = 'year').mean().reset_index()
    lowestyear = lowestyear.sort_values(by = 'min', ascending = True)[['year', 'min']].iloc[0,:]

    kpi4.metric(
        label="Coldest year 🥶",
        value= int(lowestyear[0]),
        # delta= 'goes down to' + str(round(lowestyear[1], 1)),
        help = 'By average of winter min temp'
    )

    fig_col3, fig_col4  = st.columns(2)

    densityyear = df_filtered_cityonly.groupby(by = ['year']).mean().reset_index()[['year', 'max']]
    densityyear = densityyear.transpose()
    densityyear.columns = range(1973, 2023)
    # st.write(densityyear)
    densityyear.drop(labels ='year', axis = 0, inplace = True )

    with st.container():
        st.markdown("### Yearly average temperature _ {}".format(region_filter))
        fig_year = px.imshow(densityyear, color_continuous_scale='reds')
        fig_year.update_yaxes(showticklabels=False)
        fig_year.update_layout(
            legend=dict(orientation="h"  ), 
            yaxis_title="Average of Maximum Temperature", 
            margin=dict(l=20, r=20, t=20, b=10)
        
        )

        st.plotly_chart(fig_year,use_container_width = True )
    
    montly, daily  = st.columns(2)
    # create two columns for charts

    

st.markdown("""---""")
st.markdown('#### Related Contents')
st.markdown('''
    If you are interested in learning more informations about climate change in South Korea here are few references that you might want to check out
    * Documents
        * 기상청, 한국 기후변화 평가 보고서 2020 
            * http://www.climate.go.kr/home/cc_data/2020/Korean_Climate_Change_Assessment_Report_2020_2.pdf
        * IPCC Climate Change 2022
            * https://www.ipcc.ch/report/ar6/wg3/downloads/report/IPCC_AR6_WGIII_SPM.pdf
    * Books
        * 이동학, 쓰레기책:왜 지구의 절반은 쓰레기도 뒤덮이는가
        * 김백민, 우리는 결국 지구를 위한 답을 찾을 것이다
        * 박훈, 지속가능한 미래를 위한 기후변화 데이터북 
    ''')
st.markdown("""---""")
fig_col1, fig_col2 = st.columns(2)
with fig_col1 :
    # Embed a youtube video
    st.markdown('##### Netflix: See what three degrees of global warming looks like')
    st_player("https://youtu.be/cTQ3Ko9ZKg8")
    
with fig_col2 : 
    # Embed a youtube video
    st.markdown('##### Economist: See what three degrees of global warming looks like')
    st_player("https://youtu.be/uynhvHZUOOo")

