from django.urls import path
from .views import Home, Search, OrderPdfView
urlpatterns = [
  path('', Home, name = 'Home'),
  path('search/', Search, name = 'Search'),
  path('search/pdf/<pk>/', OrderPdfView, name = 'OrderPdfView'),
]