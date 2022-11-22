import time

import numpy as np
import streamlit as st

progress_bar = st.progress(0)
status_text = st.empty()
last_rows = np.random.randn(1, 1)
chart = st.line_chart(last_rows)

with st.form('first_form'):
    if_stop = st.checkbox('stop at 50')
    total_iteration = st.slider('Total Iteration', min_value=0, max_value=100, value=100, step=1, )
    submit = st.form_submit_button('save change and re-run')

for i in range(1, total_iteration + 1):
    new_rows = last_rows[-1, :] + np.random.randn(50, 1).cumsum(axis=0)
    status_text.text("%i%% Complete" % i)
    chart.add_rows(new_rows)
    progress_bar.progress(i)
    last_rows = new_rows
    time.sleep(0.05)
    if if_stop and i == 50:
        st.stop()

progress_bar.empty()

# Streamlit widgets automatically run the script from top to bottom. Since
# this button is not connected to any other logic, it just causes a plain
# rerun.
st.button("Re-run")
