from tracemalloc import is_tracing
from django.urls import reverse
from django.db import models
from category.models import Category
# Create your models here.

class Product(models.Model):
    product_name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(max_length=500)
    price = models.IntegerField()
    image = models.ImageField(upload_to='media/photos/product')
    stock = models.IntegerField(default=0)
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)


    def get_url(self):
        return reverse('product_detail', args=[self.category.slug,self.slug])

    def __str__(self):
        return self.product_name


# creating variations manager since _set.all fetches both color and size 
class VariationManager(models.Manager):
    def colors(self):
        return super(VariationManager, self).filter(variation_category = 'color', is_active = True)
    def sizes(self):
        return super(VariationManager, self).filter(variation_category = 'size', is_active = True)



# creating a tuple for the variations

variation_category_choice = (
    ('color', 'color'),
    ('size', 'size'),
)


class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation_category = models.CharField(max_length=200, choices=variation_category_choice)
    variation_value = models.CharField(max_length=100)
    is_active = models.BooleanField(default = True)
    created_date = models.DateTimeField(auto_now=True)

    objects = VariationManager()


    def __str__(self):
        return self.variation_value