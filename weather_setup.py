import sqlite3

db = sqlite3.connect('weather.db')

cursor = db.cursor()
sql_command = """CREATE TABLE checks(
datum DATE
);"""
cursor.execute(sql_command)
sql_command = """CREATE TABLE weather_warnings(
msgType VARCHAR(50),
event VARCHAR(255),
gruppe VARCHAR(100),
color VARCHAR(12),
headline TEXT,
description TEXT,
datum DATE DEFAULT (datetime('now','localtime')),
is_checked BOOL DEFAULT False,
gueltig_ab DATE,
gueltig_bis DATE
);"""
cursor.execute(sql_command)
sql_command = """CREATE UNIQUE INDEX unique_warnings ON weather_warnings(event,headline,gueltig_ab, gueltig_bis);"""
cursor.execute(sql_command)
db.commit()
