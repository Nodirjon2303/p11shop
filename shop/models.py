from django.contrib.auth.models import User
from django.db import models
from django.core.exceptions import ValidationError


class Category(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='category')
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=125, default='slug', unique=True)

    @property
    def image_url(self):
        if self.image:
            return self.image.url
        return ""

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=225)
    price = models.BigIntegerField()
    description = models.TextField()
    image = models.ImageField('products')

    @property
    def image_url(self):
        if self.image:
            return self.image.url
        else:
            return ''

    def __str__(self):
        return f"{self.category.name} ---> {self.name}"


class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    status_choice = (
        ('progress', "Sotuv davom etmoqda"),
        ('done', "Sotuv to'liq yakunlandi"),
    )
    status = models.CharField(max_length=125, choices=status_choice, default='progress')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer.username}"


def validate_savatcha_soni(value):
    if value > 5:
        raise ValidationError("Siz maxsimum 5 ta mahsulotni savatchaga qo'sha olasiz")
    if value < 1:
        raise ValidationError("Siz 1 tadan kam mahsulot kirita olmaysiz")
    return value


class Order_detail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, models.SET_NULL, null=True, blank=True)
    number_of_product = models.IntegerField(default=1, validators=[validate_savatcha_soni])

    @property
    def all_price(self):
        return self.product.price * self.number_of_product

    def save(self, *arg, **kwargs):
        super(Order_detail, self).save(*arg, **kwargs)
        if self.number_of_product > 5:
            raise ValidationError("Siz maxsimum 5 ta mahsulotni savatchaga qo'sha olasiz")
        if self.number_of_product < 1:
            raise ValidationError("Siz 1 tadan kam mahsulot kirita olmaysiz")

    def __str__(self):
        return f"{self.product.name}  {self.product.id}"
