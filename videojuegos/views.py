"""
VISTAS = la lógica. Cada función recibe una petición (request) y devuelve una respuesta.

Flujo:  URL (urls.py)  ->  vista (views.py)  ->  modelo/BD (models.py)  ->  template (.html)

CRUD:
  C - crear     -> videojuego_crear
  R - consultar -> videojuego_lista, videojuego_detalle
  U - modificar -> videojuego_editar
  D - eliminar  -> videojuego_eliminar

GET  = pedir/mostrar una página.     POST = enviar datos de un formulario.
"""
from django.contrib import messages
from django.db.models import Q, Sum
from django.shortcuts import get_object_or_404, redirect, render

from .forms import VideojuegoCrearForm, VideojuegoEditarForm
from .models import Videojuego


def inicio(request):
    """Página principal con algunos números de la tienda."""
    contexto = {
        'total_juegos': Videojuego.objects.count(),                       # SELECT COUNT(*)
        'total_stock': Videojuego.objects.aggregate(t=Sum('stock'))['t'] or 0,
        'agotados': Videojuego.objects.filter(stock=0).count(),
        'recientes': Videojuego.objects.order_by('-fecha_registro')[:3],  # últimos 3 agregados
    }
    return render(request, 'videojuegos/inicio.html', contexto)


def videojuego_lista(request):
    """R - Listado de todos los videojuegos, con búsqueda y filtro por plataforma."""
    juegos = Videojuego.objects.all()                 # SELECT * FROM videojuegos_videojuego

    busqueda = request.GET.get('q', '').strip()       # lo que se escribió en el buscador
    plataforma = request.GET.get('plataforma', '')

    if busqueda:
        # Q permite usar OR: busca en título o descripción (icontains = LIKE '%texto%')
        juegos = juegos.filter(Q(titulo__icontains=busqueda) | Q(descripcion__icontains=busqueda))
    if plataforma:
        juegos = juegos.filter(plataforma=plataforma)

    contexto = {
        'juegos': juegos,
        'busqueda': busqueda,
        'plataforma': plataforma,
        'plataformas': Videojuego.PLATAFORMAS,
    }
    return render(request, 'videojuegos/lista.html', contexto)


def videojuego_detalle(request, pk):
    """R - Ver un videojuego. Si el id no existe, muestra error 404."""
    juego = get_object_or_404(Videojuego, pk=pk)      # SELECT ... WHERE id = pk
    return render(request, 'videojuegos/detalle.html', {'juego': juego})


def videojuego_crear(request):
    """C - Crear un videojuego."""
    if request.method == 'POST':
        form = VideojuegoCrearForm(request.POST)      # formulario con los datos enviados
        if form.is_valid():                           # ejecuta TODAS las validaciones
            juego = form.save()                       # INSERT INTO ...
            messages.success(request, f'"{juego.titulo}" se agregó al catálogo.')
            return redirect('videojuego_detalle', pk=juego.pk)
    else:
        form = VideojuegoCrearForm()                  # formulario vacío
    # Si es GET, o si hubo errores, se vuelve a mostrar el formulario
    return render(request, 'videojuegos/crear.html', {'form': form})


def videojuego_editar(request, pk):
    """U - Modificar un videojuego existente."""
    juego = get_object_or_404(Videojuego, pk=pk)
    if request.method == 'POST':
        # instance=juego indica que se actualiza ESTE registro, no que se crea uno nuevo
        form = VideojuegoEditarForm(request.POST, instance=juego)
        if form.is_valid():
            form.save()                               # UPDATE ... WHERE id = pk
            messages.success(request, f'"{juego.titulo}" se actualizó correctamente.')
            return redirect('videojuego_detalle', pk=juego.pk)
    else:
        form = VideojuegoEditarForm(instance=juego)   # formulario con los datos actuales
    return render(request, 'videojuegos/editar.html', {'form': form, 'juego': juego})


def videojuego_eliminar(request, pk):
    """D - Eliminar. GET muestra la confirmación; POST borra de verdad."""
    juego = get_object_or_404(Videojuego, pk=pk)
    if request.method == 'POST':
        titulo = juego.titulo
        juego.delete()                                # DELETE FROM ... WHERE id = pk
        messages.success(request, f'"{titulo}" se eliminó del catálogo.')
        return redirect('videojuego_lista')
    return render(request, 'videojuegos/eliminar.html', {'juego': juego})
