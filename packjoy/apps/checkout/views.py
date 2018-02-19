import pprint
import hashlib
from decimal import Decimal as D

from django import http
from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect, render
from django.utils.translation import ugettext as _
from django.shortcuts import render
from django.views import generic
from django.core.urlresolvers import reverse_lazy, reverse
from django.core.mail import send_mail

from oscar.apps.checkout.views import ShippingMethodView as OscarShippingMethodView, \
                                        PaymentDetailsView as OscarPaymentDetailsView, \
                                        ShippingAddressView as OscarShippingAddressView
from oscar.apps.payment.exceptions import PaymentError
from oscar.apps.payment import models
from oscar.apps.checkout.mixins import OrderPlacementMixin
from oscar.core.loading import get_class, get_model
from oscar.core.compat import user_is_authenticated
from oscar.core import prices

from . import tax


BillingAddressForm = get_class('checkout.forms', 'BillingAddressForm')
CheckoutSessionMixin = get_class('checkout.session', 'CheckoutSessionMixin')
UserAddress = get_model('address', 'UserAddress')
Basket = get_model('basket', 'Basket')

pp = pprint.PrettyPrinter(indent=4)


class ShippingAddressView(OscarShippingAddressView):
    '''
    Overwriting the form_valid method to save the shipping address
    to the users address fields
    '''
    def form_valid(self, form):
        # Store the address details in the session and redirect to next step
        address_fields = dict(
            (k, v) for (k, v) in form.instance.__dict__.items()
            if not k.startswith('_'))
        self.checkout_session.ship_to_new_address(address_fields)
        form.save()
        return super(ShippingAddressView, self).form_valid(form)
    



class ShippingMethodView(OscarShippingMethodView):

    def get_success_response(self):
        '''
        Overriding the default behaviour in order
        to skip the `select payment-method` view
        and go directly to the pre
        '''
        return redirect('checkout:payment-method')



class PaymentMethodView(CheckoutSessionMixin, generic.FormView):
    """
    View for a user to choose which payment method(s) they want to use.
    This would include setting allocations if payment is to be split
    between multiple sources. It's not the place for entering sensitive details
    like bankcard numbers though - that belongs on the payment details view.
    """
    '''
    Since in this moment we only have one payment method this is Overwritten
    to get the users billing address
    '''

    template_name = 'checkout/billing_address.html'
    success_url = reverse_lazy('checkout:preview')
    form_class = BillingAddressForm
    pre_conditions = [
        'check_basket_is_not_empty',
        'check_basket_is_valid',
        'check_user_email_is_captured',
        'check_shipping_data_is_captured']
    skip_conditions = ['skip_unless_payment_is_required']

    def get_context_data(self, **kwargs):
        ctx = super(PaymentMethodView, self).get_context_data(**kwargs)
        if user_is_authenticated(self.request.user):
            ctx['addresses'] = self.get_available_addresses()
        return ctx

    def get_available_addresses(self):
        return self.request.user.addresses.filter(
            country__is_shipping_country=True).order_by(
            '-is_default_for_shipping')

    def post(self, request, *args, **kwargs):
        if user_is_authenticated(self.request.user) and \
            'address_id' in self.request.POST:
            address = UserAddress._default_manager.get(
                pk=self.request.POST['address_id'], user=self.request.user)
            action = self.request.POST.get('action', None)
            if action == 'set_to_billing':
                self.checkout_session.bill_to_user_address(address=address)
                return redirect(self.get_success_url())
            else:
                return http.HttpResponseBadRequest()
        else:
            return super(PaymentMethodView, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        # Store the address details in the session and redirect to next step
        address_fields = dict(
            (k, v) for (k, v) in form.instance.__dict__.items()
            if not k.startswith('_'))
        self.checkout_session.bill_to_new_address(address_fields=address_fields)
        form.save()
        return super(PaymentMethodView, self).form_valid(form)


class PaymentDetailsView(OscarPaymentDetailsView):

    def get_context_data(self, **kwargs):
        context = super(PaymentDetailsView, self).get_context_data(**kwargs)
        context['submit'] = self.collect_submit_data()
        return context

    @staticmethod
    def collect_submit_data():
        submit = {
            'url' : settings.CHECKOUT_SUBMIT_URL,
            'account_number' : settings.CHECKOUT_ACCOUNT_NUMBER,
        }
        return submit

    def post(self, request, *args, **kwargs):
        # action_param = request.GET.get('action', None)
        # if action_param is not None:
        #     try:
        #         self.handle_place_order_submission(action=action_param, params=request.GET)
        #     except PaymentError:
        #         messages.error(self.request, _('''Something went wrong during your card processing.
        #                 #                                         Please Try again, if the problem persist please,
        #                 #                                          contact our server administrator.'''))
        send_mail(
            'New order has created - fuckers',
            'Valaki csinalt egy rendelest, lepj fel a dasboardra tobb infoert. MOOST.',
            settings.OSCAR_FROM_EMAIL,
            settings.ADMIN_MAIL_ADDRESSES,
        )
        self.handle_place_order_submission()
        return redirect('checkout:thank-you')
        #
        #     pass
        # else:
        #

    def handle_place_order_submission(self, **kwargs):
        """
        Handle a request to place an order.
        This method is normally called after the customer has clicked "place
        order" on the preview page. It's responsible for (re-)validating any
        form information then building the submission dict to pass to the
        `submit` method.
        If forms are submitted on your payment details view, you should
        override this method to ensure they are valid before extracting their
        data into the submission dict and passing it onto `submit`.
        """
        # action, resp = kwargs.get('action'), kwargs.get('params')

        # if action == 'place_order':
        #     if not self.is_valid_payment_response(resp=resp):
        #         # The card payment wasn't successfull
        #         raise PaymentError('The payment wasn\'t successfull')
        return self.submit(**self.build_submission())

    def build_submission(self, **kwargs):
        submission = super(CheckoutSessionMixin, self).build_submission(**kwargs)
        submission = tax.apply_to(submission)
        # import ipdb; ipdb.set_trace()
        submission['order_total'] = self.get_order_totals(
            submission['basket'],
            submission['shipping_charge'])

        return submission


    # @staticmethod
    # def is_valid_payment_response(resp):
    #     # Changes made here -> didn't test yet, but should be working
    #     order_number = resp['order_number']
    #     total = resp['total']
    #     key = resp['key']
    #     new_key = hashlib.md5()
    #     new_key.update(settings.CHECKOUT_SECRET_KEY.encode('utf8'))
    #     new_key.update(settings.CHECKOUT_ACCOUNT_NUMBER.encode('utf8'))
    #     new_key.update(order_number.encode('utf8'))
    #     new_key.update(total.encode('utf8'))
    #     check_hash = new_key.hexdigest()
    #     check_hash = check_hash.upper()
    #     return key == check_hash

    def handle_payment(self, order_number, order_total, **payment_kwargs):
        '''
        At this point the payment should be successfull
        and we just handle the payment on the
        oscar level.
        :param order_number: This is the Order number from, generated by oscar
        :param order_total: total amount paid by the user
        '''
        '''
        since we are not supporting bankcard payment yet,
        the only source is cash on delivery
        '''
        source_type, is_created = models.SourceType.objects.get_or_create(
            name='Cash On Delivery')
        source = source_type.sources.model(
            source_type=source_type,
            amount_allocated=order_total.incl_tax, currency=order_total.currency)
        self.add_payment_source(source)
        self.add_payment_event('Authorised', order_total.incl_tax)
