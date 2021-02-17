DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'class') THEN
        CREATE TYPE class AS ENUM('stock', 'crypto', 'forex');
    END IF;
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'source') THEN
        CREATE TYPE source AS ENUM('alpaca', 'polygon', 'binance', 'yf');
    END IF;
END$$;

CREATE TABLE IF NOT EXISTS asset (
    id SERIAL PRIMARY KEY, 
    symbol TEXT NOT NULL UNIQUE, 
    name TEXT NOT NULL,
    exchange TEXT NOT NULL,
    shortable BOOLEAN NOT NULL,
    class class,
    source source,
    source_id TEXT NOT NULL
);