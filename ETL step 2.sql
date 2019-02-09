use markets;

ALTER TABLE stocks MODIFY date date;
ALTER TABLE etf MODIFY date date;

ALTER TABLE stocks MODIFY symbol varchar(20);
ALTER TABLE etf MODIFY symbol varchar(20);
ALTER TABLE symbols MODIFY symbol varchar(20);

ALTER TABLE stocks 
add constraint pk_date primary key (date,symbol);

ALTER TABLE etf 
ADD CONSTRAINT fk_etf_symbol
  FOREIGN KEY (symbol)
  REFERENCES symbols(symbol);
  
ALTER TABLE stocks 
ADD CONSTRAINT fk_stock_symbol
  FOREIGN KEY (symbol)
  REFERENCES symbols(symbol);
  
