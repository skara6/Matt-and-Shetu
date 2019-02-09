
# coding: utf-8

# In[2]:


import pandas as pd
from iexfinance.stocks import get_historical_data
from sqlalchemy import create_engine
from datetime import datetime
import numpy as np


# In[3]:


csv_file = "data/S&P.csv"
SP_df = pd.read_csv(csv_file)
SP_df.count()


# In[4]:


csv_file = "data/NASDAQ_NYSE.csv"
NN_df = pd.read_csv(csv_file)
NN_df.count()


# In[5]:


print(f'nyse+nasdaq first date: {NN_df.date.min()} \ns&p first date: {SP_df.date.min()} \n\nnyse+nasdaq last date: {NN_df.date.max()} \ns&p last date: {SP_df.date.max()}')


# In[6]:


if SP_df.date.max() > NN_df.date.max():
    endDate = NN_df.date.max()
else:
    endDate = SP_df.date.max() 
    
if SP_df.date.min() > NN_df.date.min():
    startDate = SP_df.date.min()
else:
    startDate = NN_df.date.min()  


# In[7]:


NN_df = NN_df[NN_df.date > startDate]
SP_df = SP_df[SP_df.date > startDate]

NN_df = NN_df[NN_df.date < endDate]
SP_df = SP_df[SP_df.date < endDate]


# In[8]:


print(f'nyse+nasdaq first date: {NN_df.date.min()} \ns&p first date: {SP_df.date.min()} \n\nnyse+nasdaq last date: {NN_df.date.max()} \ns&p last date: {SP_df.date.max()}')


# In[9]:


#renaming columns to symbol, dropping adj_close column
NN_df = NN_df.drop(columns=['adj_close'])
NN_df = NN_df.rename(columns={'ticker':'symbol'})
SP_df = SP_df.rename(columns={'Name':'symbol'})


# In[10]:


csv_file = "data/ETFList.csv"
ETF_data = pd.read_csv(csv_file)
ETF_symbols = ETF_data['Symbol']

temp_data = pd.DataFrame()
ETF_df = pd.DataFrame()

start = datetime(2014, 1, 1)
end = datetime(2019, 1, 1)

for symbol in ETF_symbols:
    temp_data = get_historical_data(symbol, start, end, output_format = "pandas")
    temp_data['symbol'] = symbol
    ETF_df = ETF_df.append(temp_data)


# In[12]:


ETF_df.to_csv("data/ETF_df.csv")
NN_df.to_csv("data/NN_df.csv")
SP_df.to_csv("data/SP_df.csv")


# In[13]:


from sqlalchemy import create_engine
import MySQLdb


# In[42]:


engine = create_engine('mysql://root:datadata@localhost:3306/markets')

with engine.connect() as con:
    con.execute('drop database if exists markets;')
    con.execute('create database markets;')
    con.execute('use markets;')


# In[49]:


ETF_df.to_sql(con=engine, name='etf', if_exists='replace', index=False)


# In[61]:


stocks_df = NN_df.append(SP_df)
stocks_df = stocks_df.groupby(['date', 'symbol']).first().reset_index()
stocks_df.to_sql(con=engine, name='stocks', if_exists='replace', index=False)


# In[90]:


stock_list = stocks_df.symbol.unique().flatten()
etf_list = ETF_df.symbol.unique().flatten()
symbol_list = np.append(stock_list, etf_list)


# In[99]:


symbol_df = pd.DataFrame(symbol_list)
symbol_df = symbol_df.rename(columns={0:'symbol'})
symbol_df = symbol_df.drop_duplicates()
symbol_df.to_sql(con=engine, name='symbols', if_exists='replace', index=False)


# In[100]:


symbol_df.loc[symbol_df.symbol=='ACT']

