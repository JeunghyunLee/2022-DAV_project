import pandas as pd
import numpy as np
import datetime
import time

import streamlit as st
import seaborn as sns
import plotly.express as px
from streamlit_option_menu import option_menu
# pip install streamlit-player
from streamlit_player import st_player

import pydeck as pdk
from urllib.error import URLError

import plotly.figure_factory as ff
import plotly.graph_objects as go


st.set_page_config(page_title = 'Korea Climate change Data', 
                   page_icon = ':sunny:',
                   layout ='wide'
                   )

#https://icons.getbootstrap.com/
with st.sidebar:
    selected = option_menu("", ["Home", 'Stats'], 
        icons=['house', 'bar-chart'], menu_icon="cast", default_index=1)
    #selected(returns-> either one of home, story )
with st.sidebar:
    add_topic = st.radio(
        "Choose a topic you are interested",
        ('기온', '열대야', '폭염', '강수량')
    )

# Data Frame
path = 'C:/Users/chaelin/DAVproj/2022-DAV_project-main/2022-DAV_project-main/data_temperature/'
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
df = df[df['year']!= 2022]


# Home 기본 페이지 설정 
if selected == 'Home' :
    st.markdown("## 🎆 story telling ?")
    st.markdown("This page is a Streamlit dashboard that can be used to explore the statistics of climate change in South Korea over the last 50 years.")
    st.markdown("#### General Statistics ♟")
    st.markdown("This gives a general overview of the data including temperature by day, heat wave, and tropical nights.")
    st.markdown("#### Data Sources")
    st.markdown('* 기상청 기상자료개방포털. ')
    st.markdown('* link: https://data.kma.go.kr/stcs/grnd/grndTaList.do?pgmNo=70')

# Home을 제외한 Stats 선택시 페이지 최상단에 나오는 제목 
else :    
    st.markdown(
        '''
    <h1 style='text-align: center;
    color: grey;'
    > Climate Change in South Korea''', unsafe_allow_html=True)


