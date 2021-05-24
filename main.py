from flask import Flask, render_template, request, redirect, url_for, make_response
from models import Message, User, db

app = Flask(__name__)

db.create_all()

def getUserName():
    email_address = request.cookies.get("email")
    if(email_address):
        user = db.query(User).filter_by(email=email_address).first()
        name_user = user.name
        return name_user
    else:
        return None

@app.route("/")
def index():
    mensagens = db.query(Message).all()
    name_user = getUserName()
    if (name_user):
        return render_template("index.html", mensagens=mensagens, name_user=name_user)
    else:
        return render_template("index.html", mensagens=mensagens)


@app.route("/add-message", methods=["POST"])
def add_message():
    username = getUserName()
    mensagem = request.form.get("mensagem")

    message = Message(author = username, text = mensagem)
    message.save()

    return redirect("/")

@app.route("/login", methods=["POST"])
def login():
    name = request.form.get("user-name")
    email = request.form.get("user-email")

    user = User(name=name, email=email)
    user.save()

    response = make_response(redirect(url_for('index')))
    response.set_cookie("email", email)

    return response


if __name__ == '__main__':
    app.run()
