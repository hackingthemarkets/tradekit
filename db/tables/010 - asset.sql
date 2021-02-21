DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'source') THEN
        CREATE TYPE source AS ENUM('alpaca', 'polygon', 'binance', 'yf');
    END IF;
END$$;

CREATE TABLE IF NOT EXISTS asset(
    id SERIAL PRIMARY KEY, 
    symbol TEXT NOT NULL UNIQUE, 
    name TEXT NOT NULL,
    market TEXT,
    locale TEXT,
    currency TEXT,
    exchange TEXT NOT NULL,
    source source, 
    easy_to_borrow BOOLEAN,
    marginable BOOLEAN,
    shortable BOOLEAN,
    class TEXT,
    type TEXT, 
    active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at timestamp NOT NULL default current_timestamp,
    updated_at timestamp NOT NULL default current_timestamp
);

CREATE OR REPLACE FUNCTION trigger_set_timestamp()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = current_timestamp;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DO $$
BEGIN
  IF NOT EXISTS(SELECT *
    FROM information_schema.triggers
    WHERE event_object_table = 'asset'
    AND trigger_name = 'set_updated_at'
  )
  THEN
    CREATE TRIGGER set_updated_at AFTER INSERT ON asset FOR EACH ROW EXECUTE PROCEDURE trigger_set_timestamp();
  END IF;
END$$;