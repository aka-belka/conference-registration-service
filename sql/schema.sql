CREATE TABLE IF NOT EXISTS events ( 
    id INTEGER PRIMARY KEY, 
    title TEXT NOT NULL,  
    date TEXT NOT NULL,
    max_seats INTEGER NOT NULL,
    registered INTEGER NOT NULL DEFAULT 0
); 

CREATE TABLE IF NOT EXISTS participants ( 
    id INTEGER PRIMARY KEY, 
    name TEXT NOT NULL, 
    email TEXT NOT NULL 
); 

CREATE TABLE IF NOT EXISTS tickets ( 
    id INTEGER PRIMARY KEY, 
    event_id INTEGER NOT NULL, 
    participant_id INTEGER NOT NULL, 
    status TEXT NOT NULL,
    number TEXT NOT NULL UNIQUE,
    FOREIGN KEY (event_id) REFERENCES events(id), 
    FOREIGN KEY (participant_id) REFERENCES participants(id) 
);