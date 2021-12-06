from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

# Create a Flask Instance
app = Flask(__name__)
app.config['SECRET_KEY'] = "mysecretkey"

# Create a Form Class


# Create a route decorator
@app.route('/')
def index():
	return render_template("base.html")

@app.route('/user/<name>')
def user(name):
	return render_template("user.html", user_name=name)

# Error Pages
@app.errorhandler(404)
def page_not_found(e):
	return render_template("404.html"), 404

# Internal Server Error
@app.errorhandler(500)
def page_not_found(e):
	return render_template("500.html"), 500
