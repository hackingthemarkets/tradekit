CREATE TYPE timespan AS ENUM('minute', 'hour', 'day', 'week', 'month', 'quarter', 'year');

CREATE TABLE IF NOT EXISTS asset_price 
(
  id SERIAL PRIMARY KEY,
  dt TIMESTAMP WITHOUT TIME ZONE NOT NULL,
  asset_id INTEGER NOT NULL,
  timespan timespan,
  source source,
  open NUMERIC NOT NULL,
  high NUMERIC NOT NULL,
  low NUMERIC NOT NULL,
  close NUMERIC NOT NULL,
  volume NUMERIC NOT NULL,
  CONSTRAINT fk_asset FOREIGN KEY(asset_id) REFERENCES asset(id)