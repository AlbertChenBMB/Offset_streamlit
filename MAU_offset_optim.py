'''
## offset部分 要考慮的如以下:
1. 每次調整的上限值
2. 最大offset數值改成自動平衡(例如 2, -2, 3 可以改成是4, 0, 5)
3. 追朔offset調整紀錄
4. 確認實際設定Hz是否等於offset後的數值
4. 效益驗證分頁
5. HL 目前做定頻處理因為GP節電，犧牲靜壓
'''
## 應新增可供填寫 Move in 預計時間的功能
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
'''
### MAU offset auto control function.
'''
##option =st.selectbox("Please select the area.",('1','4','7'))
modify_step=st.selectbox("Please select the maximum modify step.",("0.5","1.0","1.5"))
max_offset= st.number_input('Set the max value of offset value.')
