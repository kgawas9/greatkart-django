from django.contrib import admin

from .models import Cart, CartItem

# Register your models here.

admin.site.register(Cart)

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'product', 'cart', 'quantity', 'is_active'
    )
