from django.conf import settings
from django.views import generic
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.template.loader import render_to_string

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
		form = self.form(request.POST)
		if form.is_valid():
			self.handle_mail_list_sending(data=form.data)
			# if form.data.get('is_email_list') == '2':
				# should send bulk emails to the email list provided
			return redirect('dashboard:index')

	def handle_mail_list_sending(self, data):
		'''
		This method is responsible to send the
		api request to the mailgun, to send
		bulk emails to the given email address
		'''
		template_path = self.html_email_template.format(data['campaign_type'])
		template = render_to_string(template_path)
		sl_fallback = 'This is a test subject line.'
		recipients = []
		if data.get('is_email_list') == '2':
			# should send bulk emails to the email list provided
			print('Not implemented')
		else:
			recipients.append(data.get('recipient'))
		send_mail(
			subject=data.get('subject_line', sl_fallback),
			message =template,
			html_message=template,
			from_email=settings.OSCAR_FROM_EMAIL,
			recipient_list=recipients,
		)

