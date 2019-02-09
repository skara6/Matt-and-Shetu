Matt and Shetu

ETL Project

We used two datasets that contained 5+ years of historical data for all stocks from the S&P500 and Nasdaq/NYSE. They were obtained from Kaggle. We also had a list of top ETF’s which were collected from the website Etfdb.com. We then proceeded to collect data  about the ETF’s from  the internet. The original idea was to get it through API’s , upon researching one of the sites that allowed unlimited API’s called EIX finance we realized it offered a python module that would enable us to collect the data far more efficiently.  

The  stock csv files from Kaggle were loaded as Dataframes.We then proceeded to  clean up the data by dropping a column and renaming them.They were then combined by date. 
The ETF data that we obtained from the web had a different set of historical data available.

The final database includes a table with the top 1000 ETFs in America, all of the stocks in the NYSE, NASDAQ, and S&P500 for the last 5 years.  The primary key for the stocks table is the date and symbol combined, and the primary key for  the  etf table is date. The foreign key for both the stocks and etf tables is ‘symbols’ from the symbol table.
