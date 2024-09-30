CREATE TABLE packages(
    `id` TEXT PRIMARY KEY NOT NULL,
    `name` TEXT NOT NULL DEFAULT ""
);

CREATE TABLE charts(
    song_id TEXT NOT NULL DEFAULT '',
    rating_class INTEGER NOT NULL DEFAULT 0,
    name_en TEXT NOT NULL DEFAULT '',
    name_jp TEXT DEFAULT '',
    artist TEXT NOT NULL DEFAULT '',
    bpm TEXT NOT NULL DEFAULT '',
    bpm_base DOUBLE NOT NULL DEFAULT 0,
    `set` TEXT NOT NULL DEFAULT '',
    `time` INTEGER DEFAULT 0,
    side INTEGER NOT NULL DEFAULT 0,
    world_unlock BOOLEAN NOT NULL DEFAULT 0,
    remote_download BOOLEAN DEFAULT '',
    bg TEXT NOT NULL DEFAULT '',
    `date` INTEGER NOT NULL DEFAULT 0,
    `version` TEXT NOT NULL DEFAULT '',
    difficulty INTEGER NOT NULL DEFAULT 0,
    rating INTEGER NOT NULL DEFAULT 0,
    note INTEGER NOT NULL DEFAULT 0,
    chart_designer TEXT DEFAULT '',
    jacket_designer TEXT DEFAULT '',
    jacket_override BOOLEAN NOT NULL DEFAULT 0,
    audio_override BOOLEAN NOT NULL DEFAULT 0,
    PRIMARY KEY(song_id, rating_class)
);


INSERT INTO packages ("id", "name") VALUES
    ('base', 'Base Pack'),
    ('core', 'Core Pack');

INSERT INTO charts ("song_id", "rating_class", "name_en", "name_jp", "artist", "bpm", "bpm_base", "set", "time", "side", "world_unlock", "remote_download", "bg", "date", "version", "difficulty", "rating", "note", "chart_designer", "jacket_designer", "jacket_override", "audio_override") VALUES
    ('base1', '0', 'Base song 1', 'ベース・ソング・ワン', 'Artist', '1024', '1024.0', 'base', '1024', '1', '1', '0', '', '1400067914', '1.0', '6', '30', '500', 'Charter', '78rwey63a', '0', '0'),
    ('base1', '1', 'Base song 1', 'ベース・ソング・ワン', 'Artist', '1024', '1024.0', 'base', '1024', '1', '1', '0', '', '1400067914', '1.0', '12', '60', '700', 'Charter', '78rwey63b', '0', '0'),
    ('base1', '2', 'Base song 1', 'ベース・ソング・ワン', 'Artist', '1024', '1024.0', 'base', '1024', '1', '1', '0', '', '1400067914', '1.0', '18', '90', '1000', 'Charter', '78rwey63c', '0', '0');
