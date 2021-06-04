from django.db import models
from django.contrib.postgres.fields import ArrayField


class Client(models.Model):
    name = models.CharField(max_length=200, blank=False)
    general_name = models.CharField(max_length=200, blank=True)
    date_from = models.DateTimeField(null=True)
    date_to = models.DateTimeField(null=True)
    tz = models.CharField(max_length=30)
    activated = models.BooleanField(null=False, default=False)
    status = models.BooleanField(null=False, default=True)


class Supplier(models.Model):
    supplier_code = models.CharField(max_length=50, null=True, blank=True)
    phone = models.CharField(max_length=25, blank=True, null=True)
    commodity_credit_days = models.IntegerField(default=0, blank=True)
    address = models.TextField(null=True, blank=True)
    identifier = models.CharField(max_length=100)
    name = models.CharField(max_length=200)
    api_updated = models.DateTimeField(auto_now=True)
    api_changed = models.BooleanField(default=True)


class Brand(models.Model):
    identifier = models.CharField(max_length=100)
    name = models.CharField(max_length=200)
    api_updated = models.DateTimeField(auto_now=True)
    api_changed = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Unit(models.Model):
    packed = models.BooleanField(null=False, default=True)
    pack_capacity = models.PositiveSmallIntegerField(null=False, default=1)
    identifier = models.CharField(max_length=100)
    name = models.CharField(max_length=200)
    api_updated = models.DateTimeField(auto_now=True)
    api_changed = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    hidden = models.BooleanField(null=False, default=False)
    parent_identifier = models.CharField(max_length=100, blank=True, null=True)
    parent = models.ForeignKey('self', null=True, on_delete=models.PROTECT)
    path = models.TextField(null=True)
    l = models.IntegerField(null=True)
    r = models.IntegerField(null=True)
    level = models.IntegerField(null=True)
    identifier = models.CharField(max_length=100)
    name = models.CharField(max_length=200)
    api_updated = models.DateTimeField(auto_now=True)
    api_changed = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    identifier = models.CharField(max_length=100)
    unit = models.ForeignKey(Unit, related_name="products", null=True, on_delete=models.PROTECT)
    category = models.ForeignKey(Category, related_name="products", null=True, on_delete=models.PROTECT)
    brand = models.ForeignKey(Brand, related_name="products", null=True, on_delete=models.PROTECT)
    producer = models.IntegerField(null=True)

    article = models.CharField(null=True, max_length=100)
    first_sale = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to="photo_products", null=True)
    barcode = models.TextField(blank=True, null=True)
    active = models.BooleanField(default=True)
    categories_list = ArrayField(models.IntegerField(), null=True)
    height = models.DecimalField(max_digits=20, decimal_places=4, null=True)
    width = models.DecimalField(max_digits=20, decimal_places=4, null=True)
    depth = models.DecimalField(max_digits=20, decimal_places=4, null=True)
    name = models.CharField(max_length=200)
    api_updated = models.DateTimeField(auto_now=True)
    api_changed = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id']


class Shop(models.Model):
    group = models.IntegerField(null=True)
    format = models.IntegerField(null=True)

    address = models.TextField(null=True)
    open_date = models.DateField(null=True)
    area = models.FloatField(null=True, blank=True, default=1)
    latitude = models.DecimalField(max_digits=10, decimal_places=8, null=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=8, null=True)
    identifier = models.CharField(max_length=100)
    name = models.CharField(max_length=200)
    api_updated = models.DateTimeField(auto_now=True)
    api_changed = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Sale(models.Model):
    client = models.ForeignKey(Client, on_delete=models.PROTECT)
    identifier = models.CharField(max_length=200, null=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=4, choices=(('edit', 'edit',), ('view', 'view',),), default='edit')
    shops = ArrayField(models.IntegerField(), null=True)
    date_from = models.DateField()
    date_to = models.DateField()
    user = models.IntegerField(null=True)
    sale_type = models.IntegerField(null=True)
    api_updated = models.DateTimeField(null=False, auto_now=True)
    api_changed = models.BooleanField(null=False, default=True)
    is_discount = models.BooleanField(null=False, default=False)


class SaleAccess(models.Model):
    client = models.ForeignKey(Client, null=False, on_delete=models.PROTECT)
    sale = models.ForeignKey(Sale, null=False, on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop, null=False, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, null=False, on_delete=models.PROTECT)

    api_updated = models.DateTimeField(null=False, auto_now=True)
    api_changed = models.BooleanField(null=False, default=True)

    class Meta:
        unique_together = ('client', 'sale', 'shop', 'product')


class Stock(models.Model):
    client = models.ForeignKey(Client, on_delete=models.PROTECT)
    dt = models.DateField()
    shop = models.ForeignKey(Shop, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    week_day = models.IntegerField(default=0)
    qty = models.DecimalField(decimal_places=4, max_digits=20)
    original_price = models.DecimalField(decimal_places=4, max_digits=20, default=0)
    stock_total_price = models.DecimalField(decimal_places=4, max_digits=20, default=0)
    api_updated = models.DateTimeField(null=False, auto_now=True)
    api_changed = models.BooleanField(null=False, default=True)

    class Meta:
        unique_together = ('client', 'dt', 'shop', 'product')
        index_together = ['client', 'shop', 'dt']


class Selling(models.Model):
    receipt_id = models.IntegerField(null=True)
    refund = models.IntegerField(null=True)
    order_id = models.IntegerField(null=True)
    shop = models.ForeignKey(Shop, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    date = models.DateField(blank=True, null=True)
    price = models.DecimalField(decimal_places=4, max_digits=20, default=0)
    original_price = models.DecimalField(decimal_places=4, max_digits=20, default=0)
    base_price = models.DecimalField(decimal_places=4, max_digits=20, default=0)
    qty = models.DecimalField(decimal_places=4, max_digits=20, default=0)
    total_price = models.DecimalField(decimal_places=4, max_digits=20, default=0)
    margin_price_total = models.DecimalField(decimal_places=4, max_digits=20, default=0)
    datetime = models.DateTimeField(null=True)
    datetime_open = models.DateTimeField(null=True)
    receipt_items_qty = models.DecimalField(decimal_places=4, max_digits=20, default=0)
    receipt_total_price = models.DecimalField(decimal_places=4, max_digits=20, default=0)
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT)
    total_vat = models.DecimalField(decimal_places=4, max_digits=20, default=0)
    total_excise = models.DecimalField(decimal_places=4, max_digits=20, default=0)









