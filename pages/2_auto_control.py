import streamlit as st
import pandas as pd
import altair as alt
import re
import numpy as np
from scipy.stats import pearsonr
from sklearn.model_selection import TimeSeriesSplit
import statsmodels.regression.linear_model as sm
import statsmodels.api as sm2
import plotly.express as px
import datetime
from datetime import timedelta

st.set_page_config(
    page_title="Offset optimization"
)
st.header('MAU offset AI platformls')
'''
### MAU offset auto control function.
'''
##option =st.selectbox("Please select the area.",('1','4','7'))
modify_step=st.selectbox("Please select the maximum modify step.",("0.5","1.0","1.5"))
max_offset= st.number_input('Set the max value of offset value.')

st.write(float(modify_step))
st.write(float(max_offset))

offset_setting=pd.read_csv(open("control//control.csv"))
real_time=pd.read_csv(open("online_data.csv"))
real_time["Date"]=pd.to_datetime(real_time["Date"],format='%Y/%m/%d %H:%M')


st.dataframe(offset_setting)