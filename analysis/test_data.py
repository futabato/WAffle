import streamlit as st
import pandas as pd

st.title('テストデータの分析')

df = pd.read_csv('../model/evaluation/evaluation.csv')

st.write(df)

st.title('False Negative一覧')
st.write(df[(df['Target']==1)&(df['WAffle']==0)]['URL'])
st.title('False Positive一覧')
st.write(df[(df['Target']==0)&(df['WAffle']==1)]['URL'])