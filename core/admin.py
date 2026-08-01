
from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from store.admin import ProductAdmin
from store.models import Product
from tags.models import Tag, TaggedItem
from .models import User
# Register your models here.

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'email'),
        }),
    )

class TagInline(GenericTabularInline):
  autocomplete_fields = ['tag']
  model = TaggedItem
  extra = 1

class CustomProductAdmin(ProductAdmin):
  inlines = [TagInline]

admin.site.unregister(Product)
admin.site.register(Product, CustomProductAdmin)