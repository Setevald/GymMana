from django.contrib import admin
from .models import *
from . import models

# Register your models here.
class BannerAdmin(admin.ModelAdmin):
	list_display=('alt_text','image_tag')
admin.site.register(models.Banners,BannerAdmin)

admin.site.register(User)
admin.site.register(Membership)
admin.site.register(Promotional)
admin.site.register(Transaction)
admin.site.register(Equipment)
admin.site.register(Maintenance)
admin.site.register(Trainer)
admin.site.register(Classes)
admin.site.register(TransactionDetail)