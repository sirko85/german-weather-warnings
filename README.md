# german-weather-warnings
checks german weather warnings via the dwd FTP-Server for your location.

You can check with crontab every x minutes for new warnings for your location.
You can push notifications via blink(1), Raspberry GPIO Pin, Telegram Messanger and E-Mail.

## Required

- >= python3.4
- sqlite3 python module

## Installation

- register you on [dwd.de](http://www.dwd.de/DE/fachnutzer/dienstleister/grundversorgung/grundversorgung_node.html) to a free ftp account for the free primary care
- Copy the config.smaple.py to config.py and edit your settings
- `python3 weather_setup.py` use it to create the database and to show a list of all current location_id's with current warnings

## TODOS

## Raspberry Pi installation

- To sending E-Mail notifications you need python3.4, also on a raspberry pi. How to install a current python3 version click [here](http://sowingseasons.com/blog/building-python-3-4-on-raspberry-pi-2.html)
