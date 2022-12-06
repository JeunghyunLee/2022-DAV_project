import streamlit as st
from streamlit_player import st_player

st.set_page_config(
    page_title= 'Korea Climate change Data', 
    page_icon = ':sunny:',
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': "# 2022 데이터 시각화 : 나연, 성만, 정현, 채린, 한휘  "
        'Reference' : 'https://www.tumblbug.com/meltingearth'
    }
)

st.image("./melting_earth.png", width=130)
st.markdown('# 녹는 아이스크림, 지구맛 출시 :droplet:')
st.markdown("This page is a Streamlit dashboard that can be used to explore the statistics about climate change in South Korea over the past 50 years.")
st.markdown("#### 들어가며 ♟")
st.markdown("본 페이지는 ___를 위해 제작되었습니다.")
st.markdown("#### 사용한 데이터")
st.markdown('''
        * 기상청 [기상자료개방포털](https://data.kma.go.kr/stcs/grnd/grndTaList.do?pgmNo=70)
        ''')
# misc contents
with st.container():
    st.markdown("""---""")
    st.markdown('#### 관련 컨텐츠')
    st.markdown('''
        If you are interested in learning more informations about climate change in South Korea here are few references that you might want to check out!
        * Documents
            * 기상청, [한국 기후변화 평가 보고서 2020](http://www.climate.go.kr/home/cc_data/2020/Korean_Climate_Change_Assessment_Report_2020_2.pdf)
            * IPCC [Climate Change 2022](https://www.ipcc.ch/report/ar6/wg3/downloads/report/IPCC_AR6_WGIII_SPM.pdf)
        * Books
            * 이동학, 쓰레기책:왜 지구의 절반은 쓰레기도 뒤덮이는가
            * 김백민, 우리는 결국 지구를 위한 답을 찾을 것이다
            * 박훈, 지속가능한 미래를 위한 기후변화 데이터북 
        ''')
    st.markdown("""---""")
    fig_col1, fig_col2 = st.columns(2)
    with fig_col1 :
        # Embed a youtube video
        st.markdown('##### Netflix: Our planet, Frozen Worlds')
        st_player("https://youtu.be/cTQ3Ko9ZKg8")
        
    with fig_col2 : 
        # Embed a youtube video
        st.markdown('##### Economist: See what three degrees of global warming looks like')
        st_player("https://youtu.be/uynhvHZUOOo")

