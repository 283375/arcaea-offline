CREATE TABLE scores (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    version INTEGER,
    score INTEGER,
    shinyPerfectCount INTEGER,
    perfectCount INTEGER,
    nearCount INTEGER,
    missCount INTEGER,
    date INTEGER,
    songId TEXT,
    songDifficulty INTEGER,
    modifier INTEGER,
    health INTEGER,
    ct INTEGER DEFAULT 0
);

CREATE TABLE cleartypes (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    songId TEXT,
    songDifficulty INTEGER,
    clearType INTEGER,
    ct INTEGER DEFAULT 0
);

INSERT INTO scores ("id", "version", "score", "shinyPerfectCount", "perfectCount", "nearCount", "missCount", "date", "songId", "songDifficulty", "modifier", "health", "ct") VALUES
    ('1', '1', '9441167', '753', '895', '32', '22', '1722100000', 'test1', '2', '2', '0', '0'),
    ('2', '1', '9752087', '914', '1024', '29', '12', '1722200000', 'test2', '2', '0', '100', '0'),
    ('3', '1', '9750000', '900', '1000', '20', '10', '1722200000', 'corrupt1', '5', '0', '0', '0'),
    ('4', '1', '9750000', '900', '1000', '20', '10', '1722200000', 'corrupt2', '2', '9', '0', '0'),
    ('5', '1', '9750000', '900', '1000', '20', '10', '1', 'date1', '2', '0', '0', '0');

INSERT INTO cleartypes ("id", "songId", "songDifficulty", "clearType", "ct") VALUES
    ('1', 'test1', '2', '0', '0'),
    ('2', 'test2', '2', '1', '0'),
    ('3', 'corrupt1', '5', '0', '0'),
    ('4', 'corrupt2', '2', '7', '0'),
    ('5', 'date1', '2', '1', '0');
