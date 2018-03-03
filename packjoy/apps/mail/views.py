from django.shortcuts import render
from django.http import HttpResponse
from django.views import View

# for some reason this isn't working
# I have to import the Product model directly
# from the oscar libary
# from oscar.core.loading import get_model
from oscar.apps.catalogue.models import Product



class IndexView(View):
	def get(self, request):
		return render(template_name='mail_templates/index.html', context={'message': 'hello'}, request=request)


class DetailView(View):
	template_name = 'mail_templates/{}.html'

	def get(self, request, slug):
		products = self.get_products()
		context = dict(products=products)
		return render(request, template_name=self.template_name.format(slug),
								context=context)

	@staticmethod
	def get_products():
		products = Product.objects.all()[:6]
		return products
