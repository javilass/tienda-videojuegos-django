"""
URLs de la app: conectan cada dirección con su vista.
<int:pk> captura un número de la URL (el id del videojuego) y se lo pasa a la vista.
name='...' permite usar {% url 'nombre' %} en los templates y redirect('nombre') en las vistas.
"""
from django.urls import path

from . import views

urlpatterns = [ #conecta cada URL con su vista correspondiente
    path('', views.inicio, name='inicio'),
    path('videojuegos/', views.videojuego_lista, name='videojuego_lista'),
    path('videojuegos/nuevo/', views.videojuego_crear, name='videojuego_crear'),
    path('videojuegos/<int:pk>/', views.videojuego_detalle, name='videojuego_detalle'),
    path('videojuegos/<int:pk>/editar/', views.videojuego_editar, name='videojuego_editar'),
    path('videojuegos/<int:pk>/eliminar/', views.videojuego_eliminar, name='videojuego_eliminar'),
]
