from django.contrib import admin

# Register your models here.
from . import models


admin.site.register(models.Movie)
admin.site.register(models.Account)
admin.site.register(models.Session)
admin.site.register(models.Group)
