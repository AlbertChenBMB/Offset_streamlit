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
st.header('MAU offset AI platformls')
#option =st.selectbox("Please select the area.",('1','4','7'))

'''
### 這頁是首頁
#### 歡迎使用MAU offset AI platform

'''


df=pd.read_csv(open("data/mau01_07.csv"))
data=df[-1000:]
time_range=pd.to_datetime(data["Date"],format='%Y/%m/%d %H:%M')
OA_data=data.filter(regex="OA")
OA_data.index=time_range
for i in ('1','4','7'):  
    check_data=data.filter(regex=("KW")).filter(regex=i)
    data["L"+str(i)+"total_kW"]=0
    num=check_data.shape[1]


    for idx,row in check_data.iterrows():
        total=0
        x=0
        while x < num:
            total=total+(row[x])
            x+=1
            
        data.loc[idx,"L "+str(i)+" total_kW"]=total
    

st.write("You have L10, L40, L70 floor.")


chart_data=data.filter(regex="total_kW")
chart_data.index=time_range
st.header("Total Power")
st.line_chart(chart_data)


st.header("External Weather")
st.line_chart(OA_data)
