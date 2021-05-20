from flask import Flask, render_template, request, redirect, url_for
from sqla_wrapper import SQLAlchemy
import os

app = Flask(__name__)
db_url = os.getenv("DATABASE_URL", "sqlite:///db.sqlite").replace("postgres://", "postgresql://", 1)
db = SQLAlchemy(db_url)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String, unique=False)
    text = db.Column(db.String, unique=False)

db.create_all()

@app.route("/")
def index():
    mensagens = db.query(Message).all()

    return render_template("index.html", mensagens=mensagens)


@app.route("/add-message", methods=["POST"])
def add_message():
    username = request.form.get("username")
    mensagem = request.form.get("mensagem")

    message = Message(author = username, text = mensagem)
    message.save()

    return redirect("/")


if __name__ == '__main__':
    app.run()
