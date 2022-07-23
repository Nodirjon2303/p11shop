from django.urls import path
from .views import *
urlpatterns = [
    path('', homeView, name='home'), 
    path('shop/<slug:slug>/', shopView, name='shop'),
    path('cart/', cartView, name='cart')
]
