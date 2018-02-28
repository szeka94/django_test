from django.db import models

'''
maybe it would be a good idea to move this
to the oscar analytics app
'''

# class MailStats(models.Model):
# 	message_id = models.CharField(max_length=50, null=True)
# 	# user_id = models.fromeignKey(Users, on_delete=models.CASCADE)
# 	code = models.IntegerField(null=True)
# 	domain = models.CharField(max_length=50)
# 	event = models.CharField(max_length=50)
# 	recipient = models.EmailField()
# 	message_header = models.TextField()
# 	created_at = models.DateField(auto_now_add=True)
# 	type_mail = models.CharField(max_length=50)
# 	address = models.CharField(max_length=200, null=True)