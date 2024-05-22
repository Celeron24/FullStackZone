from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('archive/', views.archive, name='archive'),
    path('search/', views.rss_feed_search, name='rss_feed_search'),
]

