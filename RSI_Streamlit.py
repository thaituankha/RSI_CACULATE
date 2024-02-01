#import thư viện
import streamlit as st
import pandas as pd
import numpy as np 

pip install TA-Lib


import talib
import matplotlib.pyplot as plt
import plotly.express as px

import warnings
warnings.filterwarnings("ignore")

#đọc dữ liệu
data = pd.read_csv('price_data_update.csv')
data = data.drop_duplicates()
data = data[data['volume'] > 100000]

#sắp xếp lại values
data['time'] = pd.to_datetime(data['time'])
data = data.sort_values(['ticker', 'time'])

#hàm tính toán các chỉ số RSI
def calculate_TA(data):
    data['RSI14'] = talib.RSI(data['low'], timeperiod=14)
    return data

#tính toán
group_ticker = data.groupby('ticker')
data_TA = group_ticker.apply(calculate_TA)
data_TA = data_TA.dropna()

#phân loại OV, UB
data_TA['RSI14'] = pd.cut(data_TA['RSI14'], bins=[-float('inf'), 30, 70, float('inf')], labels=[-1, 0, 1])
data_TA.reset_index(drop=True, inplace=True)

#get dữ liệu cổ phiếu nào ở sàn nào để tiến hành count
columns = listing_companies()
columns = columns[['ticker', 'comGroupCode']]
data_merge = pd.merge(columns, data_TA, on='ticker', how='inner')

# Groupby và tính giá trị 1 và -1
Cacula_1 = data_merge.groupby(['comGroupCode', 'time']).agg({'RSI14': lambda x: (x == 1).sum()})
Cacula_1.columns = ['RSI14_1']
Cacula_1.reset_index(inplace = True)
Cacula_am1 = data_merge.groupby(['comGroupCode','time']).agg({'RSI14': lambda x: (x == -1).sum()})
Cacula_am1.columns = ['RSI14_am1']
Cacula_am1.reset_index(inplace = True)
data_merge_cacula = pd.merge(Cacula_1, Cacula_am1, on=['comGroupCode', 'time'], how='inner')

#đếm số ticker
count = data_merge.groupby(['time', 'comGroupCode'])['ticker'].nunique().reset_index()
data_total = pd.merge(data_merge_cacula, count, on=['time', 'comGroupCode'], how='inner')
columns_to_calculate = ['RSI14_1', 'RSI14_am1']

#tạo dataframe chứa dữ liệu RSI
data_per_RSI = data_total[['time', 'comGroupCode']]
for col in columns_to_calculate:
    data_per_RSI[col] = (data_total[col] / data_total['ticker'])
data_per_RSI['time'] = pd.to_datetime(data_per_RSI['time'])

#chỉ chọn sàn HOSE
data_per_RSI = data_per_RSI[data_per_RSI['comGroupCode'] == 'HOSE']

#lấy dữ liệu RSI để plot
data_vnindex = stock_historical_data("VNINDEX", "2000-12-13", "2024-05-04", "1D", "index")
data_vnindex['time'] = pd.to_datetime(data_vnindex['time'])
data_vnindex.drop(['open', 'high', 'low', 'volume', 'ticker'], axis =1, inplace =True)


data_vnindex.rename(columns={'time': 'date', 'close': 'VNINDEX'}, inplace=True)
data_per_RSI.rename(columns={'time': 'date'}, inplace=True)

#merge dữ liệu để plot
data_RSI = pd.merge(data_per_RSI, data_vnindex, on='date', how='inner')
data_RSI.drop('comGroupCode', axis =1, inplace =True)

#lấy số lượng các mã RSI
data_total = data_total[data_total['comGroupCode'] == 'HOSE'].drop('comGroupCode', axis =1)
data_total.rename(columns={'time': 'date'}, inplace=True)

#tạo data cuối cùng để lưu vào excel
data_final = data_RSI.copy()
data_final.rename(columns={'RSI14_1': 'RSI_OB', 'RSI14_am1': 'RSI_OS'}, inplace=True)
data_final['RSI_NEUTRAL'] = 1 - data_final['RSI_OB'] - data_final['RSI_OS']

data_final = pd.merge(data_final, data_total, on='date', how='inner')
data_final.rename(columns={'RSI14_1': 'RSI_OB_number', 'RSI14_am1': 'RSI_OS_number'}, inplace=True)

data_final['OB-OS'] = data_final['RSI_OB'] - data_final['RSI_OS']

st.dataframe(data_final)

fig = go.Figure()
fig.add_trace(go.Scatter(x=data_final['date'], y=data_final['RSI_OB'], mode='lines', name='quá mua'))
fig.add_trace(go.Scatter(x=data_final['date'], y=data_final['RSI_OS'], mode='lines', name='quá bán'))
fig.add_trace(go.Scatter(x=data_final['date'], y=data_final['VNINDEX'], mode='lines', name='VNINDEX', yaxis='y2'))
fig.update_layout(
    title='RSI và VNINDEX',
    xaxis=dict(title='Thời gian'),
    yaxis=dict(title='RSI %'),
    yaxis2=dict(title='VNINDEX', overlaying='y', side='right'),
    legend=dict(x=0.7, y=1)
)
st.plotly_chart(fig)


fig = go.Figure()
fig.add_trace(go.Scatter(x=data_final['date'], y=data_final['OB-OS'], mode='lines', name='quá mua trừ quá bán'))
fig.add_trace(go.Scatter(x=data_final['date'], y=data_final['VNINDEX'], mode='lines', name='VNINDEX', yaxis='y2'))
fig.update_layout(
    title='OB - OS và VNINDEX',
    xaxis=dict(title='Thời gian'),
    yaxis=dict(title='%'),
    yaxis2=dict(title='VNINDEX', overlaying='y', side='right'),
    legend=dict(x=0.7, y=1)
)
st.plotly_chart(fig)
