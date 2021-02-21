CREATE TABLE IF NOT EXISTS asset_strategy (
    id INTEGER PRIMARY KEY,
    asset_id INTEGER NOT NULL,
    strategy_id INTEGER NOT NULL,
    FOREIGN KEY (asset_id) REFERENCES asset (id),
    FOREIGN KEY (strategy_id) REFERENCES strategy (id)
)