from django.conf import settings
from django.views import generic
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.template.loader import render_to_string

# for some reason this isn't working
# I have to import the Product model directly
# from the oscar libary
# from oscar.core.loading import get_model
from oscar.apps.catalogue.models import Product

from .forms import EmailSenderForm


class IndexView(generic.View):
	template_name = 'dashboard/mails/index.html'
	form  = EmailSenderForm
	html_email_template = 'mail_templates/{}.html'

	def get(self, request, *args, **kwargs):
		context=dict(form=self.form)
		return render(request, self.template_name, context)

	def post(self, request, *args, **kwargs):
		'''
		this method handles the form submission
		and should send a test email to the given address
		or send bulk emails to the given mailing list
		'''
		# import ipdb; ipdb.set_trace()
		form = self.form(request.POST)
		if form.is_valid():
			product_ids = [value for key, value in request.POST.items() if 'product_' in key]
			product_ids = [product_id for product_id in product_ids if product_id]
			products = self._get_products(product_ids=product_ids)
			campaign_type = form.data['campaign_type']
			template = self.get_template_with_context(campaign_type=campaign_type,
													products=products)
			recipients = form.data['recipient'].split(',')
			self.handle_mail_list_sending(subject=form.data['subject_line'], template=template, 
										  recipients=recipients)
			return redirect('dashboard:index')

	@staticmethod
	def handle_mail_list_sending(subject=None, recipients=[], template=None):
		'''
		This method is responsible to send the
		api request to the mailgun, to send
		bulk emails to the given email address
		'''
		send_mail(
			subject=subject,
			message =template,
			html_message=template,
			from_email=settings.OSCAR_FROM_EMAIL,
			recipient_list=recipients,
		)

	@staticmethod
	def _get_products(product_ids):
		'''
		it returns Product Objects based
		on a list of ids
		'''
		products = list(Product.objects.filter(id__in=product_ids))
		return products

	def get_template_with_context(self, campaign_type, products):
		'''
		this method saves the prepares the template
		for emails
		'''
		template_path = template_path = self.html_email_template.format(campaign_type)
		template = render_to_string(template_path, {'products': products})
		return template
