from django.contrib import admin

# Register your models here.
from apps.apply import models

admin.site.register(models.UserProfile)
admin.site.register(models.SkillLabel)
admin.site.register(models.Resume)
admin.site.register(models.WorkExperience)
admin.site.register(models.Position)