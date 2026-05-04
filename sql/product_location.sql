CREATE TABLE IF NOT EXISTS product_location (
    product_location_id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_line TEXT,
    branch TEXT,
    city TEXT,
    markup_rate REAL
);