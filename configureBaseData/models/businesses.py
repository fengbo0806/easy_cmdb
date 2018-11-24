from django.db import models


# Create your models here.
class Business(models.Model):
    '''the business is business,maybe it is more like project,but you know
    the work of maintance is always constant, adn have some leader's command
    task, so I create this for contant the needs above'''
    name = models.CharField(max_length=255)
    introduction = models.TextField(blank=True, null=True)

    def __str__(self):
        return str(self.name)


class Projects(models.Model):
    '''
    progects are start from inside,and may have many business
    '''
    name = models.CharField(max_length=255)
    introduction = models.TextField(blank=True, null=True)
    typeOfBusiness = models.ManyToManyField('Business', blank=True, null=True)

    def __str__(self):
        return str(self.name)
