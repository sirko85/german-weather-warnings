ftp_user = ''
ftp_password = ''
location_id = ['']
download_dir = '/var/tmp/weather/'
notifications = {
	'blink1': {
		'status': 'on',
	},
	'raspberry': {
		'status': 'on',
		'gpiopin': '40',
	},
#TODO: telegram module
	'telegram': {
		'status': 'on',
	},
#TODO: send e-mail notification
	'mail': {
		'status': 'on',
	}
}
#download_dir = '/home/pi/scripts/weather/temp/'