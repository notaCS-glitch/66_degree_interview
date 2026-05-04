CREATE TABLE IF NOT EXISTS sales (
    invoice_id TEXT PRIMARY KEY,
    customer_id INTEGER,
    product_location_id INTEGER,
    quantity INTEGER,
    unit_price REAL,
    markup_amount REAL,
    total REAL,
    date TEXT,
    time TEXT,
    payment TEXT,
    rating REAL,
    FOREIGN KEY (customer_id) REFERENCES customer (customer_id),
    FOREIGN KEY (product_location_id) REFERENCES product_location (product_location_id)
);