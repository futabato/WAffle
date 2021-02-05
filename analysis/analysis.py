import streamlit as st
import pandas as pd

df_block = pd.read_csv('./block.csv')
st.title('遮断した通信')
st.write(df_block)


df_through = pd.read_csv('./through.csv')
st.title('通した通信')
st.write(df_through)
