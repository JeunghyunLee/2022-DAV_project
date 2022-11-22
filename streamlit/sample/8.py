import streamlit as st

st.markdown(
            """
            <p>이미지 삽입 예시</p>
            <img src="https://upload.wikimedia.org/wikipedia/commons/2/22/Yann_LeCun_-_2018_%28cropped%29.jpg" width=50% hieght=50%">
            <p>페이지 삽입 예시</p>
            <iframe src="https://sports.news.naver.com/wfootball/index.nhn" width="600" height="600"></iframe>
            """,
            unsafe_allow_html=True
        )