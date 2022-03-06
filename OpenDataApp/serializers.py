from unicodedata import category
from attr import field
from rest_framework import serializers

from .models import Address, Category, City, Contacts, Gallery, General, Image, Organization, Phones


class AddressSerialize(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'

class CategorySerialize(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class CitySerialize(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'


class ContactsSerialize(serializers.ModelSerializer):
    class Meta:
        model = Contacts
        fields = '__all__'

class ImageSerialize(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'

class OrganizationSerialize(serializers.ModelSerializer):
    address = AddressSerialize(many=False, read_only = True)
    city = CitySerialize(many=False, read_only = True)
    class Meta:
        model = Organization
        fields = '__all__'

class PhonesSerialize(serializers.ModelSerializer):
    class Meta:
        model = Phones
        fields = '__all__'


class GeneralSerializer(serializers.ModelSerializer):
    category = CategorySerialize(many=False, read_only = True)
    organization = OrganizationSerialize(many=False, read_only = True)
    address = AddressSerialize(many=False, read_only = True)
    city = CitySerialize(many=False, read_only = True)
    image = ImageSerialize(many=False, read_only=True)
    contacts = ContactsSerialize(many=False, read_only=True)
    
    class Meta:
        model = General
        fields = '__all__'

class GallerySerializer(serializers.ModelSerializer):
    general = GeneralSerializer(many=False, read_only = True)
    class Meta:
        model = Gallery
        fields = '__all__'
