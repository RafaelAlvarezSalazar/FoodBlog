# FoodBlog Internacional

Blog de recetas internacionales hecho con Python, Flask y plantillas Jinja. Incluye diez recetas con fotos, un buscador por nombre, país, categoría o tiempo, y un formulario para publicar recetas con foto opcional. Desde cada ficha se puede votar; el ranking y las estadísticas se calculan con los datos del recetario. El botón **Sorpréndeme** abre una receta al azar.

## 1. Descargar FoodBlog en ZIP

1. Abre el [repositorio de FoodBlog](https://github.com/RafaelAlvarezSalazar/FoodBlog).
2. Pulsa el botón verde **Code** y selecciona **Download ZIP**. También puedes [descargar el ZIP directamente](https://github.com/RafaelAlvarezSalazar/FoodBlog/archive/refs/heads/main.zip). No necesitas instalar Git.
3. En el Explorador de archivos de Windows, haz clic derecho en `FoodBlog-main.zip` y elige **Extraer todo**.
4. Abre la carpeta extraída hasta que veas `app.py` y `requirements.txt`. En esa carpeta, escribe `powershell` en la barra de direcciones del Explorador y pulsa **Intro**.

## 2. Instalar Flask en Windows

Necesitas **Python 3.11**. Para comprobar que está instalado, ejecuta `py -3.11 --version` en PowerShell. Debería mostrar `Python 3.11.x`.

Crea un entorno virtual para el proyecto e instala sus dependencias. El segundo comando instala **Flask**, que ejecuta la aplicación, y **Pillow**, que procesa las fotos. Solo necesitas hacerlo la primera vez:

```powershell
py -3.11 -m venv .venv *puedes poner tambien la version de python 3.xx*
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Para comprobar que Flask está instalado en ese entorno, ejecuta `.\.venv\Scripts\python.exe -m flask --version`.

## 3. Arrancar FoodBlog

Desde la misma carpeta, ejecuta:

```powershell
.\.venv\Scripts\python.exe app.py
```

Abre **[http://127.0.0.1:5000](http://127.0.0.1:5000)** en el navegador y deja PowerShell abierto mientras usas el blog. Para detener el servidor, pulsa **Ctrl+C** en la terminal. La próxima vez solo necesitas repetir este paso.

## Organización

- `app.py`: rutas de Flask y procesamiento de formularios.
- `datos.py`: colección inicial de recetas en memoria.
- `funciones.py`: validación, filtros, tratamiento de fotos, ranking y estadísticas.
- `templates/`: páginas HTML con una plantilla base común.
- `static/`: estilos y fotografías del recetario. Consulta los [créditos y licencias de las imágenes](static/fotos/creditos.html).

Las recetas que publiques desde el navegador, sus fotos y los votos se conservan mientras el servidor está en marcha. Al reiniciarlo vuelves a las diez recetas iniciales.
