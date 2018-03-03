from oscar.apps.analytics.models import *  # noqa isort:skip

from django.db import models
from django.utils.translation import ugettext_lazy as _


class EmailRecord(models.Model):
	event = models.CharField(_('Triggered Event'), max_length=50)
	recipient = models.EmailField(_('Recipient of the Email'))
	domain = models.CharField(_('Sender domain'), max_length=50)
	ip = models.GenericIPAddressField(_('Recipients IP address'))
	address = models.CharField(_('Recipients Address'), null=True, max_length=256)
	mailing_list = models.CharField(_('Used Mailing List'), null=True, max_length=128)
	user_agent = models.CharField(_('User Agent of the Recipient'), null=True, max_length=512)
	created_at = models.DateField(_('Date Created'), auto_now_add=True)

	def __str__(self):
		return 'Email Record {}'.format(self.recipient)

	class Meta:
		app_label = 'analytics'
		verbose_name = 'Email Stat'
		verbose_name_plural = 'Emails Statistics'