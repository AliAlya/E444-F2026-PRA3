from datetime import datetime, timezone
import os

from flask import Flask, redirect, render_template, session, url_for
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
        return redirect(url_for("index"))

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
