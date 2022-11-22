import streamlit as st 
import pandas as pd 
import matplotlib.pyplot as plt 
import seaborn as sns 
import numpy as np
 
st.title("Palmer's Penguins") 
st.markdown('Use this Streamlit app to make your own scatterplot about penguins!') 

penguin_file = st.file_uploader('Select Your Local Penguins CSV') 
if penguin_file is not None: 
	penguins_df = pd.read_csv(penguin_file) 
else: 
  penguins_df = pd.read_csv('penguins.csv') 
	# st.stop()

st.dataframe(penguins_df.head())

def without_caching(n):
  list_num = np.random.randn(n, 1)
  return sum(list_num)

@st.cache
def with_caching(n):
  list_num = np.random.randn(n, 1)
  return sum(list_num)

st.code(
  """
  functions
  
  def without_caching(n):
    list_num = np.random.randn(n, 1)
    return sum(list_num)
  
  @st.cache
  def with_caching(n):
    list_num = np.random.randn(n, 1)
    return sum(list_num)
  """
)
n = st.number_input('n', step=1)
result1 = without_caching(n)
result2 = with_caching(n)
container = st.container()
st.write('without caching', result1)
st.write('with caching', result2)
n = st.button('rerun')