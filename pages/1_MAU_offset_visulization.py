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
## 應新增該層設定數值MAU數值

## 解決AI切回PLC出現offset數值keep住的問題(要跟空調同仁確認影響和限制)
st.set_page_config(
    page_title="Offset home page."
)

st.header('MAU offset visulization')
'''
### Visulization and model training
'''
option =st.selectbox("Please select the area.",('1','4','7'))
#st.write('You selected: L',option,'0')
i =option

data=pd.read_csv(open("mau01_07.csv"))
OA_data=data.filter(regex="OA")

oa_check =st.selectbox("Do you want to consider external air?",('Yes','No'))


data.Date=pd.to_datetime(data.Date,format='%Y/%m/%d %H:%M')
beging_Day= data['Date'].iloc[0]
end_Day= data['Date'].iloc[-1]

if st.checkbox('read data'):

    st.header('Show the information of'+' L'+option+'0 area!')


    if i in ('1','4','7'):  

        visu_data=pd.merge(data.filter(regex=(("MAU"+i))),OA_data,left_index=True,right_index=True,how='outer')
        check_data=visu_data.filter(regex=("KW"))
        tab = st.tabs(list(check_data.columns))

        for tb,j in enumerate(check_data.columns):
            with tab[tb]:
                x=j.split('_')[0]
                
                regr_data=visu_data.dropna(how="any").filter(regex=(x))
                st.subheader(x)
                st.write(regr_data.head(5))
                OA_data=visu_data.dropna(how="any").filter(regex=('OA'))
                vfd_f=regr_data.iloc[:,0]
                TT=OA_data.iloc[:,0]
                MT=OA_data.iloc[:,1]
                E=OA_data.iloc[:,2]
                vfd_kw=regr_data.iloc[:,1]
                #print(regr_data.iloc[:,1].columns())
                corr,_= pearsonr(vfd_f**3,vfd_kw)
                TT_corr,_= pearsonr(TT,vfd_kw)
                MT_corr,_= pearsonr(MT,vfd_kw)
                E_corr,_= pearsonr(E,vfd_kw)
                if corr >0.9:
                    
                    st.write("cor:"+str(corr))
                    #st.write("TT_corr:"+str(TT_corr))
                    #st.write("MT_corr:"+str(MT_corr))
                    #st.write("E_corr:"+str(E_corr))

                    
                    fig =px.scatter(
                        regr_data,
                        x=regr_data.iloc[:,1].name,
                        y=regr_data.iloc[:,0].name,
                                        
                    )
                    #tab = st.tabs(["Plotly native theme"])
                    st.plotly_chart(fig, theme="streamlit", use_conatiner_width=True)        
                                
                
                else:
                    
                    st.write("cor ="+str('%.2f' %corr)+", which is too low, check the data!")
                    st.subheader("MAU_"+i+"_"+x)
                    fig =px.scatter(
                        regr_data,
                        x=regr_data.iloc[:,1].name,
                        y=regr_data.iloc[:,0].name,
                                        
                    )
                    #tab = st.tabs(["Plotly native theme"])
                    st.plotly_chart(fig, theme="streamlit", use_conatiner_width=True)
    else:
        st.write('goodbye')

    if st.checkbox('Select training time.'):
        begin_d= st.date_input("select beging data of training data.",value=beging_Day,min_value=beging_Day,max_value=end_Day)
        
        end_d=begin_d+datetime.timedelta(days=30)
        time_data=pd.merge(data.filter(regex=(("MAU"+i))),OA_data,left_index=True,right_index=True,how='outer').copy()
        time_data=pd.merge(data.filter(regex=(("Date"))),time_data,left_index=True,right_index=True,how='outer').copy()
        time_data['Day']=pd.to_datetime(time_data['Date']).dt.date
        train_data= time_data.loc[(time_data["Day"]>begin_d)]
        st.write(train_data.head(5))
        if st.checkbox('Training model'):
            from sklearn.linear_model import LinearRegression as LR
            from sklearn.metrics import mean_absolute_percentage_error as mape

            check_columns=train_data.filter(regex=("KW"))
            tab = st.tabs(list(check_data.columns))
            for tb,j in enumerate(check_data.columns):
                with tab[tb]:
                    unite_name=j.split('_')[0]
                    regr_data=train_data.dropna(how="any").filter(regex=(unite_name))
                    OA_data=train_data.dropna(how="any").filter(regex=('OA_E1'))
                    training_data=pd.merge(regr_data,OA_data,left_index=True,right_index=True,how='outer').copy()
                    training_data=training_data.dropna(how="any")[(training_data[j]>10)&(training_data["OA_E1"]>0)]
                    x=training_data.copy().drop(unite_name+"_VFD_KW",axis=1)
                    x[unite_name+"_VFD_F"]=(x[unite_name+"_VFD_F"]**3)/1000
                    y=training_data[unite_name+"_VFD_KW"]
                    df=pd.DataFrame({"VFD_F**3":x[unite_name+"_VFD_F"],"KW":y})
                    reg=LR().fit(x,y)
                    fig =px.scatter(
                        df,
                        x="VFD_F**3",
                        y="KW",
                                        
                    )
                    #tab = st.tabs(["Plotly native theme"])
                    st.plotly_chart(fig, theme="streamlit", use_conatiner_width=True)
                    
                    train_pred=reg.predict(x)
                    st.write(reg.coef_)
                    st.write("training_mape:"+ str(mape(y,train_pred)))
                    


                    
    else:
        st.write('Use the same model')
st.write("That's it!")