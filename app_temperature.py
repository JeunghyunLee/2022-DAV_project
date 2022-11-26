import pandas as pd
import numpy as np

import streamlit as st
import seaborn as sns
import plotly.express as px


path = ''
df = pd.read_csv(path + 'temp_data/1121merged_temp.csv')
df = df.iloc[:, 1:]
df.columns = ['date', 'avg', 'min', 'max', 'city_name', 'year', 'month', 'day', 'dailydiff']
df = df.dropna()

st.set_page_config(page_title = 'Korea temperature Data', 
                   page_icon = ':sunny:',
                   layout ='wide'
                   )

# st.title('Temperature by region from 1973 to 2021')
st.markdown(
    '''
<h1 style='text-align: center;
 color: darkred;'
 >Temperature by region <br> : from 1973 to 2021</h1>''', unsafe_allow_html=True)

# Raw data checkbos
st.write('#### Select the checkbox below to see raw data set')
if st.checkbox('Show raw data'):
    st.subheader('Temperature from 1973 to 2021')
    st.write(df)




st.write('#### Filter1: City')
# top level filter
region_filter = st.selectbox("Select the City", pd.unique(df["city_name"]))

st.write('#### Filter2: Year ')
year_slider = st.slider(
    'Select Year',
    1973, 2021, (1980))
st.write('Selected Year:', year_slider)

st.write('### Montly Temperature')
df_filtered = df[(df['city_name'] == region_filter) & (df['year'] == year_slider) ]
df_filtered_cityonly = df[(df['city_name'] == region_filter)]

# KPI title 
# create three columns
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

# create two columns for charts

fig_col1, fig_col2 = st.columns(2)

with fig_col1:
    st.markdown("### Min temp Chart by year")
    st.bar_chart(
        data = df_filtered.groupby(by = ['year', 'month']).mean().reset_index(), 
        x = 'month', 
        y = 'min' 
        )

with fig_col2:
    st.markdown("### Max temp Chart by year")
    # fig2 = px.bar_chart(data_frame=df_filtered[['year', 'max']], x="year")
    # st.write(fig2)
    # chart_data = df_filtered[['year', 'max']]
    st.bar_chart(
        data = df_filtered.groupby(by = ['year', 'month']).mean().reset_index(), 
        x = 'month', 
        y = 'max' 
        )

fig_col3, fig_col4  = st.columns(2)


densityyear = df_filtered_cityonly.groupby(by = ['year']).mean().reset_index()[['year', 'avg']]
densityyear = densityyear.transpose()
densityyear.columns = range(1973, 2022)
# st.write(densityyear)
densityyear.drop(labels ='year', axis = 0, inplace = True )

with fig_col3:
    st.markdown("### Yearly Chart(average temp)")
    fig = px.imshow(densityyear, color_continuous_scale='sunsetdark')
    fig.update_yaxes(showticklabels=False)
    fig.update_layout(
    yaxis_title="Average Temperature")

    st.plotly_chart(fig)

densityyear = df_filtered_cityonly.groupby(by = ['year']).mean().reset_index()[['year', 'max']]
densityyear = densityyear.transpose()
densityyear.columns = range(1973, 2022)
# st.write(densityyear)
densityyear.drop(labels ='year', axis = 0, inplace = True )

with fig_col4:
    st.markdown("### Yearly Chart(max temp)")
    fig = px.imshow(densityyear, color_continuous_scale='reds')
    fig.update_yaxes(showticklabels=False)
    fig.update_layout(legend=dict(
        orientation="h" # 가로 방향으로 왜 안됨....
    ), 
    yaxis_title="Average of Maximum Temperature"
    
    )
    st.plotly_chart(fig)



groupbymonth = df_filtered_cityonly.groupby(by = ['year', 'month']).mean().reset_index()[['year','month', 'avg']]
densitymonth = pd.DataFrame(columns = range(1973, 2022))
for y in range(1, 13):
#jan
    temp = groupbymonth[groupbymonth['month']== y].transpose()
    temp.columns = range(1973, 2022)
    temp.drop(labels =['year', 'month'], axis = 0, inplace = True )
    temp.index = [y]
    densitymonth = pd.concat([densitymonth, temp])
    
