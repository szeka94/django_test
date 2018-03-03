import requests
import os
import json 
from datetime import datetime
from celery.schedules import crontab
from celery.task import periodic_task


api_key = os.environ.get('MAILGUN_ACCESS_KEY')
domain = os.environ.get('MAILGUN_SERVER_NAME')
current_date = datetime.now().strftime('%Y_%m_%d')
file_name = 'stats_{}.json'.format(current_date)
file_path = os.path.abspath('stats/email_stats')
path = os.path.join(file_path, file_name)


@periodic_task(run_every=crontab(minute=0, hour=0))
def get_stats():
	url = "https://api.mailgun.net/v3/{}/stats/total".format(domain)
	data = requests.get(
		url,
		auth=("api", api_key),
		params={"event": ["accepted", "delivered", "failed"],
				"duration": "1m"})
	with open(path, 'w') as outfile:
		json.dump(data.text, outfile)


if __name__ == '__main__':
	get_stats()