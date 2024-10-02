import streamlit as st
import pandas as pd

st.title(':blue[Dashbloard de casas para alugar]')

df_01 = pd.read_csv('houses_to_rent.csv')

st.write(df_01)

