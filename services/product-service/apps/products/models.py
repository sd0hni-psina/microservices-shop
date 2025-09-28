from django.db import models
from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name


class Product(models.Model):
    
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    stock_quantity = models.PositiveIntegerField(default=0)
    image_url = models.URLField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name
    
    @property # property это декоратор, который позволяет обращаться к методу как к атрибуту
    def is_in_stock(self):
        return self.stock_quantity > 0
    
    def reserv_quantity(self, quantiity):
        """Резервирует указанное количество товара, если оно доступно."""
        if self.quantity >= quantiity:
            self.stock_quantity -= quantiity
            self.save()
            return True
        return False
    
    def release_quantity(self, quantiity):
        """Освобождает ранее зарезервированное количество товара."""
        self.stock_quantity += quantiity
        self.save()