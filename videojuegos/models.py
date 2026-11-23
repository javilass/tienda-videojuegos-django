"""
MODELO = la estructura de la tabla en la base de datos.

Cada clase que hereda de models.Model se convierte en una TABLA en MySQL.
Cada atributo (titulo, precio, ...) se convierte en una COLUMNA.
Django crea la tabla con: python manage.py makemigrations  +  python manage.py migrate
La tabla se llamará "videojuegos_videojuego" (nombreapp_nombremodelo).
"""
from django.core.validators import MinValueValidator
from django.db import models


class Videojuego(models.Model):

    # "choices": listas de opciones fijas. El 1er valor se guarda en la BD, el 2do se muestra.
    PLATAFORMAS = [
        ('PS5', 'PlayStation 5'),
        ('XBOX', 'Xbox Series X|S'),
        ('SWITCH', 'Nintendo Switch'),
        ('PC', 'PC'),
    ]

    GENEROS = [
        ('ACCION', 'Acción'),
        ('AVENTURA', 'Aventura'),
        ('RPG', 'RPG'),
        ('DEPORTES', 'Deportes'),
        ('CARRERAS', 'Carreras'),
        ('ESTRATEGIA', 'Estrategia'),
        ('SHOOTER', 'Shooter'),
    ]

    CLASIFICACIONES = [
        ('E', 'E - Todo público'),
        ('T', 'T - Adolescentes (13+)'),
        ('M', 'M - Adultos (17+)'),
    ]

    # ---------- CAMPOS (columnas) ----------
    # VARCHAR(100) NOT NULL
    titulo = models.CharField('Título', max_length=100)

    # VARCHAR(10) con opciones
    plataforma = models.CharField('Plataforma', max_length=10, choices=PLATAFORMAS)
    genero = models.CharField('Género', max_length=12, choices=GENEROS)

    # DECIMAL(10,0): pesos chilenos sin decimales. Mínimo $1 (precio mayor que cero)
    precio = models.DecimalField(
        'Precio (CLP)', max_digits=10, decimal_places=0,
        validators=[MinValueValidator(1, 'El precio debe ser mayor que cero.')],
    )

    # INT UNSIGNED: no permite negativos
    stock = models.PositiveIntegerField('Stock', default=0)

    # SMALLINT UNSIGNED. Mínimo 1970; el máximo (año actual) se revisa en forms.py
    # porque el año actual cambia y no conviene "congelarlo" en la migración.
    anio_lanzamiento = models.PositiveSmallIntegerField(
        'Año de lanzamiento',
        validators=[MinValueValidator(1970, 'El año no puede ser anterior a 1970.')],
    )

    clasificacion = models.CharField('Clasificación', max_length=1, choices=CLASIFICACIONES)

    # TEXT, opcional (blank=True permite dejarlo vacío en el formulario)
    descripcion = models.TextField('Descripción', blank=True)

    # DATETIME que Django llena solo al crear el registro
    fecha_registro = models.DateTimeField('Fecha de registro', auto_now_add=True)

    class Meta:
        ordering = ['titulo']                  # orden por defecto al listar
        verbose_name = 'videojuego'
        verbose_name_plural = 'videojuegos'

    def __str__(self):
        # Cómo se muestra un objeto como texto (por ej. en el admin)
        return f'{self.titulo} ({self.get_plataforma_display()})'

    @property
    def disponible(self):
        """True si hay stock. Se usa en los templates para mostrar 'Agotado'."""
        return self.stock > 0
