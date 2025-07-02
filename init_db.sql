
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS stations;
DROP TABLE IF EXISTS favorites;

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE stations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    address TEXT NOT NULL,
    city TEXT NOT NULL,
    pincode TEXT NOT NULL,
    lat REAL,
    lng REAL,
    battery_types TEXT
);

CREATE TABLE favorites (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    station_id INTEGER,
    FOREIGN KEY (user_id) REFERENCES users (id),
    FOREIGN KEY (station_id) REFERENCES stations (id)
);

INSERT INTO stations (name, address, city, pincode, lat, lng, battery_types) VALUES
('Station A', '123 Street, Area A', 'Mumbai', '400001', 19.0760, 72.8777, 'Lithium-ion, Lead-acid'),
('Station B', '456 Road, Area B', 'Pune', '411001', 18.5204, 73.8567, 'Lithium-ion, Lead-acid');
