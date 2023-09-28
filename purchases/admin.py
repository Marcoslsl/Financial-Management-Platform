from django.contrib import admin
from .models import Purchase


# Register your models here.
class PurchaseAdmin(admin.ModelAdmin):
    fields = [
        "name",
        "category",
        "price",
        "credit_card",
        "day_to_receive_the_analysis",
        "description",
        "data_of_purchase",
        "created_at",
        "updated_at",
    ]


admin.site.register(Purchase, PurchaseAdmin)
