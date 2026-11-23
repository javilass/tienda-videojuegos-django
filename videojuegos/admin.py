from django.contrib import admin

from .models import Videojuego


@admin.register(Videojuego)
class VideojuegoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'plataforma', 'genero', 'precio', 'stock', 'anio_lanzamiento')
    list_filter = ('plataforma', 'genero', 'clasificacion')
    search_fields = ('titulo',)
