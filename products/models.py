from django.db import models
import os
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=50, verbose_name="Title")
    image = models.ImageField(upload_to="categories/", verbose_name="Image")

    def delete(self, *args, **kwargs):
        # Delete the image file from the filesystem before deleting the object
        if self.image:
            if os.path.isfile(self.image.path):
                os.remove(self.image.path)

        super().delete(*args, **kwargs)

    def __str__(self) -> str:
        return self.title

class Product(models.Model):
    category = models.ForeignKey(Category, verbose_name="Category", on_delete=models.SET_NULL, null=True, help_text="Product will be shown on the website only, if category is specified.")
    title = models.CharField(max_length=200, verbose_name="Title")
    description = models.TextField(max_length=1000, verbose_name="Description")
    duration = models.TimeField(verbose_name="Duration")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price")

    def __str__(self) -> str:
        return f"{self.category} | {self.title}"


class ProductImage(models.Model):
    image = models.ImageField(upload_to="products/", verbose_name="Image")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Product", related_name="images")

    def delete(self, *args, **kwargs):
        # Delete the image file from the filesystem before deleting the object
        if self.image:
            if os.path.isfile(self.image.path):
                os.remove(self.image.path)

        super().delete(*args, **kwargs)

    def __str__(self) -> str:
        return self.product.title
    

class Review(models.Model):
    product = models.ForeignKey(Product, verbose_name="Product", on_delete=models.CASCADE)
    name = models.CharField(max_length=50, verbose_name="Name")
    text = models.TextField(max_length=500, verbose_name="Text")
    date = models.DateField(auto_now_add=True, verbose_name="Date")
    mark = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ],
        verbose_name="Mark"
    )

    def __str__(self) -> str:
        return f"{self.name} - {self.mark}/5"