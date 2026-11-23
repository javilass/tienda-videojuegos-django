"""
URLs principales del proyecto.
Todo lo que no sea /admin/ se delega a las URLs de la app "videojuegos".
"""
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('videojuegos.urls')),
]
