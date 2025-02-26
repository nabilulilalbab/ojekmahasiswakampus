from django.contrib import admin
from .models import Order, Tag,Voucher,Event, BannerEvent
# Register your models here.
admin.site.register(Order)
admin.site.register(Tag)
admin.site.register(Voucher)
admin.site.register(Event)
admin.site.register(BannerEvent)
