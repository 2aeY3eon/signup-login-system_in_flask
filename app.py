from flask import Flask
from flask import render_template
from flask import request
from flask import url_for
import re
import os

def is_username_valid(username):
    valid = re.findall(r"^\S[a-zA-Z0-9~!@#$%^&*_-]+$", username)
    return bool(valid)

def is_password_valid(password):
    valid = re.findall(r"^[a-zA-Z0-9~!@#$%^&*_-]{8,}$", password)
    return bool(valid)

def user_signup(userId, userPw, userName):
    
    # 비번 길이, 대소문자, 특수문자 체크
    if not is_username_valid(userId):
        print("Invalid Username : Not Match To RegEx")
        return "Invalid userId : Not Match To RegEx"
    if not is_password_valid(userPw):
        print("Invalid userPw : Not Match To RegEx")
        return "Invalid userPw : Not Match To RegEx"
    if not is_username_valid(userName):
        print("Invalid userName : Not Match To RegEx")
        return "Invalid userName : Not Match To RegEx"

    # 파일 존재하지 않을시
    if not os.path.exists("account_db.txt"):
        f = open("account_db.txt", "x")
        f.close()

    # 중복 유저 체크
    f = open("account_db.txt", "r")
    is_account_exsist = re.findall(r"\b"+userId+r"\b", f.read())
    is_account_exsist += re.findall(r"\b"+userName+r"\b", f.read())
    f.close()

    if is_account_exsist:
        print("User's Account Already Exists!")
        return "User's Account Already Exists!"
    else: # 유저 회원가입
        f = open("account_db.txt", "a")
        f.write(f"{userId} {userPw} {userName}\n")
        print(f"User {userName}'s account has been successfully registered!")
        f.close()
        return 1

def user_login(userId, userPw, userName):
    # valid check
    if not is_username_valid(userId):
        print("Invalid Username : Not Match To RegEx")
        return "Invalid userId : Not Match To RegEx"
    if not is_password_valid(userPw):
        print("Invalid userPw : Not Match To RegEx")
        return "Invalid userPw : Not Match To RegEx"
    if not is_username_valid(userName):
        print("Invalid userName : Not Match To RegEx")
        return "Invalid userName : Not Match To RegEx"

    # login check
    f = open("account_db.txt", "r")
    if f"{userId} {userPw} {userName}" in f.read():
        print("Successfully logged in!")
        f.close()
        return 1
    else:
        print("Login Failed..")
        f.close()
        return "Login Failed.."

app = Flask(__name__)

@app.route("/")
@app.route("/index")
def index():
    return render_template('index.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        userId = request.form['userId']
        userPw = request.form['userPw']
        userName = request.form['userName']

        result = user_login(userId, userPw, userName)
        if result == 1:
            return render_template('login.html', message="Successfully logged in!", userName=userName)
        else:
            return render_template('login.html', message=result)

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')
    elif request.method == 'POST':
        userId = request.form['userId']
        userPw = request.form['userPw']
        userName = request.form['userName']

        result = user_signup(userId, userPw, userName)
        if result == 1:
            return render_template('signup.html', message=f"User {userName}'s account has been successfully registered!")
        else:
            return render_template('signup.html', message=result)



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)