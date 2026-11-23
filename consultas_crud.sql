-- =====================================================================
-- CRUD A NIVEL DE BASE DE DATOS (para demostrar en phpMyAdmin > pestaña SQL)
-- Base de datos: tienda_videojuegos   |   Tabla: videojuegos_videojuego
-- Ejecuta cada bloque por separado y muestra el resultado.
-- =====================================================================

USE tienda_videojuegos;

-- Ver la estructura de la tabla que creó la migración de Django
DESCRIBE videojuegos_videojuego;


-- ---------- R: CONSULTAR ----------
SELECT id, titulo, plataforma, precio, stock FROM videojuegos_videojuego;

-- Consultar con filtro: juegos de PS5 ordenados por precio
SELECT titulo, precio FROM videojuegos_videojuego
WHERE plataforma = 'PS5'
ORDER BY precio DESC;


-- ---------- C: CREAR ----------
INSERT INTO videojuegos_videojuego
    (titulo, plataforma, genero, precio, stock, anio_lanzamiento, clasificacion, descripcion, fecha_registro)
VALUES
    ('Minecraft', 'PC', 'AVENTURA', 19990, 10, 2011, 'E', 'Juego de construcción por bloques.', NOW());

-- Comprobar: ahora aparece también en la web (Catálogo)
SELECT * FROM videojuegos_videojuego WHERE titulo = 'Minecraft';


-- ---------- U: MODIFICAR ----------
UPDATE videojuegos_videojuego
SET precio = 14990, stock = 25
WHERE titulo = 'Minecraft';

SELECT titulo, precio, stock FROM videojuegos_videojuego WHERE titulo = 'Minecraft';


-- ---------- D: ELIMINAR ----------
DELETE FROM videojuegos_videojuego WHERE titulo = 'Minecraft';

SELECT COUNT(*) AS total_juegos FROM videojuegos_videojuego;


-- ---------- EXTRA: la validación también existe en la BD ----------
-- stock es UNSIGNED: MySQL rechaza un número negativo (error "Out of range value")
-- UPDATE videojuegos_videojuego SET stock = -5 WHERE id = 1;
