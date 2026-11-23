# Zona Arcade — Tienda de Videojuegos (Django + MySQL)

Guía de instalación, Git y estudio para la defensa.
**Tip:** en VSCode abre este archivo y presiona `Ctrl+Shift+V` para verlo con formato.

---

## Índice

1. [Mapa del proyecto](#1-mapa-del-proyecto)
2. [Instalación en tu PC (paso a paso)](#2-instalación-en-tu-pc)
3. [Git y GitHub: main + tu branch](#3-git-y-github)
4. [Cómo funciona (explicación archivo por archivo)](#4-cómo-funciona)
5. [Guion para la demostración](#5-guion-para-la-demostración)
6. [Preguntas probables de la defensa](#6-preguntas-probables-de-la-defensa)
7. [Problemas frecuentes](#7-problemas-frecuentes)

---

## 1. Mapa del proyecto

```
tienda_videojuegos/
├── manage.py                  ← comando principal de Django (runserver, migrate...)
├── requirements.txt           ← librerías a instalar (Django y PyMySQL)
├── consultas_crud.sql         ← CRUD hecho directamente en MySQL (para phpMyAdmin)
├── GUIA.md                    ← esta guía
│
├── tienda/                    ← el PROYECTO (configuración general)
│   ├── __init__.py            ← activa PyMySQL como conector a MySQL
│   ├── settings.py            ← configuración: BD, apps instaladas, idioma...
│   └── urls.py                ← URLs principales (deriva a la app)
│
└── videojuegos/               ← la APLICACIÓN (la tienda en sí)
    ├── models.py              ← modelo Videojuego = la tabla en MySQL
    ├── forms.py               ← formularios de crear y editar + validaciones
    ├── views.py               ← lógica del CRUD
    ├── urls.py                ← direcciones de la app
    ├── admin.py               ← registro en el panel /admin (extra)
    ├── migrations/            ← historial de cambios de la tabla (lo genera Django)
    ├── fixtures/juegos_ejemplo.json   ← 8 juegos de ejemplo
    ├── templatetags/formato.py        ← filtro para mostrar precios: $59.990
    ├── static/videojuegos/    ← CSS (Bootstrap + estilos propios) y JS
    └── templates/videojuegos/ ← páginas HTML
        ├── base.html          ← plantilla madre: navbar + footer
        ├── inicio.html        ← página principal
        ├── lista.html         ← listado (tabla) + buscador
        ├── detalle.html       ← ver un juego
        ├── crear.html         ← formulario de CREAR
        ├── editar.html        ← formulario de EDITAR (distinto)
        ├── eliminar.html      ← confirmación para eliminar
        └── _campos.html       ← fragmento que dibuja los campos y errores
```

**Proyecto vs aplicación:** el *proyecto* (`tienda`) es la configuración general; una *app* (`videojuegos`) es un módulo con una función concreta. Un proyecto puede tener varias apps.

---

## 2. Instalación en tu PC

### 2.1 Preparar la base de datos (XAMPP)

1. Abre el **XAMPP Control Panel** y presiona **Start** en **MySQL** (y en Apache, para usar phpMyAdmin).
2. Entra a <http://localhost/phpmyadmin>.
3. Clic en **Nueva** (izquierda) → nombre: `tienda_videojuegos` → cotejamiento: `utf8mb4_general_ci` → **Crear**.

> La configuración usa el usuario `root` **sin contraseña** (lo normal en XAMPP). Si tu root tiene contraseña, escríbela en `tienda/settings.py`, en `'PASSWORD': ''`.

### 2.2 Preparar el proyecto

1. Descomprime `tienda_videojuegos.zip` donde quieras (por ejemplo `Documentos\`).
2. En VSCode: **Archivo → Abrir carpeta** → `tienda_videojuegos`.
3. Abre la terminal (`Ctrl+ñ` o **Terminal → Nueva terminal**) y ejecuta uno por uno:

```bash
# 1) Crear el entorno virtual (una carpeta "venv" con Python aislado para este proyecto)
python -m venv venv

# 2) Activarlo (en Windows / PowerShell). Debe aparecer (venv) al inicio de la línea
venv\Scripts\activate

# 3) Instalar Django y PyMySQL
pip install -r requirements.txt

# 4) Crear el archivo de migración a partir de models.py
python manage.py makemigrations

# 5) Aplicar las migraciones: crea las tablas en MySQL
python manage.py migrate

# 6) Cargar los 8 videojuegos de ejemplo
python manage.py loaddata juegos_ejemplo

# 7) Levantar el servidor
python manage.py runserver
```

4. Abre <http://127.0.0.1:8000> en el navegador. Debería verse Zona Arcade con 8 juegos.
5. En phpMyAdmin, dentro de `tienda_videojuegos`, ahora existe la tabla **`videojuegos_videojuego`**.

Para detener el servidor: `Ctrl+C` en la terminal.

**Cada vez que vuelvas a abrir el proyecto** solo necesitas: iniciar MySQL en XAMPP → `venv\Scripts\activate` → `python manage.py runserver`.

### 2.3 (Opcional) Panel de administración

```bash
python manage.py createsuperuser
```
Luego entra a <http://127.0.0.1:8000/admin>. No es parte del CRUD pedido, es un extra de Django.

---

## 3. Git y GitHub

El profesor pide, para trabajo individual: **una branch `main` y una branch propia**. Usaremos `main` para la base del proyecto y `desarrollo` para todo el CRUD, con un commit por etapa. Así se ve claramente tu trabajo.

### 3.1 Configurar Git (solo la primera vez en tu PC)

```bash
git config --global user.name "Javiera Lasseube"
git config --global user.email "tu_correo_de_github@ejemplo.com"
```
> Usa el **mismo correo de tu cuenta de GitHub**, así los commits aparecen con tu nombre y foto.

### 3.2 Crear el repositorio en GitHub

1. En github.com → **New repository**.
2. Nombre: `tienda-videojuegos-django`. Público. **NO marques** "Add a README" (el repo debe quedar vacío).
3. **Create repository** y copia la URL (`https://github.com/TU_USUARIO/tienda-videojuegos-django.git`).

### 3.3 Commits (haz esto DESPUÉS del paso 2.2, con todo funcionando)

En la terminal de VSCode, dentro de la carpeta del proyecto:

```bash
# ---------- BRANCH main: estructura base ----------
git init
git branch -M main

git add .gitignore requirements.txt manage.py tienda/ videojuegos/__init__.py videojuegos/apps.py videojuegos/migrations/__init__.py
git commit -m "Estructura base del proyecto Django y conexión a MySQL"

git remote add origin https://github.com/TU_USUARIO/tienda-videojuegos-django.git
git push -u origin main

# ---------- BRANCH desarrollo: el CRUD ----------
git checkout -b desarrollo

git add videojuegos/models.py videojuegos/migrations/
git commit -m "Modelo Videojuego y migración inicial"

git add videojuegos/forms.py
git commit -m "Formularios de crear y editar con validaciones"

git add videojuegos/views.py videojuegos/urls.py videojuegos/admin.py
git commit -m "Vistas y URLs del CRUD de videojuegos"

git add videojuegos/templates/ videojuegos/static/ videojuegos/templatetags/
git commit -m "Templates con Bootstrap: inicio, listado, detalle y formularios"

git add videojuegos/fixtures/ consultas_crud.sql GUIA.md
git commit -m "Datos de ejemplo, consultas SQL del CRUD y guía"

git push -u origin desarrollo
```

> Revisa con `git status` que no quede nada sin agregar (la carpeta `venv` NO debe subirse; el `.gitignore` la excluye).

### 3.4 Pull Request y merge (en GitHub)

1. En tu repo aparecerá un aviso **"desarrollo had recent pushes"** → **Compare & pull request**.
2. Base: `main` ← compare: `desarrollo`. Título: "CRUD de videojuegos". **Create pull request**.
3. **Merge pull request** → **Confirm merge**. **No borres** la branch `desarrollo` (el profesor quiere verla).
4. En tu PC, actualiza main:
```bash
git checkout main
git pull
```

Para mostrar en la defensa: `git log --oneline --graph --all` o la pestaña **Commits** / **Branches** de GitHub.

---

## 4. Cómo funciona

### 4.1 El recorrido de una petición (lo más importante para la defensa)

```
Navegador pide /videojuegos/3/editar/
        │
        ▼
tienda/urls.py        →  path('', include('videojuegos.urls'))
        │
        ▼
videojuegos/urls.py   →  path('videojuegos/<int:pk>/editar/', views.videojuego_editar)
        │                 (pk = 3)
        ▼
views.py              →  videojuego_editar(request, pk=3)
        │                 busca el juego en la BD (models.py → MySQL)
        │                 crea el formulario (forms.py)
        ▼
template editar.html  →  arma el HTML con los datos
        │
        ▼
Navegador muestra la página
```

Django sigue el patrón **MVT**: **M**odelo (datos), **V**ista (lógica), **T**emplate (presentación).

### 4.2 `tienda/settings.py` — configuración

- **`INSTALLED_APPS`**: incluye `'videojuegos'`. Sin esto Django no ve el modelo ni los templates.
- **`DATABASES`**: la conexión a MySQL.
  - `ENGINE: django.db.backends.mysql` → usar MySQL/MariaDB.
  - `NAME: tienda_videojuegos` → nombre de la BD creada en phpMyAdmin.
  - `USER root`, `PASSWORD ''`, `HOST 127.0.0.1`, `PORT 3306` → los datos de XAMPP.
  - `charset utf8mb4` → admite tildes, ñ y emojis.
- **`CsrfViewMiddleware`**: protege los formularios (ver `{% csrf_token %}`).

### 4.3 `tienda/__init__.py` — el conector

Django necesita un *driver* para hablar con MySQL. Usamos **PyMySQL** (se instala fácil en Windows) y `pymysql.install_as_MySQLdb()` hace que Django lo use como si fuera el driver oficial (`mysqlclient`).

### 4.4 `models.py` — la tabla

La clase `Videojuego(models.Model)` **es la tabla**. Cada atributo es una **columna**:

| Campo | Tipo Django | Tipo en MySQL | Regla |
|---|---|---|---|
| `id` | automático | BIGINT AUTO_INCREMENT, PK | lo crea Django |
| `titulo` | `CharField(max_length=100)` | VARCHAR(100) | obligatorio |
| `plataforma` | `CharField(choices=...)` | VARCHAR(10) | PS5, XBOX, SWITCH, PC |
| `genero` | `CharField(choices=...)` | VARCHAR(12) | lista de géneros |
| `precio` | `DecimalField(10, 0)` | DECIMAL(10,0) | `MinValueValidator(1)` → mayor que 0 |
| `stock` | `PositiveIntegerField` | INT UNSIGNED | no negativo |
| `anio_lanzamiento` | `PositiveSmallIntegerField` | SMALLINT UNSIGNED | mín. 1970 |
| `clasificacion` | `CharField(choices=...)` | VARCHAR(1) | E, T, M |
| `descripcion` | `TextField(blank=True)` | LONGTEXT | opcional |
| `fecha_registro` | `DateTimeField(auto_now_add=True)` | DATETIME | se llena sola al crear |

- **`choices`**: lista de opciones. Se guarda el código (`'PS5'`) y se muestra el nombre (`'PlayStation 5'`) con `get_plataforma_display`.
- **`class Meta: ordering = ['titulo']`**: orden alfabético por defecto.
- **`__str__`**: cómo se ve el objeto como texto.
- **`disponible`** (`@property`): devuelve `True` si `stock > 0`; el template lo usa para mostrar "Agotado".
- **¿Por qué `DecimalField` y no `FloatField` para el precio?** `Float` tiene errores de redondeo; `Decimal` es exacto, que es lo correcto para dinero.

### 4.5 Migraciones

- `makemigrations` lee `models.py` y escribe un archivo en `migrations/` (`0001_initial.py`) con las instrucciones para crear la tabla.
- `migrate` ejecuta esas instrucciones en MySQL (`CREATE TABLE ...`).
- Si mañana agregas un campo al modelo, repites ambos comandos y Django genera `0002_...` solo con el cambio.
- Para ver el SQL que genera: `python manage.py sqlmigrate videojuegos 0001`.

### 4.6 `forms.py` — formularios y validaciones

- **`ModelForm`**: crea los campos automáticamente a partir del modelo (`Meta.model` y `Meta.fields`).
- **`widgets`**: agregan clases de Bootstrap (`form-control`, `form-select`).
- **Dos formularios distintos** (lo pide la pauta):
  - `VideojuegoCrearForm`: todos los campos editables.
  - `VideojuegoEditarForm`: el **título queda bloqueado** (`disabled = True`). El juego no cambia de nombre; Django ignora cualquier valor que llegue para ese campo y mantiene el guardado.
  - Ambos heredan de `VideojuegoBaseForm`, para no repetir las validaciones (herencia).

**Validaciones (todas se ejecutan al llamar a `form.is_valid()`):**

| Validación | Dónde |
|---|---|
| Campos obligatorios | automático (campos sin `blank=True`) |
| Valores numéricos | automático (`DecimalField`, `IntegerField` rechazan "abc") |
| Opción válida en listas | automático (`choices`) |
| Título de al menos 2 caracteres (y sin espacios sobrantes) | `clean_titulo()` |
| Precio mayor que cero | `clean_precio()` + `MinValueValidator` del modelo |
| Stock no negativo | `clean_stock()` + `PositiveIntegerField` |
| Año entre 1970 y el año actual | `clean_anio_lanzamiento()` |
| No repetir el mismo juego en la misma plataforma | `clean()` (valida 2 campos juntos) |

- **`clean_<campo>()`** valida un campo; si falla, `raise forms.ValidationError('mensaje')` y el error aparece bajo ese campo.
- **`clean()`** valida campos combinados; su error aparece arriba del formulario.
- **`self.instance.pk`** en `clean()`: al **editar**, se excluye el propio juego, para que no se detecte a sí mismo como duplicado.
- En los `<form>` se usa `novalidate` para desactivar la validación del navegador y que se vean las de Django (las del servidor son las que realmente protegen la BD).

### 4.7 `views.py` — la lógica del CRUD

Todas son **vistas basadas en funciones** (FBV): reciben `request` y devuelven una respuesta.

| Vista | CRUD | Qué hace | SQL equivalente |
|---|---|---|---|
| `inicio` | — | cuenta juegos, stock total, agotados, 3 recientes | `COUNT`, `SUM` |
| `videojuego_lista` | **R** | todos los juegos + búsqueda (`?q=`) y filtro por plataforma | `SELECT ... WHERE titulo LIKE` |
| `videojuego_detalle` | **R** | un juego por su id | `SELECT ... WHERE id=` |
| `videojuego_crear` | **C** | GET: formulario vacío. POST: valida y guarda | `INSERT` |
| `videojuego_editar` | **U** | GET: formulario con datos. POST: valida y actualiza | `UPDATE` |
| `videojuego_eliminar` | **D** | GET: pide confirmación. POST: borra | `DELETE` |

**Patrón de crear/editar (memorízalo):**
```python
if request.method == 'POST':              # se envió el formulario
    form = Formulario(request.POST)       # se llena con lo enviado
    if form.is_valid():                   # pasa las validaciones
        form.save()                       # guarda en MySQL
        return redirect(...)              # redirige (evita reenvío con F5)
else:
    form = Formulario()                   # GET: formulario vacío
return render(request, 'template.html', {'form': form})   # si hay errores, se re-muestra con ellos
```
- En editar se agrega **`instance=juego`**: así `save()` hace UPDATE de ese registro en vez de crear uno nuevo.
- **`get_object_or_404`**: si el id no existe, muestra error 404 en vez de que la app falle.
- **`redirect`** después de guardar: patrón *Post/Redirect/Get*; evita que al recargar la página se cree el juego dos veces.
- **`messages.success`**: el mensaje verde "se agregó al catálogo" que aparece en la siguiente página.
- **`Q(...) | Q(...)`**: permite búsquedas con OR. **`icontains`**: contiene, sin importar mayúsculas (`LIKE '%texto%'`).
- **¿Por qué eliminar usa POST y no un enlace?** Un GET no debe modificar datos (un buscador o el navegador podría "visitar" el enlace y borrar). Además POST lleva el token CSRF.

### 4.8 `urls.py`

```python
path('videojuegos/<int:pk>/editar/', views.videojuego_editar, name='videojuego_editar')
```
- `<int:pk>` captura el número de la URL y lo pasa como parámetro `pk` a la vista.
- `name=` permite escribir `{% url 'videojuego_editar' juego.pk %}` en los templates en vez de la dirección fija: si la URL cambia, los enlaces siguen funcionando.

### 4.9 Templates

- **Herencia**: `base.html` tiene la navbar, los mensajes y el footer. Las demás páginas usan `{% extends 'videojuegos/base.html' %}` y solo llenan `{% block contenido %}`. Así la navegación es la misma en todas las páginas.
- **`{% include '_campos.html' %}`**: reutiliza el fragmento que dibuja los campos y sus errores en crear y editar.
- **Sintaxis**: `{{ variable }}` muestra un dato; `{% etiqueta %}` es lógica (`for`, `if`, `url`, `csrf_token`).
- **`{% for ... %}{% empty %}`**: muestra un mensaje si no hay registros.
- **`{% csrf_token %}`**: token oculto que demuestra que el formulario viene de nuestra página (protección CSRF). Sin él, Django rechaza el POST con error 403.
- **`{% load static %}`**: para enlazar CSS/JS. Bootstrap está **incluido en el proyecto** (carpeta `static`), funciona sin internet.
- **`{{ juego.precio|clp }}`**: filtro propio (`templatetags/formato.py`) que muestra `$59.990`.

---

## 5. Guion para la demostración

Ten abiertos: VSCode, el navegador en la app y phpMyAdmin.

1. **Arranque:** XAMPP con MySQL encendido → `python manage.py runserver` sin errores.
2. **Conexión:** muestra `DATABASES` en `settings.py` y la tabla `videojuegos_videojuego` en phpMyAdmin (pestaña Estructura).
3. **CRUD web:**
   - **C**: "Agregar juego" → primero envía con errores (precio 0, stock -1, año 2050) y muestra los mensajes → luego datos correctos → guardar.
   - **R**: catálogo, búsqueda por título y filtro por plataforma, ver detalle.
   - **U**: editar el juego (muestra que el título está bloqueado) → cambiar precio y stock.
   - **D**: eliminar → pantalla de confirmación → eliminar.
   - Después de cada paso, **refresca phpMyAdmin** (pestaña Examinar) para mostrar que el cambio está en MySQL.
4. **CRUD en la BD:** en phpMyAdmin → pestaña **SQL** → ejecuta los bloques de `consultas_crud.sql` (INSERT, SELECT, UPDATE, DELETE) y muestra que el cambio aparece en la web al recargar.
5. **Git:** GitHub → branches `main` y `desarrollo`, lista de commits y el Pull Request.

---

## 6. Preguntas probables de la defensa

**1. ¿Cómo se conecta Django con MySQL?**
En `settings.py`, en `DATABASES`, con `ENGINE` `django.db.backends.mysql`, el nombre de la BD, usuario, contraseña, host y puerto de XAMPP. Además se necesita un driver: usé PyMySQL, activado en `tienda/__init__.py` con `pymysql.install_as_MySQLdb()`.

**2. ¿Qué es un modelo?**
Una clase en `models.py` que representa una tabla. Cada atributo es una columna con su tipo. Django la traduce a SQL mediante las migraciones.

**3. ¿Qué es el ORM?**
*Object-Relational Mapping*: permite trabajar con la BD usando objetos Python en vez de SQL. Por ejemplo `Videojuego.objects.filter(plataforma='PS5')` equivale a `SELECT * FROM videojuegos_videojuego WHERE plataforma='PS5'`.

**4. ¿Diferencia entre `makemigrations` y `migrate`?**
`makemigrations` detecta cambios en `models.py` y crea el archivo de migración. `migrate` aplica esos archivos en la base de datos (crea o modifica tablas).

**5. ¿Qué pasa si agrego un campo nuevo al modelo?**
Corro `makemigrations` (se crea `0002_...`) y `migrate` (se agrega la columna). Si el campo es obligatorio, Django pide un valor por defecto para los registros existentes.

**6. ¿Cómo valida los datos tu aplicación?**
En `forms.py`: validaciones automáticas (obligatorios, numéricos, opciones), métodos `clean_precio`, `clean_stock`, `clean_anio_lanzamiento`, `clean_titulo` para cada campo, y `clean()` para evitar duplicados. Además, el modelo tiene `MinValueValidator` y `PositiveIntegerField`, y la columna `stock` es UNSIGNED en MySQL.

**7. ¿Qué hace `form.is_valid()`?**
Ejecuta todas las validaciones. Si todo está bien devuelve `True` y deja los datos limpios en `cleaned_data`; si no, guarda los errores en `form.errors` y devuelve `False`.

**8. ¿Diferencia entre GET y POST?**
GET pide o muestra información (abrir una página, la búsqueda del catálogo). POST envía datos para crear, modificar o eliminar. Por eso las vistas preguntan `if request.method == 'POST'`.

**9. ¿Para qué sirve `{% csrf_token %}`?**
Protege contra ataques CSRF: agrega un código secreto al formulario que Django verifica, para asegurarse de que el envío viene de nuestra propia página. Sin él, el POST da error 403.

**10. ¿Por qué tus formularios de crear y editar son distintos?**
Son dos clases: `VideojuegoCrearForm` permite todos los campos y `VideojuegoEditarForm` bloquea el título. Además tienen templates diferentes (`crear.html` y `editar.html`); el de editar muestra un panel con los datos actuales. Ambos heredan las validaciones de `VideojuegoBaseForm`.

**11. ¿Cómo sabe el formulario de editar qué registro actualizar?**
Por `instance=juego`. La vista busca el juego con `get_object_or_404(Videojuego, pk=pk)` y se lo pasa al formulario; así `form.save()` hace un UPDATE de ese registro.

**12. ¿Qué es `pk` y de dónde viene?**
*Primary key*, la clave primaria (`id`). Viene de la URL: `<int:pk>` en `urls.py` lo captura y lo pasa a la vista.

**13. ¿Qué hace `get_object_or_404`?**
Busca el registro y, si no existe, responde con error 404 en lugar de que la aplicación se caiga.

**14. ¿Por qué después de guardar haces `redirect`?**
Para no reenviar el formulario si el usuario recarga la página (patrón Post/Redirect/Get), lo que crearía duplicados.

**15. ¿Cómo funciona la herencia de templates?**
`base.html` define la estructura común (navbar, mensajes, footer) y un `{% block contenido %}`. Cada página hace `{% extends %}` y rellena solo ese bloque.

**16. ¿Qué es MVT?**
Modelo (datos, `models.py`), Vista (lógica, `views.py`) y Template (HTML). Las URLs conectan la petición con la vista.

**17. ¿Por qué el precio es `DecimalField`?**
Porque es dinero: `DecimalField` es exacto, mientras que `FloatField` puede tener errores de redondeo.

**18. ¿Qué es `choices`?**
Una lista de opciones válidas para un campo. En la BD se guarda el código (`PS5`) y en pantalla se muestra el nombre con `get_plataforma_display`. El formulario la convierte en un menú desplegable.

**19. ¿Qué es el entorno virtual y por qué usarlo?**
Una instalación de Python aislada para el proyecto, con sus propias librerías (Django, PyMySQL). Evita conflictos de versiones con otros proyectos. Se crea con `python -m venv venv`.

**20. ¿Cómo usaste Git?**
La base del proyecto está en `main`. Desarrollé el CRUD en la branch `desarrollo` con un commit por etapa (modelo, formularios, vistas, templates) y lo uní a `main` con un Pull Request.

---

## 7. Problemas frecuentes

| Error | Solución |
|---|---|
| `venv\Scripts\activate` no se puede ejecutar ("ejecución de scripts deshabilitada") | En PowerShell: `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` → responde `S` y vuelve a activar. O usa la terminal **Command Prompt** de VSCode. |
| `Can't connect to MySQL server` / `(2003, ...)` | MySQL no está iniciado en XAMPP. Presiona Start. |
| `Unknown database 'tienda_videojuegos'` | No creaste la BD en phpMyAdmin (paso 2.1). |
| `Access denied for user 'root'` | Tu root tiene contraseña: escríbela en `settings.py` → `PASSWORD`. |
| `No module named 'pymysql'` o `'django'` | No está activado el venv (falta `(venv)` al inicio) o falta `pip install -r requirements.txt`. |
| `MariaDB 10.x or later is required` | Instalaste Django 5. Usa `pip install -r requirements.txt` (fija Django 4.2, compatible con el MariaDB 10.4 de XAMPP). |
| `No changes detected` en `makemigrations` | Ya existe la migración; continúa con `migrate`. |
| Error al instalar Django con Python 3.14 | Instala Python 3.12 o 3.13 desde python.org y crea el venv con esa versión. |
| Puerto 8000 ocupado | `python manage.py runserver 8080` y entra a `http://127.0.0.1:8080`. |
| La página se ve sin estilos | Revisa que `DEBUG = True` en `settings.py` y que exista la carpeta `videojuegos/static`. |
