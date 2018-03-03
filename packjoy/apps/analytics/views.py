import hashlib, hmac, json

from django.views import View
from django.conf import settings
from django.http import HttpRequest
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from .models import EmailRecord

@method_decorator(csrf_exempt, name='dispatch')
class EmailAnalytics(View):
	def post(self, request):
		'''
		Endpoint for the mailgun trackings
		@TODO: Move this thing inside a job, 
		shouldn't just hang in here
		'''
		# body = request.body.decode('utf-8')
		# data = json.loads(body)
		# print(data)
		# if not self.verify(token=data['token'], timestamp=data['timestamp'],
		# 				   signature=data['signature']):
		# 	# In this case we want mailgun to retry the request
		# 	# Any status code can be returned except 406
		# 	# Returning 406 well cause mailgun to stop trying
		# 	return HttpRequest(status=400)

		# # If the signature is verified we should store the url
		# address = ', '.join([data[fields] for fields in ('country, region, city')])
		# EmailRecord(event=data['event'], recipient=data['recipient'],
		# 			domain=data['domain'], ip=data['ip'],
		# 			address=address, mailing_list=data['mailing-list'],
		# 			user_agent=data['user-agent'])
		# return HttpRequest(status=200)
		pass

	def verify(token, timestamp, signature):
		hmac_digest = hmac.new(key=settings.MAILGUN_ACCESS_KEY,
							   msg='{}{}'.format(timestamp, token),
							   digestmod=hashlib.sha256).hexdigest()
		return hmac.compare_digest(unicode(signature), unicode(hmac_digest))