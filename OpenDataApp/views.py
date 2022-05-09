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
from rest_framework import status
import requests
from requests.structures import CaseInsensitiveDict
from turfpy import measurement
from geojson import Point, Feature
from datetime import date, datetime, timedelta
from dateutil import parser


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

class GeneralListView(APIView):

    def get(self, request, pk, format = None):
        url = "https://nominatim.openstreetmap.org/reverse?format=jsonv2&lat=-34.44076&lon=-58.70521"

        resp = requests.get(url)
        data = resp.json()
        return(data)


class GetCategoryView(APIView):
    def parsingData(self, category, city):
        url = '''https://opendata.mkrf.ru/v2/'''+ category + '''/$?f={"data.general.locale.name":{"$eq":"''' + city + '''"}}&l=1000'''
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

#Тестовый класс выдачи мероприятий по организациям Волгограда
class TestGetEventsView(APIView):
    def get(self, request, format = None):
        url = '''https://opendata.mkrf.ru/v2/museums/$?f={"data.general.locale.name":{"$search":"Волгоград"}}&l=100'''
        resp = requests.get(url, headers=headers)
        data = resp.json()['data']
        returndata = []
        for i in range(len(data)):
            url = '''https://opendata.mkrf.ru/v2/events/$?f={"data.general.start":{"$gt":"2022-03-09"},"data.general.organization.id":{"$eq":"''' + str(data[i]['data']['general']['organization']['id']) + '''"}}&l=100'''
            resp = requests.get(url, headers=headers)
            returndata.extend(resp.json()['data'])
        return Response(returndata)


#Работа с данными мероприятий, доделать цикл на поиск городов, когда несколько точек проведения события
class GetEventsView(APIView):
    def get(self, request, city = '', format = None):
        # data = self.parsingData(category, city)
        # returndata = []
        current_datetime = datetime.now()
        # for i in range(len(data)):
        #     returndata.extend(self.parsingEvent(current_datetime, data[i]['data']['general']['organization']['id']))
        url = '''https://opendata.mkrf.ru/v2/events/$?f={"data.general.end":{"$gt":"''' + str(current_datetime) + '''"},"data.general.places[].locale.name":{"$eq":"''' + city + '''"}}&l=1000'''
        resp = requests.get(url, headers=headers)
        data = resp.json()['data']
        count = 0
        
        for i in range(len(data)):
            countCategory = 0
            for j in range(len(data[i-count]['data']['general']['places'])):
                # print(j)
                if not 'category' in data[i-count]['data']['general']['places'][j-countCategory]:
                    del data[i-count]['data']['general']['places'][j-countCategory]
                    countCategory += 1
                    continue
                if  data[i-count]['data']['general']['places'][j-countCategory]['locale']['name'] != city:
                    del data[i-count]['data']['general']['places'][j-countCategory]
                    countCategory += 1
            if not data[i-count]['data']['general']['places']:
                del data[i-count]
                count += 1
            countSeances = 0
            for u in range(len(data[i-count]['data']['general']['seances'])):
                if  datetime.strptime(data[i-count]['data']['general']['seances'][u-countSeances]['end'], "%Y-%m-%dT%H:%M:%SZ") < current_datetime:
                    del data[i-count]['data']['general']['seances'][u-countSeances]
                    countSeances += 1

        return Response(data)

class PostCityView(APIView):
    def post(self, request, format = None):
        post_body = json.loads(request.body)
        url = "https://nominatim.openstreetmap.org/reverse?format=json&lat=" + str(post_body['lat']) +"8&lon=" + str(post_body['lon'])
        resp = requests.get(url)
        data = resp.json()['address']['city']
        return Response(data)


class GetCountEventsToYear(APIView):
    def get(self, request, city = '', category = '', format = None):
        to_date = datetime.now()
        month = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']
        data = []
        url = '''https://opendata.mkrf.ru/v2/events/$?f={"data.general.start":{"$gt":"''' + str(to_date - timedelta(days=365)) + '''"},"data.general.end":{"$lt":"''' + str(to_date) + '''"},"data.general.category.name":{"$search":"''' + category + '''"},"data.general.places[].locale.name":{"$eq":"''' + city + '''"}}&l=1000'''
        resp = requests.get(url, headers=headers)
        var = resp.json()['data']
        for i in range(12):
            count = 0
            after_date = to_date
            to_date = after_date - timedelta(days=30)
            for j in range(len(var)):
                for x in range(len(var[j]['data']['general']['seances'])):
                    if datetime.strptime(var[j]['data']['general']['seances'][x]['start'], "%Y-%m-%dT%H:%M:%SZ") > to_date and datetime.strptime(var[j]['data']['general']['seances'][x]['end'], "%Y-%m-%dT%H:%M:%SZ") < after_date:
                        count = count + 1
            #data.append({'month': month[after_date.month-1], 'count': resp.json()['count']})
            data.append({'month': month[after_date.month-1], 'count': count})
        return Response(data)