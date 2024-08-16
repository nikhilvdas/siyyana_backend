from django.db import models

# Create your models here.


class Country(models.Model):
    name = models.CharField(max_length=100)
    class Meta:
        verbose_name_plural = "COUNTRIES"
    def __str__(self):
        return self.name
    

class State(models.Model):
    name = models.CharField(max_length=100)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    class Meta:
        verbose_name_plural = "STATE"
    def __str__(self):
        return self.name


class District(models.Model):
    name = models.CharField(max_length=100)
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    class Meta:
        verbose_name_plural = "DISTRICTS"
    def __str__(self):
        return self.name




class Category(models.Model):
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='category')
    class Meta:
        verbose_name_plural = "CATEGORY"
    def __str__(self):
        return self.name



class SubCategory(models.Model):
    name = models.CharField(max_length=100)
    service = models.ForeignKey(Category, on_delete=models.CASCADE)
    class Meta:
        verbose_name_plural = "SUBCATEGORY"
    def __str__(self):
        return self.name
