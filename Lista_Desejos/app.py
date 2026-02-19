from flask import Flask, render_template, request, redirect, url_for, flash
from models.database import init_db
from models.tarefa import Desejo

app = Flask(__name__)
app.secret_key = "must-watch-lista-secreta-2026"

init_db()


# ── Rotas ─────────────────────────────────────────────────


@app.route("/")
def home():
    total = len(Desejo.listar_todos())
    return render_template("home.html", titulo="Must Watch", total=total)


@app.route("/desejos", methods=["GET", "POST"])
def listar_desejos():
    if request.method == "POST":
        titulo = request.form.get("titulo", "").strip()
        data_limite = request.form.get("data-limite", "") or None
        categoria = request.form.get("categoria", "Geral")
        prioridade = int(request.form.get("prioridade", 1))

        if titulo:
            desejo = Desejo(titulo, data_limite, categoria, prioridade)
            desejo.salvar()
            flash(f'"{titulo}" adicionado à lista!', "sucesso")
        else:
            flash("O título não pode ficar vazio.", "erro")

        return redirect(url_for("listar_desejos"))

    desejos = Desejo.listar_todos()
    return render_template(
        "lista.html",
        titulo="Lista de Desejos",
        desejos=desejos,
        categorias=Desejo.CATEGORIAS,
    )


@app.route("/excluir/<int:id_desejo>")
def excluir(id_desejo):
    desejo = Desejo.buscar_por_id(id_desejo)
    nome = desejo.titulo
    desejo.excluir()
    flash(f'"{nome}" removido da lista.', "info")
    return redirect(url_for("listar_desejos"))


@app.route("/editar/<int:id_desejo>", methods=["GET", "POST"])
def editar(id_desejo):
    if request.method == "POST":
        titulo = request.form.get("titulo", "").strip()
        data_limite = request.form.get("data-limite", "") or None
        categoria = request.form.get("categoria", "Geral")
        prioridade = int(request.form.get("prioridade", 1))

        desejo = Desejo(titulo, data_limite, categoria, prioridade, id_desejo)
        desejo.atualizar()
        flash(f'"{titulo}" atualizado com sucesso!', "sucesso")
        return redirect(url_for("listar_desejos"))

    desejos = Desejo.listar_todos()
    selecionado = Desejo.buscar_por_id(id_desejo)
    return render_template(
        "lista.html",
        titulo=f"Editando: {selecionado.titulo}",
        desejos=desejos,
        categorias=Desejo.CATEGORIAS,
        selecionado=selecionado,
    )


if __name__ == "__main__":
    app.run(debug=True)