# Stats 선택 & 기온 선택
if (selected != 'Home') & (add_topic == '기온') :
    
    st.markdown(
            '''
        <h3 style='text-align: center;
        color: darkgrey;'
        > Temperature''', unsafe_allow_html=True)

    with st.sidebar:
        region_filter = st.selectbox("Select the City", pd.unique(df["지역"]))
        year_slider = st.slider(
            'Select Year',
            1973, 2021, (1980))
        st.write('Selected Year:', year_slider)

    # with st.spinner("Loading..."):
    #     time.sleep(5)
    # st.success("Done!")

    st.write('### Region Statistics')
    df_filtered = df[(df['지역'] == region_filter) & (df['year'] == year_slider) ]
    df_filtered_cityonly = df[(df['지역'] == region_filter)]

   
    kpi4, kpi1, kpi2, kpi3 = st.columns(4)

    kpi4.metric(
        label=f"You are now at",
        value=region_filter,
    )

    kpi1.metric(
        label=f"Average summer temp of this region on {year_slider} ⏳",
        value=round(
            df_filtered[df_filtered['month'].isin([6, 7, 8])]
            ['avg'].mean()
            ),
        # delta=round(df_filtered['avg'].mean()) - 10,
    )

    lowestyear = df_filtered_cityonly[(df_filtered_cityonly['month'].isin([12, 1, 2]))].groupby(by = 'year').mean().reset_index()
    lowestyear = lowestyear.sort_values(by = 'min', ascending = True)[['year', 'min']].iloc[0,:]

    kpi2.metric(
        label="Coldest year 🥶",
        value= lowestyear[0],
        delta= 'temp: '+ str(round(lowestyear[1], 1)),
        help = 'By average of winter min temp'
    )

    highestyear = df_filtered_cityonly[(df_filtered_cityonly['month'].isin([6, 7, 8]))].groupby(by = 'year').mean().reset_index()
    highestyear = highestyear.sort_values(by = 'max', ascending = False)[['year', 'max']].iloc[0, :]
    # st.write(highestyear)

    kpi3.metric(
        label="Warmest year 🥵",
        value= highestyear[0],
        delta= 'temp: '+ str(round(highestyear[1], 1)),
        help = 'By average of summer max temp'
    )
    
    fig_col3, fig_col4  = st.columns(2)


    densityyear = df_filtered_cityonly.groupby(by = ['year']).mean().reset_index()[['year', 'max']]
    densityyear = densityyear.transpose()
    densityyear.columns = range(1973, 2022)
    # st.write(densityyear)
    densityyear.drop(labels ='year', axis = 0, inplace = True )

    with fig_col3:
        st.markdown("### Yearly Chart(max temp)")
        fig_year = px.imshow(densityyear, color_continuous_scale='reds')
        fig_year.update_yaxes(showticklabels=False)
        fig_year.update_layout(legend=dict(
            orientation="h" 
        ), 
        yaxis_title="Average of Maximum Temperature"
        
        )
        st.plotly_chart(fig_year,use_container_width = True )
    
    montly, daily  = st.columns(2)

    # Montly chart
    with montly :
        groupbymonth = df_filtered_cityonly.groupby(by = ['year', 'month']).mean().reset_index()[['year','month', 'avg']]
        densitymonth = pd.DataFrame(columns = range(1973, 2022))
        for y in range(1, 13):
        #jan
            temp = groupbymonth[groupbymonth['month']== y].transpose()
            temp.columns = range(1973, 2022)
            temp.drop(labels =['year', 'month'], axis = 0, inplace = True )
            temp.index = [y]
            densitymonth = pd.concat([densitymonth, temp])


        # st.write(densitymonth)

        st.markdown("### Montly Chart")
        fig_month = px.imshow(
            densitymonth, 
            color_continuous_scale='RdBu_r'
            )
        fig_month.update_xaxes(side="top")
        fig_month.update_layout(
            yaxis = dict(
                # tickmode = 'linear',
                # tick0 = 1973,
                # dtick = 1
                tickmode = 'array',
                tickvals = list(range(1, 13)),
                ticktext = list(range(1, 13))
            ),
            legend=dict(
                orientation="h" # 가로 방향으로 왜 안됨....
                # yanchor="top", y=0.99, # y축 방향 위치 설정
                # xanchor="left", x=0.01, # x축 방향 위치 설정
            ))

        st.plotly_chart(fig_month)


    with daily:
        # Daily chart 
        daylist = df['monthday'][:365].tolist()

        dfforday = df_filtered_cityonly[['year', 'monthday', 'avg']]
        # summer only
        dfforday = df_filtered_cityonly[df_filtered_cityonly['month'].isin([6, 7, 8])][['year', 'monthday', 'avg']]


        groupbyday = df_filtered_cityonly.groupby(by = ['monthday', 'year']).mean().reset_index()[['monthday', 'year', 'avg']]

        daypivot = groupbyday.pivot('monthday', 'year', 'avg')

        st.markdown("### Daily Chart")
        fig_day = px.imshow(
            daypivot, 
            color_continuous_scale='RdBu_r'
            )
        fig_day.update_xaxes(side="top")
        fig_day.update_layout(
            # yaxis = dict(
            #     # tickmode = 'array',
            #     # tickvals = daylist,
            #     # ticktext = daylist
            # ),
            xaxis = dict(
                tickmode = 'array',
                tickvals = list(range(1973, 2022, 5)),
                ticktext = list(range(1973, 2022, 5))
            ),
            legend=dict(
                orientation="h" # 
                # yanchor="top", y=0.99, # y축 방향 위치 설정
                # xanchor="left", x=0.01, # x축 방향 위치 설정
            ))

        st.plotly_chart(fig_day)


    # create two columns for charts

    fig_col1, fig_col2 = st.columns(2)

    with fig_col1 :
        st.text_area('Related Contents', '''
        * It was the best of times, it was the worst of times, it was
        the age of wisdom, it was the age of foolishness, it was
        the epoch of belief, it was the epoch of incredulity, it
        was the season of Light, it was the season of Darkness, it
        was the spring of hope, it was the winter of despair, (...)
        ''')
        st.markdown("""
        <style>
        .stTextArea [data-baseweb=base-input]{
        background-color: beige ;
        -webkit-text-fill-color: black;
        }
        .stTextArea [data-baseweb=base-input]{
        background-color: beige ;
        -webkit-text-fill-color: black;
        }
        </style>
        """,unsafe_allow_html=True)


    with fig_col2 : 
        # Embed a youtube video
        st_player("https://youtu.be/CmSKVW1v0xMhttps://youtu.be/dIsjcG7hTmo")

