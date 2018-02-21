from django.conf.urls import url

from oscar.core.application import Application
from oscar.core.loading import get_class


class AnalyticsApplication(Application):
    name='analytics'
    email_analytics = get_class('analytics.views', 'EmailAnalytics')

    def get_urls(self):
        urls = [
            # url(r'^email-analytics/add/(?P<type>[-\w]+)/$', self.email_analytics.as_view(), name='email-analytics'),
            url(r'^email-analytics/$', self.email_analytics.as_view(), name='email-analytics'),
        ]

        return self.post_process_urls(urls)


application = AnalyticsApplication()