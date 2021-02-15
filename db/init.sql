CREATE TABLE IF NOT EXISTS asset (
    id SERIAL PRIMARY KEY, 
    symbol TEXT NOT NULL UNIQUE, 
    name TEXT NOT NULL,
    exchange TEXT NOT NULL,
    shortable BOOLEAN NOT NULL,
    class ENUM('stock', 'crypto', 'forex'),
    source ENUM('alpaca', 'polygon', 'binance'),
    source_id TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS asset_price 
(
  id SERIAL PRIMARY KEY,
  dt TIMESTAMP WITHOUT TIME ZONE NOT NULL,
  asset_id INTEGER NOT NULL,
  open NUMERIC NOT NULL,
  high NUMERIC NOT NULL,
  low NUMERIC NOT NULL,
  close NUMERIC NOT NULL,
  volume NUMERIC NOT NULL,
  CONSTRAINT fk_asset FOREIGN KEY(asset_id) REFERENCES asset(id)
);

CREATE TABLE IF NOT EXISTS asset_tick  
(
  id SERIAL PRIMARY KEY,
  dt TIMESTAMP WITHOUT TIME ZONE NOT NULL,
  asset_id INTEGER NOT NULL,
  bid NUMERIC NOT NULL,
  ask NUMERIC NOT NULL,
  bid_vol NUMERIC,
  ask_vol NUMERIC,
  CONSTRAINT fk_asset FOREIGN KEY(asset_id) REFERENCES asset(id)
);