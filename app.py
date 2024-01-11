

from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import date

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    prio = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=date.today)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"
    

@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method=='POST':
        title = request.form['title']
        prio = request.form['prio']
        todo = Todo(title=title, prio=prio)
        db.session.add(todo)
        db.session.commit()
    allTodo = Todo.query.all() 
    return render_template('home.html', allTodo=allTodo)

@app.route('/delete/<int:sno>', methods=['GET', 'POST'])
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')

@app.route('/edit/<int:sno>', methods=['GET', 'POST'])
def edit(sno):
    if request.method == 'POST':
        title = request.form['title']
        prio = request.form['prio']
        todo = Todo.query.filter_by(sno=sno).first()
        todo.title = title
        todo.prio = prio
        db.session.add(todo)
        db.session.commit()
        return redirect('/')
    todo = Todo.query.filter_by(sno=sno).first()
    return render_template('edit.html', todo=todo)
    
with app.app_context():
    db.create_all()

if __name__ == "__main__": 
      app.run(debug=True, port=5000)
