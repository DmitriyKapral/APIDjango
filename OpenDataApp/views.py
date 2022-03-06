from tkinter.messagebox import NO
from turtle import pos
from typing import List
from unicodedata import category
from django.shortcuts import render
from django.db.models.query import QuerySet
import json
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from django.http import HttpResponse, JsonResponse, QueryDict
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
from rest_framework.decorators import api_view
from rest_framework import viewsets
from rest_framework.views import APIView
from .serializers import GeneralSerializer
from rest_framework import status
from .models import Address, Category, City, Contacts, Gallery, General, Image, Organization, Phones
from OpenDataApp import serializers
import requests
from requests.structures import CaseInsensitiveDict
from turfpy import measurement
from geojson import Point, Feature


headers = CaseInsensitiveDict()
headers["Accept"] = "application/json"
headers["X-API-KEY"] = "8bb73f27c25ad10e2ee76f800b6e1a9f63aa2ae6dea659e3288ddea6499186da"

class GeneralView(APIView):
    """serializer_class = GeneralSerializer
    model = General"""

    def get(self, request, format = None):
        """
        List all code snippets, or create a new snippet.
        """
        url = "https://nominatim.openstreetmap.org/reverse?format=json&lat=48.7784448&lon=44.777472"
        headers1 = CaseInsensitiveDict()
        headers1["Accept"] = "application/json"
        resp = requests.get(url)
        data = resp.json()
        return Response(data)

    '''@csrf_exempt
    def post(self, request, format = None):
        post_body = json.loads(request.body)
        body_category = post_body.get('category')
        general = General.objects.filter(category__name = body_category[1]['name'])
        for i in range(len(body_category)):
            if i == 0:
                general = General.objects.filter(category__name = body_category[i]['name'])
                query = general
            else:
                general = General.objects.filter(category__name = body_category[i]['name'])
                query = query.union(general)

           
            
        serializers = GeneralSerializer(query, many=True)
        #body_data = {
        #    'name': body_name,
        #    'one': one,
        #}
        print(serializers.data)
        return Response(serializers.data)'''

class GeneralListView(APIView):

    def get(self, request, pk, format = None):
        url = "https://nominatim.openstreetmap.org/reverse?format=jsonv2&lat=-34.44076&lon=-58.70521"

        resp = requests.get(url)
        data = resp.json()
        return(data)


class AllLibraryView(APIView):
    def get(self, request, format = None):
        url = "https://opendata.mkrf.ru/v2/libraries/$?l=10"

        resp = requests.get(url, headers=headers)
        data = resp.json()['data']
        return Response(data)


class AllCinemaView(APIView):
    def get(self, request, format = None):
        url = "https://opendata.mkrf.ru/v2/cinema/$?l=10"

        resp = requests.get(url, headers=headers)
        data = resp.json()['data']
        return Response(data)


class AllCircusesView(APIView):
    def get(self, request, format = None):
        url = "https://opendata.mkrf.ru/v2/circuses/$?l=10"

        resp = requests.get(url, headers=headers)
        data = resp.json()['data']
        return Response(data)

class AllConcertView(APIView):
    def get(self, request, format = None):
        url = "https://opendata.mkrf.ru/v2/concert_halls/$?l=10"

        resp = requests.get(url, headers=headers)
        data = resp.json()['data']
        return Response(data)


class AllMuseumsView(APIView):
    def get(self, request, format = None):
        url = "https://opendata.mkrf.ru/v2/museums/$?l=10"

        resp = requests.get(url, headers=headers)
        data = resp.json()['data']
        return Response(data)


class AllParksView(APIView):
    def get(self, request, format = None):
        url = "https://opendata.mkrf.ru/v2/parks/$?l=10"

        resp = requests.get(url, headers=headers)
        data = resp.json()['data']
        return Response(data)


class AllTheatersView(APIView):
    def get(self, request, format = None):
        url = "https://opendata.mkrf.ru/v2/theaters/$?l=10"

        resp = requests.get(url, headers=headers)
        data = resp.json()['data']
        return Response(data)


class GetCategoryView(APIView):
    def get(self, request, category = '', city = 'Москва', format = None):
        url = '''https://opendata.mkrf.ru/v2/'''+ category + '''/$?f={"data.general.locale.name":{"$search":"''' + city + '''"}}&l=10'''
        resp = requests.get(url, headers=headers)
        data = resp.json()['data']
        return Response(data)

    def post(self, request, category, city, format = None):
        post_body = json.loads(request.body)
        url = '''https://opendata.mkrf.ru/v2/'''+ category + '''/$?f={"data.general.locale.name":{"$search":"''' + city + '''"}}&l=100'''
        resp = requests.get(url, headers=headers)
        data = resp.json()['data']
        returnData = []
        userPoint = Feature(geometry=Point((post_body['lat'], post_body['long'])))
        for i in range(len(data)):
            objectPoint = Feature(geometry=Point((data[i]['data']['general']['address']['mapPosition']['coordinates'][1], data[i]['data']['general']['address']['mapPosition']['coordinates'][0])))
            if measurement.distance(userPoint, objectPoint)*1000 < post_body['radius']:
                returnData.append(data[i])
        return Response(returnData)

#ПОД ВОПРОСОМ!!!
class GetSearchObjectView(APIView):
    def get(self, request, category = '', city = 'Москва', search = '', format = None):
        url = '''https://opendata.mkrf.ru/v2/'''+ category +'''/$?f={"data.general.name":{"$contain":"''' + search + '''"},"data.general.locale.name":{"$search":"''' + city +'''"}}&l=10'''
        resp = requests.get(url, headers=headers)
        data = resp.json()['data']
        return Response(data)

class GetEventsView(APIView):
    def get(self, request, city = '', date = '', format = None):
        url = '''https://opendata.mkrf.ru/v2/events/$?f={"data.general.start":{"$gt":"''' + date + '''"},"data.general.organizerPlace.name":{"$search":"''' + city + '''"}}&l=1000'''
        resp = requests.get(url, headers=headers)
        data = resp.json()['data']
        return Response(data)
