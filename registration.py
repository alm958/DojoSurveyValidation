from flask import Flask, render_template, request, redirect, flash, session
from datetime import date, datetime, timedelta
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
name_exclude_regex = re.compile(r'[0-9~`!@#$%^&*()_+=|";:?/.>,<\\]')
hyphenstart = re.compile(r'^-')
hyphenend = re.compile(r'-$')
pwdregex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z]).+$')
app = Flask(__name__)
app.secret_key = 'supersecret'
# our index route will handle rendering our form
@app.route('/')
def index():
    return render_template("index.html")

# this route will handle our form submission
# notice how we defined which HTTP methods are allowed by this route
@app.route('/process', methods=['POST'])
def process():
    today = date.today()
    mindob = today.replace(year=(today.year - 21))
    session['firstname']  = request.form['firstname']
    session['lastname']   = request.form['lastname']
    session['email']      = request.form['email']
    session['dob']        = request.form['dob']
    session['psw']        = request.form['password']
    session['pswconfirm'] = request.form['confirmation']
    #Pretty good, Anthony, but do you need to save all the form fields into session before you start validating?  You could save code by not putting anything in session until validating the form
    errors = False
    if len(request.form['email']) > 0 and not EMAIL_REGEX.match(request.form['email']):
        errors = True
        flash("Invalid e-mail address. Enter e-mail.")
    if len(request.form['firstname']) > 0 and ( name_exclude_regex.search(request.form['firstname']) or hyphenstart.search(request.form['firstname']) or hyphenend.search(request.form['firstname'])):
        errors = True
        flash("Invalid first name. Enter valid name. If your name contains numbers or special charaters I am sorry...on many levels")
    if len(request.form['lastname']) > 0 and ( name_exclude_regex.search(request.form['lastname']) or hyphenstart.search(request.form['lastname']) or hyphenend.search(request.form['lastname'])):
        errors = True
        flash("Invalid last name. Enter valid name. If your name contains numbers or special charaters I am sorry...on many levels")
    for k, v in request.form.items():
        if len(v) < 1: #I would check the length of all the fields (like you're doing here) first before doing your other checks up top
            errors = True
            flash(k +' is required and cannot be empty')
    if len(request.form['dob']) > 0:
        inputdob = datetime.strptime(request.form['dob'], "%Y-%m-%d").date()
        if inputdob > mindob:
            error = True
            flash('You must be over 21 years of age to register.', 'tooyoung')
            return render_template('options.html')
    if len(request.form['password']) > 0 :
        if len(request.form['password']) < 8:
            session.pop('psw', None)
            session.pop('pswconfirm',None)
            error = True
            flash('Password must be at least 8 characters in length.')
        if not pwdregex.match(request.form['password']):
            session.pop('psw', None)
            session.pop('pswconfirm',None)
            error = True
            flash('Password must contain at least one upper case and one lower case letter. Enter valid password.')
        if not request.form['password'] == request.form['confirmation']:
            session.pop('psw', None)
            session.pop('pswconfirm',None)
            error = True
            flash('Password confirmation does not match password.  reenter valid passwords.')
    if errors:
        return redirect('/')
    return render_template('show.html')

@app.route('/reset', methods=['POST','get'])
def reset():
    session.pop('firstname',None)
    session.pop('lastname',None)
    session.pop('email', None)
    session.pop('dob',None)
    session.pop('psw', None)
    session.pop('pswconfirm',None)
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
