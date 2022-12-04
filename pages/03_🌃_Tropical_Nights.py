import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from utilities import to_map_df, getmap
import time
import streamlit as st
import altair as alt 
plt.style.use('ggplot')
rng = (0,40)

df2 = pd.read_csv('total3.csv')

## region_selectbox
region_options = df2['지역'].unique().tolist()
region = st.selectbox('Which region would you like to see?', region_options, 0)
df2 = df2[df2['지역'] == region]
df2.drop(['Unnamed: 0'], axis = 1, inplace = True)

## line_chart animation
lines = alt.Chart(df2).mark_line().encode(
    x=alt.X('연도', title='연도'),
    y=alt.Y('연합계', title='연합계'),
    color = '지역'
).properties(
    width=600,
    height=450
)

@st.cache
def plot_animation(df2):
    lines = alt.Chart(df2).mark_line().encode(
       x=alt.X('연도', axis=alt.Axis(title='연도')),
       y=alt.Y('연합계',axis=alt.Axis(title='연합계')),
     ).properties(
    width=600,
    height=450
)
    return lines


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
                st.plotly_chart(mapfig)
            with c2:
                st.pyplot(histfig)
        time.sleep(speed)

df = pd.read_csv('total.csv')

if __name__ == "__main__":
    # load all data
    res= df
    gb = res.groupby('year')
    years = list(res.year.values.astype(int))

    with st.container():
        # year slider
        year = st.slider("year",1973,2022)
        temp = gb.get_group(year)

        # plot
        label = st.empty()
        e1 = st.empty()
        e2 = st.empty()


        #mdf = to_map_df(res.groupby(['year','location']).mean().reset_index(), datacol = ['avg','year'])
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