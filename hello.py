from datetime import datetime, timezone
import os
import re

from flask import Flask, jsonify, redirect, render_template, request, session, url_for
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email, ValidationError

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get(
    "SECRET_KEY", "development-key-change-before-deployment"
)
bootstrap = Bootstrap(app)
moment = Moment(app)


def uoft_email(form, field):
    if "utoronto" not in field.data.lower():
        raise ValidationError("Please enter a UofT email address containing 'utoronto'.")


class NameEmailForm(FlaskForm):
    name = StringField("What is your name?", validators=[DataRequired()])
    email = StringField(
        "What is your UofT email address?",
        validators=[
            DataRequired(),
            Email(message="Please enter a valid email address."),
            uoft_email,
        ],
    )
    submit = SubmitField("Submit")


@app.route("/", methods=["GET", "POST"])
def index():
    form = NameEmailForm()
    if form.validate_on_submit():
        session["name"] = form.name.data
        session["email"] = form.email.data
        return redirect(url_for("chat"))

    return render_template(
        "index.html",
        form=form,
        name=session.get("name"),
        email=session.get("email"),
        current_time=datetime.now(timezone.utc),
    )


@app.route("/user/<name>")
def user(name):
    return render_template(
        "index.html",
        form=NameEmailForm(),
        name=name,
        email=None,
        current_time=datetime.now(timezone.utc),
    )


@app.route("/chat", methods=["GET", "POST"])
def chat():
    if "name" not in session or "email" not in session:
        if request.method == "POST":
            return jsonify(reply="Please submit your name and UofT email first."), 401
        return redirect(url_for("index"))

    if request.method == "GET":
        return render_template(
            "chat.html",
            name=session["name"],
            email=session["email"],
        )

    data = request.get_json(silent=True) or {}
    message = data.get("message", "").strip()
    if not message:
        return jsonify(reply="Please enter a message."), 400
    if len(message) > 500:
        return jsonify(reply="Please keep your message under 500 characters."), 400

    name_question = re.search(r"\bwhat(?:'s| is) my name\??$", message, re.IGNORECASE)
    name_statement = re.search(
        r"\bmy name is\s+([A-Za-z][A-Za-z' -]{0,49}?)\s*[.!?]*$",
        message,
        re.IGNORECASE,
    )

    if name_question:
        remembered_name = session.get("chat_name")
        if remembered_name:
            reply = f"Your name is {remembered_name}."
        else:
            reply = "I don't know your name yet."
    elif name_statement:
        remembered_name = name_statement.group(1).strip()
        session["chat_name"] = remembered_name
        reply = f"Nice to meet you, {remembered_name}!"
    elif "hello" in message.lower():
        reply = "Hello!"
    else:
        reply = "I don't understand. Try telling me, 'My name is Alice.'"

    return jsonify(reply=reply)


@app.post("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))
