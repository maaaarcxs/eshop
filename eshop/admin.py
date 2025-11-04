from django.contrib import admin
from .models import Item, Category, Brand


class BrandAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    fieldsets = (
        ("Основная информация", {
            "fields": ("name",)
        }),
    )


class ItemAdmin(admin.ModelAdmin):
    list_display = ("brand", "model", "price", "stock", "category")
    list_editable = ("stock",)
    list_filter = ("category", "stock", "price")
    search_fields = ("model", "brand__name")
    ordering = ("-price",)
    fieldsets = (
        ("Основная информация", {
            "fields": ("photo", "brand", "model", "price", "stock", "category", "description")
        }),
    )
    

class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    fieldsets = (
        ("Основная информация", {
            "fields": ("name",)
        }),
    )
    

admin.site.register(Item, ItemAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Brand, BrandAdmin)