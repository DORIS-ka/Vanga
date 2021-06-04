from django.contrib import admin

from predict.models import Product, Shop, Category, Brand, Client, Supplier, Selling, Stock


@admin.register(Brand)
class BrandModelAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Category)
class CategoryModelAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Client)
class ClientModelAdmin(admin.ModelAdmin):
    list_display = ("name", "tz", "date_from", "date_to", "status")
    search_fields = ("name",)


@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "brand", "active", "barcode")
    search_fields = ("name", "barcode")


@admin.register(Selling)
class SellingModelAdmin(admin.ModelAdmin):
    list_display = ("product", "qty", "original_price", "shop")
    search_fields = ("product",)


@admin.register(Shop)
class ShopModelAdmin(admin.ModelAdmin):
    list_display = ("name", "address")
    search_fields = ("name",)


@admin.register(Supplier)
class SupplierModelAdmin(admin.ModelAdmin):
    list_display = ("name", "address", "phone")
    search_fields = ("name", "phone")


@admin.register(Stock)
class StockModelAdmin(admin.ModelAdmin):
    list_display = ("product", "qty", "original_price", "shop")
    search_fields = ("product",)