st.markdown("### Montly Chart")
fig = px.imshow(
    densitymonth, 
    color_continuous_scale='RdBu_r'
    )
fig.update_xaxes(side="top")
fig.update_layout(
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

st.plotly_chart(fig)



# view = [100, 50, 30]
# view
# st.write('Youtube view')
# st.bar_chart(view)

# st.write('''
# # Title1
# ## Title 2
# ### Title''')
# st.write('whereever?')

# sview = pd.Series(view)
# sview

### file loading


# splot = sns.scatterplot(data = df[df['year']==1973], x = 'month', y = 'max' )
# splot

# df


# #---sidebar
# st.sidebar.header('Please filter Here:')
# Year = st.sidebar.multiselect(
#     "Select the Year:",
#     options = df['year'].unique(), 
#     default = 2021
# )

    
# #---sidebar
# st.sidebar.header('Please filter Here:')
# Month = st.sidebar.multiselect(
#     "Select the month:",
#     options = df['month'].unique(), 
#     default = df['month'].unique()
# )

# df_selection = df.query(
#     ("city_name == @Cityname") and ("year == @Year") and ("month = @Month")
#     )

# st.dataframe(df_selection)


# #---sidebar
# st.sidebar.header('Please filter Here:')
# Cityname = st.sidebar.multiselect(
#     "Select the region:",
#     options = df['city_name'].unique(), 
#     default = "seoulgyeonggi" )

header1 = st.subheader('최고 기온 35도 이상 ')
# option = st.selectbox(
#     'Select region', 
#     (df['city_name'].unique()), key = 1)

region_data = df_filtered_cityonly[df_filtered_cityonly['max']>35]
# region_data = region_data.loc[(region_data['city_name'] == region_filter)]
region_data = region_data[['date', 'max']]

# s_index = region_data[['city_name']]
# region_data = region_data[['date', 'max']].transpose()
# region_data.columns = region_data.iloc[:, 0]
# region_data.drop(labels = [''])
# region_data = region_data.rename(columns=region_data.iloc[0])
# region_data.drop(['date'], axis = 0)

st.bar_chart(data = region_data, x = 'date', y = 'max', use_container_width=True)

#_____________ try 1_________________________________________

# 그해 여름의 평균 기온, 33/35도 이상인 날들 카운트


temp_level = 35

import matplotlib.pyplot as plt

sum_avg = df[df['month'].isin([6, 7, 8])].groupby(by = ['city_name', 'year']).mean()[['max']].reset_index()
cnt_hot = df[(df['month'].isin([6, 7, 8])&(df['max']>=temp_level))].groupby(by = ['city_name', 'year']).count()[['max']].reset_index()
sum_merged = sum_avg.merge(cnt_hot, how = 'left', on = ['city_name', 'year'], suffixes=('_avg', '_cnt'))
sum_merged = sum_merged.fillna(0)

# plt.figure(figsize=(20, 10))

# fig, ax = plt.subplots()
# ax.plot(tempd['year'], tempd['max_avg'], c = 'black')
# ax.scatter(tempd['year'], tempd['max_avg'], c=tempd['max_cnt'], 
#             s=tempd['max_cnt']**2.1 ,cmap=plt.cm.Reds)
# ax.set_ylim(26, 32)

# st.pyplot(fig)


# import chart_studio
# chart_studio.tools.set_credentials_file(username='username', api_key='api_key')

#------------ 지역별 여름 평균 기온 및 폭염
st.subheader('지역별 여름 평균 기온 35도 이상 폭염')
# option = st.selectbox(
#     'Select region', 
#     (df['city_name'].unique()), key = 2)

import plotly.figure_factory as ff
# import chart_studio.plotly as py
import plotly.express as px
import plotly.graph_objects as go
# import plotly.subplots import make_subplots

tempd = sum_merged[sum_merged['city_name']==region_filter]
size = tempd['max_cnt']
fig = go.Figure(data = [go.Scatter(x=tempd['year'], y=tempd['max_avg'], 
    mode = 'lines+markers+text',
    opacity = 1,
    line = {'color':'black', 
            'width':1,
            'dash':'dash'},
    text = tempd['max_cnt'],
    marker = dict (
        size = size ,
        sizemode = 'area',
        sizeref = 2.*max(size)/(40.**2), 
        sizemin = 4,
        color=tempd['max_cnt'],
        # line=dict(color="#ffe476"), 
        colorscale='bluered'
        
    )
)])

# fig.add_trace(go.Line(x = tempd['year'], y = tempd['max_avg']))

fig.update_layout(showlegend=False,
                         height=200,
                         margin={'l': 10, 'r': 10, 't': 0, 'b': 0})
# fig = px.scatter(x = tempd['year'], y = tempd['max_avg'], 
#     mode = 'markers+text', mode = [trace]))
    #  color=tempd['max_cnt'], size = tempd['max_cnt']**2.1, color_continuous_scale='redor'
    #  )))

# fig = fig.add_trace(
#     go.Line(tempd, x = 'year', y = 'max_avg'))

st.plotly_chart(fig)


#---------------------try 2---------------------------------------#

temp_level = 3

import matplotlib.pyplot as plt

sum_avg = df.groupby(by = ['city_name', 'year']).mean()[['dailydiff']].reset_index()

cnt_hot = df[(df['dailydiff']<=temp_level)].groupby(by = ['city_name', 'year']).count()[['dailydiff']].reset_index()

sum_merged = sum_avg.merge(cnt_hot, how = 'left', on = ['city_name', 'year'], suffixes=('_avg', '_cnt'))

sum_merged = sum_merged.fillna(0)

# plt.figure(figsize=(20, 10))

# fig, ax = plt.subplots()
# ax.plot(tempd['year'], tempd['dailydiff_avg'], c = 'black')
# ax.scatter(tempd['year'], tempd['dailydiff_avg'], c=tempd['dailydiff_cnt'], 
#             s=tempd['dailydiff_cnt']**2.1 ,cmap=plt.cm.Reds)
# ax.set_ylim(26, 32)

# st.pyplot(fig)


# import chart_studio
# chart_studio.tools.set_credentials_file(username='username', api_key='api_key')

#------------ 지역별 여름 평균 기온 및 폭염
st.subheader('일교차 '+str(temp_level)+'도 이하')
# option = st.selectbox(
#     'Select region', 
#     (df['city_name'].unique()), key = 3)

import plotly.figure_factory as ff
# import chart_studio.plotly as py
import plotly.express as px
import plotly.graph_objects as go
# import plotly.subplots import make_subplots

tempd = sum_merged[sum_merged['city_name']==region_filter]
size = tempd['dailydiff_cnt']
fig = go.Figure(data = [go.Scatter(x=tempd['year'], y=tempd['dailydiff_avg'], 
    mode = 'lines+markers+text',
    opacity = 1,
    line = {'color':'black', 
            'width':1,
            'dash':'dash'},
    text = tempd['dailydiff_cnt'],
    marker = dict (
        size = size ,
        sizemode = 'area',
        sizeref = 2.*max(size)/(40.**2), 
        sizemin = 4,
        color=tempd['dailydiff_cnt'],
        # line=dict(color="#ffe476"), 
        colorscale='bluered'
        
    )
)])

# fig.add_trace(go.Line(x = tempd['year'], y = tempd['dailydiff_avg']))

fig.update_layout(showlegend=False,
                         height=200,
                         margin={'l': 10, 'r': 10, 't': 0, 'b': 0})
st.plotly_chart(fig)


#---------------------try 3---------------------------------------#

temp_level = -15

import matplotlib.pyplot as plt

sum_avg = df[df['month'].isin([12, 1, 2])].groupby(by = ['city_name', 'year']).mean()[['min']].reset_index()

cnt_hot = df[(df['month'].isin([12, 1, 2])&(df['min']<=temp_level))].groupby(by = ['city_name', 'year']).count()[['min']].reset_index()

sum_merged = sum_avg.merge(cnt_hot, how = 'left', on = ['city_name', 'year'], suffixes=('_avg', '_cnt'))

sum_merged = sum_merged.fillna(0)

st.subheader('겨울철 최저 '+str(temp_level)+'도 이하')
# option = st.selectbox(
#     'Select region', 
#     (df['city_name'].unique()), key = 4)

import plotly.figure_factory as ff
import plotly.express as px
import plotly.graph_objects as go

tempd = sum_merged[sum_merged['city_name']==region_filter]

size = tempd['min_cnt']
fig = go.Figure(data = [go.Scatter(x=tempd['year'], y=tempd['min_avg'], 
    mode = 'lines+markers+text',
    opacity = 1,
    line = {'color':'black', 
            'width':1,
            'dash':'dash'},
    text = tempd['min_cnt'],
    marker = dict (
        size = size ,
        sizemode = 'area',
        sizeref = 2.*max(size)/(40.**2), 
        sizemin = 1,
        color=tempd['min_cnt'],
        # line=dict(color="#ffe476"), 
        colorscale='rdbu'
        
    )
)])

fig.update_layout(showlegend=False,
                         height=200,
                         margin={'l': 10, 'r': 10, 't': 0, 'b': 0})
st.plotly_chart(fig)


#_----------------------------------------------------------#
#interactive st.altair_chart

st.subheader('지역별 1일의 최고 기온')

import altair as alt
from datetime import datetime, date

df_inter = df.drop_duplicates(subset = ['city_name', 'year', 'month'], keep = 'first')
df_inter = df_inter[df_inter['city_name'].isin(['chungbuk', 'chungnam'])]
df_inter['date'] = pd.to_datetime(df_inter['date'])

def get_chart(data):
    hover = alt.selection_single(
        fields=["date"],
        nearest=True,
        on="mouseover",
        empty="none",
    )

    lines = (
        alt.Chart(data, title="Changes in max temperature(1st)")
        .mark_line()
        .encode(
            x="date",
            y="max",
            color="city_name",
        )
    )

    # Draw points on the line, and highlight based on selection
    # if mouseover -> draw a circle on point
    points = lines.transform_filter(hover).mark_circle(size=65)

    # Draw a rule at the location of the selection
    tooltips = (
        alt.Chart(data)
        .mark_rule()
        .encode(
            x="yearmonthdate(date)",
            y="max",
            opacity=alt.condition(hover, alt.value(0.3), alt.value(0)),
            tooltip=[
                alt.Tooltip("date", title="Date"),
                alt.Tooltip("max", title="Max(°C)"),
            ],
        )
        .add_selection(hover)
    )
    return (lines + points + tooltips).interactive()

chart = get_chart(df_inter)

# Add annotations arrow if needed
# ANNOTATIONS = [
#     ("Mar 01, 2008", "Pretty good day for GOOG"),
#     ("Dec 01, 2007", "Something's going wrong for GOOG & AAPL"),
#     ("Nov 01, 2008", "Market starts again thanks to..."),
#     ("Dec 01, 2009", "Small crash for GOOG after..."),
# ]
# annotations_df = pd.DataFrame(ANNOTATIONS, columns=["date", "event"])
# annotations_df.date = pd.to_datetime(annotations_df.date)
# annotations_df["y"] = 10

# annotation_layer = (
#     alt.Chart(annotations_df)
#     .mark_text(size=20, text="⬇", dx=-8, dy=-10, align="left")
#     .encode(
#         x="date:T",
#         y=alt.Y("y:Q"),
#         tooltip=["event"],
#     )
#     .interactive()
# )

# st.altair_chart(
#     (chart + annotation_layer).interactive(),
#     use_container_width=True
# )

st.altair_chart(
    (chart).interactive(),
    use_container_width=True
)