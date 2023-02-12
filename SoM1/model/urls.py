from django.urls import path
from .views import *

urlpatterns = [
    path('form/', beam_creator),
    path('support/', support_type),
    path('cantilevered/', cantilevered),
    path('pinroller/', pinroller),
]