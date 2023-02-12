from .views import *
from django.urls import path

urlpatterns = [
    path('home/', homepage, name='home'),
    path('beam/', beam_button, name='beam'),
    path('supports/', supports_button, name='supports'),
    path('forces/', forces_button, name='forces'),
    path('moments/', moments_button, name='moments'),
    path('calculate/', calculator, name='results'),
]