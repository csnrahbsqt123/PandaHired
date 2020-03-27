from django.contrib import admin

# Register your models here.
from apps.apply import models
admin.site.register(models.StoreAuthentication)
admin.site.register(models.CompanyHring)