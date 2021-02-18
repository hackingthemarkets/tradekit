
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'i_lib') THEN
        CREATE TYPE i_lib AS ENUM('tulip', 'ta-lib');
    END IF;
END$$;

CREATE TABLE IF NOT EXISTS asset_indicator 
(
  id SERIAL PRIMARY KEY,
  asset_price_id INTEGER NOT NULL,
  i_lib i_lib,
  sma_20 NUMERIC,
  sma_50 NUMERIC,
  rsi_14 NUMERIC,
  CONSTRAINT fk_asset_price FOREIGN KEY(asset_price_id) REFERENCES asset_price(id)
);