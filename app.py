from flask import Flask , render_template , request , redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


application = Flask(__name__)
application.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(application)


class Todo_class(db.Model):
    sno = db.Column(db.Integer , primary_key=True)
    title = db.Column(db.String(200) , nullable = False)
    description = db.Column(db.String(500) , nullable = False)
    datetime = db.Column(db.DateTime ,default=datetime.utcnow)

    def __repr__ (self) -> str:
        return f"{self.sno} - {self.title}"

        
@application.route('/' , methods = ['GET','POST'] )
def hello_world():
    if request.method == "POST":
        titles = request.form['titles']
        description = request.form['description']
         # made a instance todo_instance of class TODO_class
        todo = Todo_class(title = titles , description = description)
        db.session.add(todo)
        db.session.commit()

    alltodo = Todo_class.query.all()
    # print(alltodo)

    return render_template('index.html', alltodo = alltodo)

# @application.route('/')
# def update():

@application.route('/update/<int:sno>' , methods = ['GET' , 'POST'])
def update(sno):
    if request.method == "POST":
        titles = request.form['titles']
        description = request.form['description']
        todo = Todo_class.query.filter_by(sno=sno).first()
        todo.title = titles
        todo.description = description
        db.session.add(todo)
        db.session.commit()
        return redirect('/')

    todo = Todo_class.query.filter_by(sno=sno).first()
    return render_template('update.html', todo = todo)
   

@application.route('/delete/<int:sno>')
def delete(sno):
    todo = Todo_class.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")



    

if __name__ == "__main__":
    application.run(debug=True)