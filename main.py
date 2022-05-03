from flask import Flask, render_template, request, redirect
import qrcode
from forms import QrForm


app = Flask(__name__)
app.config['SECRET_KEY'] = 'lolmamamialol123'
@app.route('/generate',methods=['GET', "POST"])
@app.route('/generate/',methods=['GET', "POST"])
@app.route('/',methods=['GET', "POST"])
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

@app.route('/result')
def result():
    return render_template("result.html", srcc="some_file.png")


@app.route('/list')
def list():
    return render_template("list.html")

@app.route('/profile')
def form():
    return render_template("form.html")

if __name__ == '__main__':
    app.run()