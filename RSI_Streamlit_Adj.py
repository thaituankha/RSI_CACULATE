#import thư viện
import streamlit as st
import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objs as go


import warnings
warnings.filterwarnings("ignore")

data_final =pd.read_excel('caculate_OB_OS_RSI.xlsx')
data_final['OB'] = data_final['RSI_OB_number'] / (data_final['RSI_OB_number']+data_final['RSI_OS_number'])
data_final['OS'] = data_final['RSI_OS_number'] / (data_final['RSI_OB_number']+data_final['RSI_OS_number'])

st.dataframe(data_final)

fig = go.Figure()
fig.add_trace(go.Scatter(x=data_final['date'], y=data_final['RSI_OB'], mode='lines', name='quá mua', line=dict(color='green')))
fig.add_trace(go.Scatter(x=data_final['date'], y=data_final['RSI_OS'], mode='lines', name='quá bán', line=dict(color='red')))
fig.add_trace(go.Scatter(x=data_final['date'], y=data_final['VNINDEX'], mode='lines', name='VNINDEX', yaxis='y2', line=dict(color='blue')))
fig.update_layout(
    title='RSI và VNINDEX',
    xaxis=dict(title='Thời gian'),
    yaxis=dict(title='%'),
    yaxis2=dict(title='VNINDEX', overlaying='y', side='right'),
    legend=dict(x=0.7, y=1)
)
st.plotly_chart(fig)


fig = go.Figure()
fig.add_trace(go.Scatter(x=data_final['date'], y=data_final['OB'], mode='lines', name='quá mua', line=dict(color='green')))
fig.add_trace(go.Scatter(x=data_final['date'], y=data_final['OS'], mode='lines', name='quá bán', line=dict(color='red')))
fig.update_layout(
    title='Tỷ lệ quá mua/quá bán trên tổng quá mua, quá bán và VNINDEX',
    xaxis=dict(title='Thời gian'),
    yaxis=dict(title='%'),
    yaxis2=dict(title='VNINDEX', overlaying='y', side='right'),
    legend=dict(x=0.7, y=1)
)
st.plotly_chart(fig)


#biểu đồ SMA200
data_SMA_200 = pd.read_csv('data_SMA200.csv')

fig = go.Figure()
fig.add_trace(go.Scatter(x=data_SMA_200['date'], y=data_SMA_200['% CP có giá trên SMA200'], mode='lines', name='% CP có giá trên SMA200', line=dict(color='green')))
fig.add_trace(go.Scatter(x=data_SMA_200['date'], y=data_SMA_200['% CP có giá dưới SMA200'], mode='lines', name='% CP có giá dưới SMA200', line=dict(color='red')))
#fig.add_trace(go.Scatter(x=data_SMA_200['date'], y=data_SMA_200['index'], mode='lines', name='Vnindex', yaxis='y2', line=dict(color='blue')))
fig.update_layout(
    title='SMA200',
    xaxis=dict(title='Thời gian'),
    yaxis=dict(title='%'),
    yaxis2=dict(title='VNINDEX', overlaying='y', side='right'),
    legend=dict(x=0.7, y=1)
)
st.plotly_chart(fig)

