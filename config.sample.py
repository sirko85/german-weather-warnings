ftp_user = ''
ftp_password = ''
ftp_server = 'ftp-outgoing2.dwd.de'
location_id = ['']
download_dir = '/var/tmp/weather/'
notifications = {
	'blink1': {
		'status': 'on',
	},
	'raspberry': {
		'status': 'off',
		'gpiopin': '40',
	},
#TODO: telegram module
	'telegram': {
		'status': 'off',
		'contactname': 'hans_wurst',
		'telegram_send_script_path': '/path/to/send_script',
		'msg': "Unwetterwarnung: {headline} | {description} | {valid_till}",
		# possible Infos:headline, description, valid_till, valid_from, color, weather_group, event, msgType
		'automaticcheck': True,
	},
	'mail': {
		'status': 'on',
		'mail': 'test@example.org',
		'subject': 'Unwetterwarnung',
		'msg': "Unwetterwarnung: {headline} \n\n {description} \n\n Gültig ab: {valid_from} \n\n Gültig bis: {valid_till}",
		# possible Infos:headline, description, valid_till, valid_from, color, weather_group, event, msgType
		'automaticcheck': True,
		'smtp_mail_server': '',
		'smtp_port': 587,
		'login': '',
		'password': '',
	}
}
#download_dir = '/home/pi/scripts/weather/temp/'
