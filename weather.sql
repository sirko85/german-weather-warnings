CREATE TABLE checks(
id INT PRIMARY KEY,
datum DATE
);
CREATE TABLE weather_warnings(
id INT PRIMARY KEY,
msgType VARCHAR(50),
event VARCHAR(255),
gruppe VARCHAR(100),
color VARCHAR(12),
headline TEXT,
description TEXT,
datum DATE DEFAULT (datetime('now','localtime')),
'is_checked' BOOL
);
