from django.contrib import admin

from .models import Videojuego


@admin.register(Videojuego) #permite registrar el modelo en el admin de Django
class VideojuegoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'plataforma', 'genero', 'precio', 'stock', 'anio_lanzamiento')
    list_filter = ('plataforma', 'genero', 'clasificacion')
    search_fields = ('titulo',)
