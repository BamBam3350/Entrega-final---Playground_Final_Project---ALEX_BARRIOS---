from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('agregar/', views.agregar_post, name='agregar_post'),
    path('buscar/', views.buscar_posts, name='buscar_posts'),
    path('post/<int:pk>/', views.detalle_post, name='detalle_post'),
]