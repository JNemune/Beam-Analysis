from .views import *
from django.urls import path

urlpatterns = [
    path('floading/', ForceLoad),
    path('mloading/', MomentLoad),
    path('F_delete/', ClearForce),
    path('M_delete/', ClearMoment),
]