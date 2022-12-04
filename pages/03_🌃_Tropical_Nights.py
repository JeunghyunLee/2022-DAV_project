import pandas as pd
import matplotlib.pyplot as plt
from utilities import to_map_df, getmap, areas, years
import time
import streamlit as st
import altair as alt 
plt.style.use('ggplot')
rng = (0,25)
with st.sidebar:
    region = st.selectbox("Select the City", areas)


def plot_animation(df2):
    lines = alt.Chart(df2).mark_line().encode(
       x=alt.X('연도', axis=alt.Axis(title='연도')),
       y=alt.Y('연합계',axis=alt.Axis(title='연합계')),
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
    year = st.slider("Select Year",min(years),max(years), value=max(years))
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
            st.plotly_chart(mapfig, use_container_width=True)
        with c2:
            st.pyplot(histfig)

    st.button("Play",on_click=animation)




df2 = pd.read_csv('data_tropical/total3.csv')

## region_selectbox
df2 = df2[df2['지역'] == region]
df2.drop(['Unnamed: 0'], axis = 1, inplace = True)

## line_chart animation
lines = alt.Chart(df2).mark_line().encode(
    x=alt.X('연도', title='연도'),
    y=alt.Y('연합계', title='연합계'),
    color = '지역'
    ).properties(width=600,height=450)


N = df2.shape[0] # number of elements in the dataframe
burst = 6       # number of elements (months) to add to the plot
size = burst     # size of the current dataset

line_plot = st.altair_chart(lines)
start_btn = st.button('Start')

if start_btn:
   for i in range(1,N):
      step_df2 = df2.iloc[0:size]
      lines = plot_animation(step_df2)
      line_plot = line_plot.altair_chart(lines)
      size = i + burst
      if size >= N: 
         size = N - 1
      time.sleep(0.1)


st.markdown('#')
st.markdown('#')

