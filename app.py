from flask import Flask, render_template, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

# Create a Flask Instance
app = Flask(__name__)
app.config['SECRET_KEY'] = "mysecretkey"

# Create a Form Class
class nameForm(FlaskForm):
	name = StringField("Whats Your Name?", validators=[DataRequired()])
	submit = SubmitField("Submit")


# Create a route decorator
@app.route('/')
def index():
	flash("Welcome to my Website!")
	return render_template("index.html")

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

# Create Name Page
@app.route('/name', methods=['GET', 'POST'])
def nameform():
	name = None
	form = nameForm()
	# VALIDATE FORM
	if form.validate_on_submit():
		name = form.name.data
		form.name.data = ''
		flash("Form Submitted Successfully")

	return render_template("nameform.html", 
		name=name,
		form=form)
