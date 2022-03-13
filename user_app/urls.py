from unicodedata import name
from django.urls import path, include
from .views import Index
from . import views


urlpatterns = [
    path('', Index.as_view(), name='home'),

]
