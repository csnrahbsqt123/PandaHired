from django.db import models

# Create your models here.
class TestModel(models.Model):
    name=models.CharField(max_length=12,null=True,blank=True)
    status = models.CharField(max_length=6, choices=(("on", "招聘中"), ("stop", "暂停招聘"), ("full", "招满")), default="on")

    class Meta:
        db_table = 'test'