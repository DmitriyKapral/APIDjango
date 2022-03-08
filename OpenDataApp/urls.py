from django.urls import re_path, include
from OpenDataApp import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    re_path(r'^general/$', views.GeneralView.as_view(), name='general'),
    re_path(r'^general/(?P<pk>[^\d]+)/$', views.GeneralListView.as_view(), name='generals'),
    re_path(r"^categoryget/(?P<category>[^\d]+)/(?P<city>[^\d]+)/$", views.GetCategoryView.as_view(), name='alllist72'),
    re_path(r"^searchObject/(?P<category>[^\d]+)/(?P<city>[^\d]+)/(?P<search>[^\d]+)/$", views.GetSearchObjectView.as_view()),
    re_path(r"^getevents/(?P<city>[^\d]+)/(?P<date>[^\s]+)/$", views.GetEventsView.as_view()),
    re_path(r"^testevent/$", views.TestGetEventsView.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)

