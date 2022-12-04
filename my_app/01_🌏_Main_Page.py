import pandas as pd
import numpy as np
import datetime
import time
from utilities import to_map_df
import matplotlib.pyplot as plt
import time, json, datetime

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

st.set_page_config(
    page_title= 'Korea Climate change Data', 
    page_icon = ':sunny:',
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        # 'Get Help': 'https://www.extremelycoolapp.com/help',
        # 'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# 2022 winter Data Sciencen and Visualization project. Contributors:  "
    }
)

import streamlit as st

# def main_page():
#     st.markdown("# Main page 🎈")
#     st.sidebar.markdown("# Main page 🎈")

# def page2():
#     st.markdown("# Page 2 ❄️")
#     st.sidebar.markdown("# Page 2 ❄️")

# def page3():
#     st.markdown("# Page 3 🎉")
#     st.sidebar.markdown("# Page 3 🎉")

# page_names_to_funcs = {
#     "Main Page": main_page,
#     "Page 2": page2,
#     "Page 3": page3,
# }

# selected_page = st.sidebar.selectbox("Select a page", page_names_to_funcs.keys())
# page_names_to_funcs[selected_page]()

# #https://icons.getbootstrap.com/
# with st.sidebar:
#     selected = option_menu("", ["Home", 'Stats'], 
#         icons=['house', 'bar-chart'], menu_icon="cast", default_index=0)
#     #selected(returns-> either one of home, story )
# with st.sidebar:
#     add_topic = st.radio(
#         "Choose a topic you are interested",
#         ('기온', '열대야', '폭염', '강수량')
#     )

# Home 기본 페이지 설정 
# if selected == 'Home' :
st.markdown('# :rotating_light: Are we really close to climate breakdown? :rotating_light:')
st.markdown("This page is a Streamlit dashboard that can be used to explore the statistics about climate change in South Korea over the last 50 years.")
st.markdown("#### General Statistics ♟")
st.markdown("This gives a general overview of the data including temperature by day, heat wave, and tropical nights.")
st.markdown("#### Data Sources")
st.markdown('''
        * 기상청 기상자료개방포털
            * link: https://data.kma.go.kr/stcs/grnd/grndTaList.do?pgmNo=70
        * ''')
