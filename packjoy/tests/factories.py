import factory
from decimal import Decimal as D

from oscar.core.loading import get_model
from oscar.core.compat import get_user_model

Product = get_model('catalogue', 'Product')
ProductClass = get_model('catalogue', 'ProductClass')
Partner = get_model('partner', 'Partner')
Category = get_model('catalogue', 'Category')
ProductCategory = get_model('catalogue', 'ProductCategory')
StockRecord = get_model('partner', 'StockRecord')
User = get_user_model()


class ProductClassFactory(factory.DjangoModelFactory):

    class Meta:
        model = ProductClass

    requires_shipping = True
    name = 'Cigarette Packs'
    track_stock = True


class PartnerFactory(factory.DjangoModelFactory):

    class Meta:
        model = Partner

    name = 'default_partner'


class CategoryFactory(factory.DjangoModelFactory):

    class Meta:
        model = Category

    name = factory.Sequence(lambda n: 'Category_%d' % n)
    depth = 0
    path = factory.Sequence(lambda n: '000%d' % n)


class ProductCategoryFactory(factory.DjangoModelFactory):

    class Meta:
        model = ProductCategory

    category = factory.RelatedFactory(CategoryFactory)


class StockRecordFactory(factory.DjangoModelFactory):

    class Meta:
        model = StockRecord

    partner = factory.SubFactory(PartnerFactory)
    partner_sku = factory.Sequence(lambda n: '19830302%d' % n)
    price_currency = 'USD'
    price_excl_tax = D('1000.0')
    num_in_stock = 0


class ProductFactory(factory.DjangoModelFactory):

    class Meta:
        model = Product

    structure = Meta.model.STANDALONE
    # reference = factory.Sequence(lambda n: '19830302%d' % n)
    title = factory.Sequence(lambda n: 'product_%d' % n)
    product_class = factory.SubFactory(ProductClassFactory)
    stockrecords = factory.RelatedFactory(StockRecordFactory, 'product')

    @factory.post_generation
    def categories(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for category in extracted:
                self.categories.add(category)


class UserFactory(factory.DjangoModelFactory):

    class Meta:
        model = User

    email = factory.Sequence(lambda n: 'packjoy_customer_%d@gmail.com' % n)
    username = email
    first_name = 'test'
    last_name = 'user'
    password = factory.PostGenerationMethodCall('set_password', 'password')
    is_active = True
    is_superuser = False
    is_staff = False
















