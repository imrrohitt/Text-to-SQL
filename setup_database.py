import sqlite3

# Connect to SQLite database (creates a file named ecommerce.db)
conn = sqlite3.connect('ecommerce.db')
cursor = conn.cursor()

# Create tables
cursor.executescript("""
CREATE TABLE IF NOT EXISTS orders (
    order_id TEXT PRIMARY KEY,
    user_id TEXT,
    product_id TEXT,
    city TEXT,
    order_date DATETIME,
    quantity INTEGER
);

CREATE TABLE IF NOT EXISTS users (
    user_id TEXT PRIMARY KEY,
    username TEXT
);
""")

# Insert sample data
cursor.executescript("""
INSERT OR REPLACE INTO orders (order_id, user_id, product_id, city, order_date, quantity) VALUES
('550e8400-e29b-41d4-a716-446655440000', '6ba7b810-9dad-11d1-80b4-00c04fd430c8', '123e4567-e89b-12d3-a456-426614174000', 'Bangalore', '2025-07-25 10:00:00', 2),
('550e8400-e29b-41d4-a716-446655440001', '6ba7b811-9dad-11d1-80b4-00c04fd430c8', '123e4567-e89b-12d3-a456-426614174001', 'Bangalore', '2025-07-24 12:00:00', 1),
('550e8400-e29b-41d4-a716-446655440002', '6ba7b810-9dad-11d1-80b4-00c04fd430c8', '123e4567-e89b-12d3-a456-426614174002', 'Mumbai', '2025-07-20 15:00:00', 3),
('550e8400-e29b-41d4-a716-446655440003', '6ba7b810-9dad-11d1-80b4-00c04fd430c8', '123e4567-e89b-12d3-a456-426614174003', 'Bangalore', '2025-07-23 09:00:00', 4),
('550e8400-e29b-41d4-a716-446655440004', '6ba7b810-9dad-11d1-80b4-00c04fd430c8', '123e4567-e89b-12d3-a456-426614174004', 'Bangalore', '2025-07-22 14:00:00', 1);

INSERT OR REPLACE INTO users (user_id, username) VALUES
('6ba7b810-9dad-11d1-80b4-00c04fd430c8', 'alice'),
('6ba7b811-9dad-11d1-80b4-00c04fd430c8', 'bob');
""")

# Commit and close
conn.commit()
conn.close()
print("SQLite database created and populated successfully.")