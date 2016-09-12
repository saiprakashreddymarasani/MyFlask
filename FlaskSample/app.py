from flask import Flask, flash, render_template, request, session
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)


class User:
    def __init__(self , username ,password ):
        self.username = username
        self.set_password(password)
        self.temppass='password'

    # generate hashpassword from generate_password_hash
    def set_password(self , password):
        self.password = generate_password_hash(password)

    def check_password(self,password):
        print(check_password_hash(self.password , self.temppass))
        return check_password_hash(self.password , self.temppass)

    # check for authentication
    def is_authenticated(self):
        return self.loginValidate()

    # validate credentials based on username and password(hash). Username is provided ad admin
    def loginValidate(self):
        if self.username=="admin" and self.check_password(self.temppass):
            return True
        else:
            return False

    # static method decorator so that I can call this method from class
    @staticmethod
    def logout():
        session['logged_in'] = False


@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return "Hi Daniel!  <a href='/logout'>Logout</a>"


@app.route('/login', methods=['POST'])
def do_admin_login():

    password=request.form['password']
    username=request.form['username']
    user = User(username=username, password=password)

    if user.is_authenticated():
        session['logged_in'] = True
    else:
        flash('wrong password!')
    return home()


@app.route("/logout")
def logout():
    User.logout()
    return home()


if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True, host='127.0.0.1', port=4000)
