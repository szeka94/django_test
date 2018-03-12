from packjoy.apps.dashboard.mail import views

from oscar.test.factories import RequestFactory


class TestIndexView:
	'''
	Fix the FUCKING TESTS
	'''
	def test_anon_user_redirect(self):
		req = RequestFactory().get()
		resp = views.IndexView.as_view()(req)
		assert resp.status_code == 302, 'Should redirect to login page'
		assert 'login' in resp.url