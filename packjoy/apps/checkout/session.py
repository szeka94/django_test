from django.urls import reverse
from django.conf import settings
from django.utils.translation import ugettext as _

from oscar.apps.checkout.exceptions import FailedPreCondition
from oscar.apps.checkout.session import CheckoutSessionMixin as OscarCheckoutSessionMixin

from . import tax


class CheckoutSessionMixin(OscarCheckoutSessionMixin):
	'''
	TODO: I'm not sure if this is the best place for this kind of logic
	DO SOME RESEARCH because you might want to move this to the partner
	app, somewhere you can overwrite the avability policty method of the
	Strategy Class
	'''

	def check_basket_is_valid(self, request):
		messages = []
		try:
			super(CheckoutSessionMixin, self).check_basket_is_valid(request)
		except FailedPreCondition as e:
			messages += e.messages
		for line in request.basket.all_lines():
			if line.quantity < int(settings.MINIMUM_ORDER_QUANTITY):
				messages.append(_('Cantitate minimuma este {} bucati.'
									.format(settings.MINIMUM_ORDER_QUANTITY)))
		if messages:
			raise FailedPreCondition(url=reverse('basket:summary'), messages=messages)

	def build_submission(self, **kwargs):
		'''
		we need to overwrite the price_incl_tax attribute to 
		continue checkout at this point
		'''
		# REFACTOR THIS SHIT, THIS IS NOT HOW IT SUPPOSED TO WORK

		submission = super(CheckoutSessionMixin, self).build_submission(**kwargs)
		if submission['shipping_address']:
			tax.apply_to(submission)
			submission['order_total'] = self.get_order_totals(
					submission['basket'],
					shipping_charge=submission['shipping_method'])
		return submission
