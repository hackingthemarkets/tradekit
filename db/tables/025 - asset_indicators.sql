
CREATE TYPE i_lib AS ENUM('tulip', 'ta-lib');

CREATE TABLE IF NOT EXISTS asset_indicators 
(
  id SERIAL PRIMARY KEY,
  asset_price_id INTEGER NOT NULL,
  i_lib i_lib,
  sma_20 NUMERIC,
  sma_50 NUMERIC,
  rsi_14 NUMERIC,
  CONSTRAINT fk_asset_price FOREIGN KEY(asset_price_id) REFERENCES asset_price(id)
);