from django.conf.urls import url

from oscar.core.application import DashboardApplication
from oscar.core.loading import get_class


class EmailApplication(DashboardApplication):
	name = 'email'

	default_permissions = ['is_staff', ]
	index_view = get_class('dashboard.mails.views', 'IndexView')

	def get_urls(self):
		urls = [
			url(r'^index/$', self.index_view.as_view(), name='index'),
		]
		return self.post_process_urls(urls)


application = EmailApplication()