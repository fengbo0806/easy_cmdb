from django.db import models

# Create your models here.
class Business(models.Model):
    '''the business is business,maybe it is more like project,but you know
    the work of maintance is always constant, adn have some leader's command
    task, so I create this for contant the needs above'''
    name=models.CharField(max_length=256)
    introduction=models.TextField(blank=True)
