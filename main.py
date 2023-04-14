import base64
import io
import os
import shutil

from PIL import Image
from flask import Flask, render_template, request, redirect, send_from_directory
import qrcode
from forms import QrForm, SignIn, SignUp, Send
from data import db_session
from flask_login import LoginManager, logout_user, login_required, current_user
from data.user import User
from data.qrs import QRC
from flask_login import login_user


app = Flask(__name__)
app.config['SECRET_KEY'] = 'lolmamamialol123'

login_manager = LoginManager()
login_manager.init_app(app)

@app.route('/',methods=['GET', "POST"])
def mamain():
    return redirect("/generate")
@app.route('/generate',methods=['GET', "POST"])
@app.route('/generate/',methods=['GET', "POST"])
def my_form_post():
    form = QrForm()
    if request.method == "POST":
        text = form.name.data
        img = qrcode.make(text)
        type(img)  # qrcode.image.pil.PilImage
        img.save("static/imgs/some_file.png")
        return redirect("/result")
    else:
        text = ""
        img = qrcode.make(text)
        type(img)  # qrcode.image.pil.PilImage
        img.save("static/imgs/some_file.png")
    return render_template("index.html", form=form)

@app.route('/generate_file',methods=['GET', "POST"])
def index_file():
    if request.method == 'GET':
        return render_template("index_photo.html")
    elif request.method == 'POST':
        f = request.files['file']

        img = qrcode.make(f.read())
        type(img)  # qrcode.image.pil.PilImage
        img.save("static/imgs/some_file.png")
        return "Форма отправлена"

@app.route('/result', methods=['GET', 'POST'])
def result():
    form = Send()
    print(1)
    if request.method == "POST":
        db_sess = db_session.create_session()
        qrc = QRC()
        with open('static/imgs/some_file.png', 'rb') as file:
            blob_data = file.read()
        qrc.info = blob_data
        current_user.qrc.append(qrc)
        db_sess.merge(current_user)
        db_sess.commit()
        print('qr')
        return redirect('/list')
    return render_template("result.html", srcc="some_file.png", form=form)



@app.route('/list', methods=['GET', 'POST'])
@login_required
def show():
    db_sess = db_session.create_session()
    qrc = db_sess.query(QRC).filter(QRC.user_id == current_user.id)
    x = 0
    somar = []
    for el in qrc:
        print(el.info)
        img = Image.open(io.BytesIO(el.info))
        try:
            os.makedirs("static/qrs")
        except FileExistsError:
            pass
        img.save(f"static/qrs/qr_user_{x}.jpg")
        somar.append(f"qrs/qr_user_{x}.jpg")
        x += 1

    return render_template('list.html', qrc=qrc, x = x, somar=somar)

@app.route('/login',methods=['GET', "POST"])
def form():
    form = SignIn()
    if request.method == 'POST':
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.name == form.login.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect("/")
        return render_template('form.html',message="Неправильный логин или пароль",form=form)
    else:
        return render_template("form.html", form=form)

@app.route('/registration', methods=['GET', "POST"])
def form1():
    form = SignUp()
    if request.method == 'POST':
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.name == form.login.data).first():
            return render_template('form_reg.html',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.login.data,
            hashed_password=form.password.data,
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('form_reg.html', title='Регистрация', form=form)

@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    try:
        shutil.rmtree("static/qrs")
    except FileNotFoundError:
        pass
    return redirect("/")

@app.route('/save', methods=['GET', 'POST'])
@login_required
def save():
    print(1)
    if request.method == "POST":
        db_sess = db_session.create_session()
        qrc = QRC()
        with open('static/imgs/some_file.png', 'rb') as file:
            blob_data = file.read()
        qrc.info = blob_data
        current_user.qrc.append(qrc)
        db_sess.merge(current_user)
        db_sess.commit()
    else:
        print("23")
    return redirect("/")
if __name__ == '__main__':
    db_session.global_init("db/accounts.db")
    app.run()