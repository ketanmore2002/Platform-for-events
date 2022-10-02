from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(host)
admin.site.register(events)
admin.site.register(teams)
admin.site.register(player)


