from flask import Flask,render_template,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__) # uygulamamızı oluşturduk
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////Users/asuma/Desktop/tech_istanbul_bootcamp_projesi/TodoApp/todo.db" # veritabanımızı oluşturduk
db = SQLAlchemy(app) # nesne üzerinden db oluşturduk bunun üzerinden veritabanı işlemleri yapacağız.

@app.route("/")
def index():
    todos = Todo.query.all() # veritabanındaki verileri alıyoruz liste içinde sözlük = todos
    return render_template("index.html",todos = todos) 

@app.route("/add", methods = ["POST"])
def addTodo():
    title = request.form.get("title")
    content = request.form.get("content")

    newTodo = Todo(title = title,content = content,complete = False)
    
    db.session.add(newTodo)
    db.session.commit()
    "Ekleme islemi bitti ve veritabanına eklendi. Bir önceki sayfaya dönmeli"
    return redirect(url_for("index"))

@app.route("/complete/<string:id>", methods = ["GET"])
def completedTodo(id):

    todo = Todo.query.filter_by(id=id).first()
    if todo.complete == False:
         todo.complete = True
    else:
         todo.complete = False

    db.session.commit()
    return redirect(url_for("index"))

@app.route("/delete/<string:id>",methods = ["GET"])
def deleteTodo(id):
    todo = Todo.query.filter_by(id=id).first()
    db.session.delete(todo)
    db.session.commit()

    return redirect(url_for("index"))

@app.route("/detail/<string:id>" , methods = ["GET"])
def detailTodo(id):
    todo = Todo.query.filter_by(id=id).first()
    
    return render_template("detail.html",todo = todo)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100))
    content = db.Column(db.Text)
    complete = db.Column(db.Boolean)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)

   