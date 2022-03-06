from csv import list_dialects
from django.contrib import admin
from .models import Address, Category, City, Contacts, Gallery, General, Image, Organization, Phones

# Register your models here.

class AddressAdmin(admin.ModelAdmin):
    list_display = ('street', 'fulladdress', 'mappositionX', 'mappositionY')

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

class CityAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

class ContactsAdmin(admin.ModelAdmin):
    list_display = ('website', 'email')

class ImageAdmin(admin.ModelAdmin):
    list_display = ('url', 'title')

class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'inn', 'type', 'address', 'city')

class PhonesAdmin(admin.ModelAdmin):
    list_display = ('value', 'comment', 'contact')

class GeneralAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'category', 'organization', 'contacts', 'address', 'city', 'image')

class GalleryAdmin(admin.ModelAdmin):
    list_display = ('url', 'title', 'general')


admin.site.register(Address, AddressAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(Contacts, ContactsAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(Organization, OrganizationAdmin)
admin.site.register(Phones, PhonesAdmin)
admin.site.register(General, GeneralAdmin)
admin.site.register(Gallery, GalleryAdmin)