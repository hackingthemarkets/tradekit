CREATE TYPE class AS ENUM('stock', 'crypto', 'forex');
CREATE TYPE source AS ENUM('alpaca', 'polygon', 'binance', 'yf');

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