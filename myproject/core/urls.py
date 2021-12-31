from django.urls import path
from core import views
from django.views.decorators.csrf import csrf_exempt 
urlpatterns = [
    path('', csrf_exempt(views.base), name='base'),
    path('exito', csrf_exempt(views.success), name='success'),
    path('refund/', views.refund, name='refund'),
]

