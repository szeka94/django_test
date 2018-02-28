from django.shortcuts import render
from django.http import HttpResponse
from django.views import View


class IndexView(View):
	def get(self, request):
		return render(template_name='mail_templates/index.html', context={'message': 'hello'}, request=request)


class DetailView(View):
	def get(self, request, slug):
		template_name = 'mail_templates/{}.html'.format(slug)
		return render(request, template_name=template_name)
