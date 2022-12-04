import streamlit as st

st.set_page_config(
    page_title= 'Korea Climate change Data', 
    page_icon = ':sunny:',
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': "# 2022 winter Data Sciencen and Visualization project. Contributors:  "
    }
)

st.markdown('# :rotating_light: Are we really close to climate breakdown? :rotating_light:')
st.markdown("This page is a Streamlit dashboard that can be used to explore the statistics about climate change in South Korea over the last 50 years.")
st.markdown("#### General Statistics ♟")
st.markdown("This gives a general overview of the data including temperature by day, heat wave, and tropical nights.")
st.markdown("#### Data Sources")
st.markdown('''
        * 기상청 기상자료개방포털
            * link: https://data.kma.go.kr/stcs/grnd/grndTaList.do?pgmNo=70
        * ''')
