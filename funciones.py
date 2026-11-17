import unicodedata
from io import BytesIO

from PIL import Image, ImageOps


def preparar_foto(archivo):
    """Valida el contenido y devuelve una copia JPEG pequeña sin metadatos."""
    limite = 5 * 1024 * 1024
    contenido = archivo.read(limite + 1)
    if len(contenido) > limite:
        raise ValueError("Elige una foto de 5 MB o menos.")
    try:
        with Image.open(BytesIO(contenido), formats=["JPEG", "PNG", "WEBP"]) as imagen:
            if imagen.width * imagen.height > 25_000_000:
                raise ValueError("La resolución es demasiado alta. Reduce la foto a 25 megapíxeles o menos.")
            imagen.thumbnail((1280, 1280))
            copia = ImageOps.exif_transpose(imagen).convert("RGBA")
            fondo = Image.new("RGB", copia.size, "white")
            fondo.paste(copia, mask=copia.getchannel("A"))
            salida = BytesIO()
            fondo.save(salida, format="JPEG", quality=85)
            return salida.getvalue()
    except (OSError, SyntaxError, Image.DecompressionBombError) as error:
        raise ValueError("No se ha podido leer la foto. Elige un archivo JPG, PNG o WebP válido.") from error


def validar_receta(campos, categorias):
    errores = {}
    for campo, texto in campos.items():
        if not texto:
            errores[campo] = "Completa este campo."
    if campos["categoria"] not in categorias:
        errores["categoria"] = "Elige una categoría de la lista."
    try:
        if int(campos["tiempo"]) < 1:
            raise ValueError
    except ValueError:
        errores["tiempo"] = "Indica un número entero de minutos, mayor que cero."
    return errores


def buscar_por_id(recetas, receta_id):
    """Devuelve la receta con ese ID, o None si no existe."""
    for receta in recetas:
        if receta["id"] == receta_id:
            return receta
    return None


def normalizar(texto):
    letras = unicodedata.normalize("NFD", texto.casefold())
    return "".join(letra for letra in letras if not unicodedata.combining(letra))


def cinco_mas_populares(recetas):
    # En caso de empate, sorted conserva el orden de publicación.
    return sorted(recetas, key=lambda receta: receta["likes"], reverse=True)[:5]


def calcular_estadisticas(recetas):
    total = len(recetas)
    minutos = sum(receta["tiempo"] for receta in recetas)
    return {
        "total": total,
        "media": round(minutos / total, 1) if total else 0,
        "likes": sum(receta["likes"] for receta in recetas),
    }


def filtrar_recetas(recetas, criterio, valor):
    if criterio == "tiempo":
        minutos = int(valor)
        if minutos <= 0:
            raise ValueError("Tiempo no válido")
        return [receta for receta in recetas if receta["tiempo"] <= minutos]
    consulta = normalizar(valor)
    return [receta for receta in recetas if consulta in normalizar(receta[criterio])]
