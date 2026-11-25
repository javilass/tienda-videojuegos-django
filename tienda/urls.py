"""
URLs principales del proyecto.
Todo lo que no sea /admin/ se delega a las URLs de la app "videojuegos".
"""
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls), #esto es para acceder al panel de administración de Django
    path('', include('videojuegos.urls')), #esto es para que todo lo que no sea /admin/ se maneje con las urls de la app videojuegos
]
