from django.urls import re_path, include
from OpenDataApp import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    re_path(r"^categoryget/(?P<category>[^\d]+)/(?P<city>[^\d]+)/$", views.GetCategoryView.as_view(), name='alllist72'),
    re_path(r"^geteventscategory/(?P<city>[^\d]+)/$", views.GetEventsView.as_view()),
    re_path(r"^position/$", views.PostCityView.as_view()),
    re_path(r"^getcountevents/(?P<category>[^\d]+)/(?P<city>[^\d]+)/$", views.GetCountEventsToYear.as_view()),
    re_path(r"^getcountobjects/(?P<city>[^\d]+)/$", views.GetCountObjectsToCity.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)