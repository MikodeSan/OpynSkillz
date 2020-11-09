from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from .models import ZPath, ZContentSource, ZContent

admin.site.register(ZPath, MPTTModelAdmin)
admin.site.register(ZContentSource)
admin.site.register(ZContent)
