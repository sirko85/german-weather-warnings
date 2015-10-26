# german-weather-warnings
checks german weather warnings via the dwd FTP-Server for your location.

It's my first Python project. I want to check with crontab every x minutes for new warnings for my location.
The script is running on a raspberry pi and use for the notification a blink(1)

## Required Python Modules

- sqlite3

## Installation

- register you on [dwd.de](http://www.dwd.de/DE/fachnutzer/dienstleister/grundversorgung/grundversorgung_node.html) to a free ftp account for the free primary care
- Copy the config.smaple.py to config.py and edit your settings
- create a sqlite3 database in this directory with name "weather.db"

## TODOS

- Notification with Telegram Messanger
- Notification with E-Mail
