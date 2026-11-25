"""
FORMULARIOS y VALIDACIONES.

Un ModelForm crea automáticamente los campos del formulario a partir del modelo.
Las validaciones se ejecutan cuando la vista llama a form.is_valid():
  1) validaciones de cada campo (obligatorio, tipo numérico, validators del modelo)
  2) métodos clean_<campo>()  -> validan UN campo
  3) método clean()           -> valida varios campos juntos
Si algo falla, el error se guarda en form.errors y se muestra en el template.
"""
from datetime import date

from django import forms

from .models import Videojuego

ANIO_MINIMO = 1970

# Clases de Bootstrap para que los campos se vean bien
WIDGETS = { #son diccionarios que indican cómo se renderizan los campos del formulario
    'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: The Legend of Zelda'}),
    'plataforma': forms.Select(attrs={'class': 'form-select'}),
    'genero': forms.Select(attrs={'class': 'form-select'}),
    'precio': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'placeholder': 'Ej: 49990'}),
    'stock': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
    'anio_lanzamiento': forms.NumberInput(attrs={'class': 'form-control', 'min': ANIO_MINIMO}),
    'clasificacion': forms.Select(attrs={'class': 'form-select'}),
    'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
}


class VideojuegoBaseForm(forms.ModelForm):
    """Validaciones comunes a ambos formularios."""

    class Meta:
        model = Videojuego
        fields = ['titulo', 'plataforma', 'genero', 'precio', 'stock',
                  'anio_lanzamiento', 'clasificacion', 'descripcion']
        widgets = WIDGETS

    def clean_titulo(self): #validación de un solo campo: título
        titulo = self.cleaned_data['titulo'].strip()   # quita espacios al inicio/fin
        if len(titulo) < 2:
            raise forms.ValidationError('El título debe tener al menos 2 caracteres.')
        return titulo

    def clean_precio(self): #validación de un solo campo: precio
        precio = self.cleaned_data['precio']
        if precio is not None and precio <= 0:
            raise forms.ValidationError('El precio debe ser mayor que cero.')
        return precio

    def clean_stock(self): #validación de un solo campo: stock
        stock = self.cleaned_data['stock']
        if stock is not None and stock < 0:
            raise forms.ValidationError('El stock no puede ser negativo.')
        return stock

    def clean_anio_lanzamiento(self): #validación de un solo campo: año de lanzamiento
        anio = self.cleaned_data['anio_lanzamiento']
        anio_actual = date.today().year
        if anio is not None and not (ANIO_MINIMO <= anio <= anio_actual):
            raise forms.ValidationError(f'El año debe estar entre {ANIO_MINIMO} y {anio_actual}.')
        return anio

    def clean(self):
        """Validación de varios campos: no repetir el mismo juego en la misma plataforma."""
        datos = super().clean()
        titulo = datos.get('titulo')
        plataforma = datos.get('plataforma')
        if titulo and plataforma:
            repetidos = Videojuego.objects.filter(titulo__iexact=titulo, plataforma=plataforma)
            if self.instance.pk:                       # al editar, no compararse consigo mismo
                repetidos = repetidos.exclude(pk=self.instance.pk)
            if repetidos.exists():
                raise forms.ValidationError('Ya existe este videojuego para esa plataforma.')
        return datos


class VideojuegoCrearForm(VideojuegoBaseForm):
    """Formulario de creación: todos los campos."""
    pass


class VideojuegoEditarForm(VideojuegoBaseForm):
    """Formulario de edición: el título se muestra pero no se puede modificar."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # disabled=True: el navegador no deja escribir y Django ignora lo que llegue,
        # usando siempre el valor que ya está guardado.
        self.fields['titulo'].disabled = True
        self.fields['titulo'].help_text = 'El título no se puede modificar.'
