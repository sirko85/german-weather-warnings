import sqlite3
from lib.weather import weather

db = sqlite3.connect('weather.db')

cursor = db.cursor()

sql_command = """CREATE TABLE checks(
created_at DATE
);"""
cursor.execute(sql_command)

sql_command = """CREATE TABLE weather_warnings(
msgType VARCHAR(50),
event VARCHAR(255),
weather_group VARCHAR(100),
color VARCHAR(12),
headline TEXT,
description TEXT,
created_at DATE DEFAULT (datetime('now','localtime')),
is_checked BOOL DEFAULT False,
valid_from DATE,
valid_till DATE
);"""
cursor.execute(sql_command)

sql_command = """CREATE UNIQUE INDEX unique_warnings ON weather_warnings(event,headline,valid_from, valid_till);"""
cursor.execute(sql_command)
db.commit()
weatherwarning = weather()
print('Current Location ID\'s:')
weatherwarning.printCurrentIds()
