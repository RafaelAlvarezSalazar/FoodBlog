import random

from flask import Flask, Response, abort, redirect, render_template, request, url_for

from datos import categorias, fotos_subidas, recetas
from funciones import (buscar_por_id, calcular_estadisticas, cinco_mas_populares,
                       filtrar_recetas, normalizar, preparar_foto, validar_receta)

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 8 * 1024 * 1024


@app.template_global()
def url_foto(receta):
    if receta["id"] in fotos_subidas:
        return url_for("foto_publicada", receta_id=receta["id"])
    if receta["foto"]:
        return url_for("static", filename="fotos/" + receta["foto"])


@app.get("/receta/<int:receta_id>/foto")
def foto_publicada(receta_id):
    if receta_id not in fotos_subidas:
        abort(404)
    return Response(fotos_subidas[receta_id], mimetype="image/jpeg")


@app.get("/")
def inicio():
    return render_template("inicio.html", ultimas=recetas[-3:][::-1])


@app.get("/sorprendeme")
def sorprendeme():
    receta = random.choice(recetas)
    respuesta = redirect(url_for("detalle", receta_id=receta["id"]))
    respuesta.cache_control.no_store = True
    return respuesta


@app.get("/recetas")
def listado():
    return render_template("listado.html", recetas=recetas)


@app.get("/receta/<int:receta_id>")
def detalle(receta_id):
    receta = buscar_por_id(recetas, receta_id)
    if receta is None:
        abort(404)
    return render_template("detalle.html", receta=receta)


@app.post("/receta/<int:receta_id>/like")
def dar_like(receta_id):
    receta = buscar_por_id(recetas, receta_id)
    if receta is None:
        abort(404)
    receta["likes"] += 1
    return redirect(url_for("detalle", receta_id=receta_id, _anchor="votos"), code=303)


@app.get("/populares")
def ranking():
    return render_template("ranking.html", populares=cinco_mas_populares(recetas))


@app.get("/estadisticas")
def estadisticas():
    return render_template("estadisticas.html", resumen=calcular_estadisticas(recetas))


@app.route("/publicar", methods=["GET", "POST"])
def publicar():
    campos = {campo: request.form.get(campo, "").strip() for campo in
              ("nombre", "pais", "categoria", "tiempo", "ingredientes", "preparacion")}
    errores = {}
    if request.method == "POST":
        errores = validar_receta(campos, categorias)
        archivo = request.files.get("foto")
        foto = None
        if archivo and archivo.filename:
            try:
                foto = preparar_foto(archivo)
            except ValueError as error:
                errores["foto"] = str(error)
        if not errores:
            nuevo_id = max((r["id"] for r in recetas), default=0) + 1
            receta = dict(campos, id=nuevo_id, tiempo=int(campos["tiempo"]), likes=0, foto=None)
            recetas.append(receta)
            if foto is not None:
                fotos_subidas[nuevo_id] = foto
            return redirect(url_for("detalle", receta_id=nuevo_id), code=303)
    return render_template("publicar.html", campos=campos, categorias=categorias,
                           errores=errores), 422 if errores else 200


@app.get("/buscar")
def buscar():
    criterios = {"nombre": "Nombre", "pais": "País", "categoria": "Categoría", "tiempo": "Tiempo máximo (minutos)"}
    criterio = request.args.get("criterio", "nombre")
    valor = request.args.get("valor", "").strip()
    opciones = {campo: sorted({r[campo] for r in recetas}) for campo in criterios}
    resultados = None
    error = None
    if criterio not in criterios:
        criterio = "nombre"
        error = "Elige uno de los criterios disponibles."
    elif "valor" in request.args and "cambiar" not in request.args:
        if not valor:
            error = "Selecciona una opción para buscar."
        else:
            # Reconoce también enlaces antiguos, por ejemplo «mexico» sin tilde.
            for opcion in opciones[criterio]:
                if normalizar(str(opcion)) == normalizar(valor):
                    valor = str(opcion)
                    break
            try:
                resultados = filtrar_recetas(recetas, criterio, valor)
            except ValueError:
                error = "Escribe el tiempo máximo en minutos, con un entero positivo."
    return render_template("buscar.html", criterios=criterios, criterio=criterio,
                           opciones=opciones, valor=valor, resultados=resultados, error=error)


@app.errorhandler(404)
def no_encontrada(error):
    return render_template("404.html"), 404


@app.errorhandler(413)
def envio_demasiado_grande(error):
    return render_template("publicar.html", campos={}, categorias=categorias,
                           errores={"foto": "El envío es demasiado grande. Elige una foto de 5 MB o menos."}), 413


if __name__ == "__main__":
    app.run()
