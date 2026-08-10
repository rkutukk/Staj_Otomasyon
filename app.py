from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/academic-login")
def academic_login():
    return render_template("academic_login.html")


@app.route("/student-login", methods=["GET", "POST"])
def student_login():

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # Şimdilik test kullanıcı bilgileri
        if username == "ogrenci" and password == "1234":
            return redirect(url_for("student_home"))

        return render_template(
            "student_login.html",
            error="Kullanıcı adı veya şifre hatalı."
        )

    return render_template("student_login.html")


@app.route("/student")
def student_home():
    return render_template("student_home.html")

@app.route("/application")
def application():
    return render_template("application.html")


if __name__ == "__main__":
    app.run(debug=True)