from flask import Flask, redirect, url_for, render_template, request
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash, check_password_hash
import os
from flask_mysqldb import MySQL
from flask_login import LoginManager, login_user, login_required, logout_user, UserMixin
load_dotenv()

app = Flask(__name__)

app.config["MYSQL_USER"] = os.getenv("user")
app.config["MYSQL_PASSWORD"] = os.getenv("password")
app.config["MYSQL_HOST"] = os.getenv("host")
app.config["MYSQL_DB"] = os.getenv("db")
app.secret_key = os.getenv("secret_key")

mysql = MySQL(app)

#### CONFIGURACION FLASK - LOGIN ###########
class User(UserMixin):
    def __init__(self, id, email):
        self.id = id
        self.email = email

## ACA INICIAMOS FUNCION LOGINMANGER Y INICIAMOS LA APP
login_manager = LoginManager()
login_manager.init_app(app)

# VISTA QUE MOSTRARE SI PERSONA NO ESTA AUTENTICADA
login_manager.login_view = "login"

#CARGAR EL USUARIO EN EL FLASK LOGIN 
@login_manager.user_loader
def load_user(user_id):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM admins WHERE id = %s", (int(user_id),))
    user = cursor.fetchone()
    if user:
        return User(id=user[0], email=user[1]) 
    return None
    
    
#### RUTAS PARA LOGIN Y REGISTER ########

@app.route("/")
def home():
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        cursor = mysql.connection.cursor()
        email = request.form["email"]
        password = request.form["password"]
        cursor.execute("SELECT * from admins where email = (%s)",(email,))
        user = cursor.fetchone()
        
        if user and check_password_hash(user[2], password):
            usuario = User(id=user[0], email=user[1])
            login_user(usuario)
            return redirect(url_for("books"))

    
        
    return render_template("login.html")


@app.route("/register",methods=["GET", "POST"])
def register():
    if request.method == "POST":
        cursor = mysql.connection.cursor()
        email = request.form["email"]
        password = generate_password_hash(request.form["password"])
        phone = request.form["phone"]
        print(email, password, phone)
        cursor.execute("INSERT INTO admins VALUES (NULL, %s, %s, %s)",(email, password, phone,))
        mysql.connection.commit()
        return redirect(url_for("login"))
       
        
    return render_template("register.html")

################### RUTAS PARA GESTION DE LIBROS ##########################

@app.route("/books",methods=["GET", "POST"])
@login_required
def books():
    if request.method == "POST":
        cursor = mysql.connection.cursor()
        
        nombre_libro = request.form["nombre"]
        categoria_libro = request.form["categoria"]
        autor_libro = request.form["autor"]
        cursor.execute("INSERT INTO books VALUES (NULL, %s, %s, %s, %s)",(nombre_libro, categoria_libro, autor_libro, 2,))
        mysql.connection.commit()
        return redirect(url_for("books"))
    
    if request.method == "GET":
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM books")
        libros = cursor.fetchall()
        return render_template("books.html", libros = libros)
    

@app.route("/edit/<string:id>",methods=["GET", "POST"])
@login_required
def edit(id):
    if request.method == "GET":
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * from books where id = (%s)", (id,))
        libroencontrado = cursor.fetchone()
        print(libroencontrado)
        return render_template("edit.html", libro = libroencontrado)
    
    if request.method == "POST":
        cursor = mysql.connection.cursor()
        nombre_libro = request.form["nombre"]
        categoria_libro = request.form["categoria"]
        autor_libro = request.form["autor"]
        cursor.execute("UPDATE books set name = %s, category = %s, autor = %s where id = %s",(nombre_libro, categoria_libro, autor_libro, id,))
        mysql.connection.commit()
        return redirect(url_for("books"))
       


@app.route("/delete/<string:id>",methods=["POST"])
@login_required
def delete(id):
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM books where id = (%s)", (id,))
    mysql.connection.commit()
    print("Libro eliminado", id)
    return redirect(url_for("books"))

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))
    


##########################################################

@app.route("/recovery")
def recovery():
    return render_template("recovery.html")


############################################################3

if __name__ == "__main__":
    app.run(debug=True, port=3030, host="localhost")