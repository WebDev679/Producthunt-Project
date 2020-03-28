from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.

class Product(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField()
    image = models.ImageField(upload_to="images/")
    votes_total = models.IntegerField(default=1)
    pub_date = models.DateTimeField()
    icon = models.ImageField(upload_to="images/")
    url = models.TextField()
    hunter = models.ForeignKey(User, on_delete=models.CASCADE)


    def __str__(self):
        return self.title

    def summary(self):
            return self.body[:100]

    def pub_date_pretty(self):
        return self.pub_date.strf_time('%b, %e, %Y')

class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
