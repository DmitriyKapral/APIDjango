from http.client import responses
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
from datetime import date


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


class GetCategoryView(APIView):
    def parsingData(self, category, city):
        url = '''https://opendata.mkrf.ru/v2/'''+ category + '''/$?f={"data.general.locale.name":{"$search":"''' + city + '''"}}&l=100'''
        resp = requests.get(url, headers=headers)
        return resp.json()['data']

    def get(self, request, category = '', city = 'Москва', format = None):
        data = self.parsingData(category, city)
        return Response(data)

    def post(self, request, category, city, format = None):
        post_body = json.loads(request.body)
        data = self.parsingData(category, city)
        returnData = []
        userPoint = Feature(geometry=Point((post_body['lat'], post_body['long'])))
        for i in range(len(data)):
            objectPoint = Feature(geometry=Point((data[i]['data']['general']['address']['mapPosition']['coordinates'][1], 
            data[i]['data']['general']['address']['mapPosition']['coordinates'][0])))
            if measurement.distance(userPoint, objectPoint)*1000 < int(post_body['radius']):
                returnData.append(data[i])
        return Response(returnData)

#ПОД ВОПРОСОМ!!!
class GetSearchObjectView(APIView):
    def get(self, request, category = '', city = 'Москва', search = '', format = None):
        url = '''https://opendata.mkrf.ru/v2/'''+ category +'''/$?f={"data.general.name":{"$contain":"''' + search + '''"},
        "data.general.locale.name":{"$search":"''' + city +'''"}}&l=10'''
        resp = requests.get(url, headers=headers)
        data = resp.json()['data']
        return Response(data)

#НЕПРАВИЛЬНО(не всё возвращает)
"""class GetEventsView(APIView):
    def get(self, request, city = '', date = '', format = None):
        url = '''https://opendata.mkrf.ru/v2/events/$?f={"data.general.start":{"$gt":"''' + date + '''"},"data.general.organizerPlace.name":{"$search":"''' + city + '''"}}&l=1000'''
        resp = requests.get(url, headers=headers)
        data = resp.json()['data']
        return Response(data)

    def post(self, request, city = '', date = '', format = None):
        post_body = json.loads(request.body)
        url = '''https://opendata.mkrf.ru/v2/events/$?f={"data.general.ageRestriction":{"$gte":"''' + str(post_body['age']) + '''"},"data.general.start":{"$gt":"''' + date + '''"},"data.general.organizerPlace.name":{"$search":"''' + city + '''"}}&l=1000'''
        resp = requests.get(url, headers=headers)
        data = resp.json()['data']
        returnData = []
        for i in range(len(data)):
            for j in range(len(post_body['category'])):
                if(data[i]['data']['general']['category']['name'] == post_body['category'][j]['name']):
                    returnData.append(data[i])
        return Response(returnData)"""

#Тестовый класс выдачи мероприятий по организациям Волгограда
class TestGetEventsView(APIView):
    def get(self, request, format = None):
        url = '''https://opendata.mkrf.ru/v2/cinema/$?f={"data.general.locale.name":{"$search":"Волгоград"}}&l=100'''
        resp = requests.get(url, headers=headers)
        data = resp.json()['data']
        returndata = []
        for i in range(len(data)):
            url = '''https://opendata.mkrf.ru/v2/events/$?f={"data.general.start":{"$gt":"2022-03-09"},"data.general.organization.id":{"$eq":"
            ''' + str(data[i]['data']['general']['organization']['id']) + '''"}}&l=100'''
            resp = requests.get(url, headers=headers)
            returndata.extend(resp.json()['data'])
        return Response(returndata)


#Работа с данными мероприятий, доделать цикл на поиск городов, когда несколько точек проведения события
class GetEventsView(APIView):
    def parsingData(self, category, city):
        url = '''https://opendata.mkrf.ru/v2/'''+ category + '''/$?f={"data.general.locale.name":{"$search":"''' + city + '''"}}&l=100'''
        resp = requests.get(url, headers=headers)
        return resp.json()['data']

    def parsingEvent(self, datetime, id, ageRestriction = 0, isFree = 2, category = ''):
        if isFree >=2:
            isFreeString = ""
        elif isFree == 1:
            isFreeString = '''"data.general.isFree":{"$eq":"1"},'''
        else:
            isFreeString = '''"data.general.isFree":{"$eq":"0"},'''

        if not category:
            categoryString = ""
        else:
            categoryString = '''"data.general.category.name":{"$search":"''' + category + '''"},'''

        #url = '''https://opendata.mkrf.ru/v2/events/$?f={"data.general.start":{"$gt":"''' + str(datetime) + '''"},"data.general.organization.id":{"$eq":"''' + str(id) + '''"}}&l=100'''
        url = '''https://opendata.mkrf.ru/v2/events/$?f={"data.general.ageRestriction":{"$gte":"'''+ str(ageRestriction) +'''"},''' + isFreeString + '''
        "data.general.start":{"$gt":"''' + str(datetime) + '''"},''' + categoryString + '''"data.general.organization.id":{"$eq":"''' + str(id) + '''"}}&l=100'''
        
        resp = requests.get(url, headers=headers)
        return resp.json()['data']
    
    def get(self, request, category = '', city = '', format = None):
        data = self.parsingData(category, city)
        returndata = []
        current_datetime = date.today()
        for i in range(len(data)):
            returndata.extend(self.parsingEvent(current_datetime, data[i]['data']['general']['organization']['id']))
        return Response(returndata)

    def post(self, request, category = '', city = '', format = None):
        post_body = json.loads(request.body)
        data = self.parsingData(category, city)
        returndata = []
        current_datetime = date.today()
        for i in range(len(data)):
            for j in range(len(post_body['category'])):
                returndata.extend(self.parsingEvent(current_datetime, data[i]['data']['general']['organization']['id'], post_body['ageRestriction'], 
                post_body['isFree'], post_body['category'][j]['name']))
        return Response(returndata)