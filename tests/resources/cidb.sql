CREATE TABLE charts_info (
    song_id TEXT NOT NULL,
    rating_class INTEGER NOT NULL,
    constant INTEGER NOT NULL,
    notes INTEGER
);

INSERT INTO charts_info (song_id, rating_class, constant, notes) VALUES
    ("test1", 1, 90, 900),
    ("test2", 2, 95, 950),
    ("test3", 3, 100, NULL);
