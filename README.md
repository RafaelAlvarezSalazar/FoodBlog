# FoodBlog Internacional

Blog de recetas internacionales hecho con Python, Flask y plantillas Jinja. Incluye diez recetas con fotos, un buscador por nombre, país, categoría o tiempo, y un formulario para publicar recetas con foto opcional. Desde cada ficha se puede votar; el ranking y las estadísticas se calculan con los datos del recetario. El botón **Sorpréndeme** abre una receta al azar.

## Ejecutar en Windows

Con Python 3.11 instalado, abre PowerShell en la carpeta del proyecto (donde está `app.py`) y ejecuta:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe app.py
```

Abre **[http://127.0.0.1:5000](http://127.0.0.1:5000)** en el navegador. Para detener el servidor, pulsa **Ctrl+C** en la terminal. En los siguientes arranques solo necesitas el último comando.

## Organización

- `app.py`: rutas de Flask y procesamiento de formularios.
- `datos.py`: colección inicial de recetas en memoria.
- `funciones.py`: validación, filtros, tratamiento de fotos, ranking y estadísticas.
- `templates/`: páginas HTML con una plantilla base común.
- `static/`: estilos y fotografías del recetario. Consulta los [créditos y licencias de las imágenes](static/fotos/creditos.html).

Las recetas que publiques desde el navegador, sus fotos y los votos se conservan mientras el servidor está en marcha. Al reiniciarlo vuelves a las diez recetas iniciales.
