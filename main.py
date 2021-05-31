import hashlib, uuid
from flask import Flask, render_template, request, redirect, url_for, make_response
from models import Message, User, db

app = Flask(__name__)

db.create_all()

def getUser():
    session_token = request.cookies.get("session_token")
    user = db.query(User).filter_by(session_token=session_token).first()
    return user

@app.route("/")
def index():
    mensagens = db.query(Message).all()

    user = getUser()
    if (user):
        name_user = user.name
    else:
        name_user = None

    return render_template("index.html", mensagens=mensagens, name_user=name_user)

@app.route("/login", methods=["POST"])
def login():
    name = request.form.get("user-name")
    email = request.form.get("user-email")
    password = request.form.get("user-password")

    # hash the password
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    user = db.query(User).filter_by(email=email).first()

    if not user:
        user = User(name=name, email=email, password=hashed_password)
        user.save()

    # check if password is incorrect
    if hashed_password != user.password:
        return "WRONG PASSWORD! Go back and try again."
    elif hashed_password == user.password:
        #create a random session token
        session_token = str(uuid.uuid4())

        #save user session token on db
        user.session_token = session_token
        user.save()

    response = make_response(redirect(url_for('index')))
    response.set_cookie("session_token", session_token, httponly=True, samesite='Strict')

    return response

@app.route("/add-message", methods=["POST"])
def add_message():
    user = getUser()

    mensagem = request.form.get("mensagem")

    message = Message(author = user.name, text = mensagem)
    message.save()

    return redirect("/")


@app.route("/profile", methods=["GET"])
def profile():
    user = getUser()
    if user:
        return render_template("profile.html", user=user)
    else:
        return redirect(url_for("index"))

@app.route("/profile/edit", methods=["GET", "POST"])
def profile_edit():
    user = getUser()

    if request.method == "GET":
        if user:
            return render_template("profile_edit.html", user=user)
        else:
            return redirect(url_for("index"))

    elif request.method == "POST":
        if user:
            name = request.form.get("profile-name")
            email = request.form.get("profile-email")

            # update the user object
            user.name = name
            user.email = email
            # store changes into the database
            user.save()
            return redirect(url_for("profile"))
        else:
            return "You don't have access to this page!"

@app.route("/profile/delete", methods=["GET", "POST"])
def profile_delete():
    user = getUser()

    if request.method == "GET":
        if user:
            return render_template("profile_delete.html", user=user)
        else:
            return redirect(url_for("index"))

    elif request.method == "POST":
        if user:
            user.delete()
            return redirect(url_for("index"))
        else:
            return "You don't have access to this page!"

@app.route("/users", methods=["GET"])
def all_users():
    users = db.query(User).all()

    return render_template("users.html", users=users)


@app.route("/user/<user_id>", methods=["GET"])
def user_details(user_id):
    user = db.query(User).get(int(user_id))
    return render_template("user_details.html", user=user)

if __name__ == '__main__':
    app.run()