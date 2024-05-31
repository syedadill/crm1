from django.contrib import admin

from .models import *

admin.site.register(Projects)
admin.site.register(Tasks)
admin.site.register(Tags)
admin.site.register(Status)
# Register your models here.