# Stats 선택 & 열대야 선택
elif (selected != 'Home') & (add_topic == '열대야'):

    # 가운데 정렬 - 소제목 설정
    st.markdown(
            '''
        <h3 style=
        '
        text-align: left;
        color: green;
        font-family:apple;
        ' > Tropical Nights''', unsafe_allow_html=True)
    
    # markdown text로 제목 
    st.markdown("# Mapping Demo")
    
    filter1, filter2 = st.columns(2)

    # 페이지 내에서 지역 multi select
    with filter1 :
            region_filter = st.multiselect(
            "Choose regions", df['지역'].unique().tolist(), 
        )
    # 페이지 내에서 year 선택
    with filter2 :
        year_slider = st.slider(
                'Select Year',
                1973, 2021, (1980))

    # 사이드 바에서 지역 multiselect/year 설택
    # with st.sidebar:
    #     region_filter = st.selectbox("Select the City", pd.unique(df["지역"]))
    #     year_slider = st.slider(
    #         'Select Year',
    #         1973, 2021, (1980))
    #     st.write('Selected Year:', year_slider)

    # 펼쳐지는 페이지 설정 
    with st.expander("See explanation"):
        st.write("""
            Tropical Night is when ...
        """)
        st.image("https://t3.ftcdn.net/jpg/02/56/12/92/360_F_256129231_RHUe7uAQGPxUmUnFAtaB5pzYhPNCLCed.jpg")

    # 데이터 정보 요약 표현 가능한 metrics

    st.write('### Region Statistics')
    region_filter = region_filter[0]
    df_filtered = df[(df['지역'] == region_filter) & (df['year'] == year_slider) ]
    df_filtered_cityonly = df[(df['지역'] == region_filter)]

    kpi1, kpi2, kpi3, kpi4 = st.columns(4)

    kpi1.metric(
        label=f"You are now at",
        value=region_filter,
    )

    kpi2.metric(
        label=f"Average summer temp of this region on {year_slider} ⏳",
        value=round(
            df_filtered[df_filtered['month'].isin([6, 7, 8])]
            ['avg'].mean()
            ),
        # delta=round(df_filtered['avg'].mean()) - 10,
    )

    lowestyear = df_filtered_cityonly[(df_filtered_cityonly['month'].isin([12, 1, 2]))].groupby(by = 'year').mean().reset_index()
    lowestyear = lowestyear.sort_values(by = 'min', ascending = True)[['year', 'min']].iloc[0,:]

    kpi3.metric(
        label="Coldest year 🥶",
        value= lowestyear[0],
        delta= 'temp: '+ str(round(lowestyear[1], 1)),
        help = 'By average of winter min temp'
    )

    highestyear = df_filtered_cityonly[(df_filtered_cityonly['month'].isin([6, 7, 8]))].groupby(by = 'year').mean().reset_index()
    highestyear = highestyear.sort_values(by = 'max', ascending = False)[['year', 'max']].iloc[0, :]
    # st.write(highestyear)

    kpi4.metric(
        label="Warmest year 🥵",
        value= highestyear[0],
        delta= 'temp: '+ str(round(highestyear[1], 1)),
        help = 'By average of summer max temp'
    )

# Stats 선택 & 폭염 선택
elif (selected != 'Home') & (add_topic == '폭염'):
    # 가운데 정렬 - 소제목 설정
    st.markdown(
            '''
        <h3 style='text-align: center;
        color: darkgreen;'
        > Heat Waves''', unsafe_allow_html=True)
    
    # markdown text로 제목 
    st.markdown("# Mapping Demo")
    
    filter1, filter2 = st.columns(2)

    # 페이지 내에서 지역 multi select
    with filter1 :
            countries = st.multiselect(
            "Choose regions", df['지역'].unique().tolist(), 
        )
    # 페이지 내에서 year 선택
    with filter2 :
        year_slider = st.slider(
                'Select Year',
                1973, 2021, (1980))

    # 사이드 바에서 지역 multiselect/year 설택
    # with st.sidebar:
    #     region_filter = st.selectbox("Select the City", pd.unique(df["지역"]))
    #     year_slider = st.slider(
    #         'Select Year',
    #         1973, 2021, (1980))
    #     st.write('Selected Year:', year_slider)

    # 펼쳐지는 페이지 설정 
    with st.expander("See explanation"):
        st.write("""
            Tropical Night is when ...
        """)
        st.image("https://t3.ftcdn.net/jpg/02/56/12/92/360_F_256129231_RHUe7uAQGPxUmUnFAtaB5pzYhPNCLCed.jpg")

# Stats 선택 & 폭염 선택
elif (selected != 'Home') & (add_topic == '강수량'):
    # 가운데 정렬 - 소제목 설정
    st.markdown(
            '''
        <h3 style='text-align: center;
        color: darkgreen;'
        > Precipitation ''', unsafe_allow_html=True)
    
    # markdown text로 제목 
    st.markdown("# Mapping Demo")
    
    filter1, filter2 = st.columns(2)

    # 페이지 내에서 지역 multi select
    with filter1 :
            countries = st.multiselect(
            "Choose regions", df['지역'].unique().tolist(), 
        )
    # 페이지 내에서 year 선택
    with filter2 :
        year_slider = st.slider(
                'Select Year',
                1973, 2021, (1980))

    # 사이드 바에서 지역 multiselect/year 설택
    # with st.sidebar:
    #     region_filter = st.selectbox("Select the City", pd.unique(df["지역"]))
    #     year_slider = st.slider(
    #         'Select Year',
    #         1973, 2021, (1980))
    #     st.write('Selected Year:', year_slider)

    # 펼쳐지는 페이지 설정 
    with st.expander("See explanation"):
        st.write("""
            Tropical Night is when ...
        """)
        st.image("https://t3.ftcdn.net/jpg/02/56/12/92/360_F_256129231_RHUe7uAQGPxUmUnFAtaB5pzYhPNCLCed.jpg")
    