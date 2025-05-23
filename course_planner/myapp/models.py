from django.db import models

# Create your models here.
class Course(models.Model) :
    subject = models.CharField(max_length=4)
    code = models.IntegerField(min=100, max=699)
    name = models.CharField(max_length=100)
    credits = models.PositiveSmallIntegerField
    cdf = models.BooleanField     #credit/d/failing available?
    desc = models.TextField
    prereqs = models.ManyToManyField("self", symmetrical=False)




