
from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime


app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS '] = False
db = SQLAlchemy(app)

class Todo(db.Model):# created database coloumn
     Sno=db.Column(db.Integer, primary_key = True)
     title=db.Column(db.String(200),nullable=False) #coc it can not be null
     desc=db.Column(db.String(500),nullable=False)
     date_created=db.Column(db.DateTime,default=datetime.utcnow)
     
     def __repr__(self) -> str:  #what u want to see from database object
        return f"{self.Sno} - {self.desc}"

@app.route('/',methods=['GET','POST'])
def hello_world():
    if request.method=='POST':
        title=request.form['title']#title variable me form ka title aa raha hai
        desc=request.form['desc']
        todo =Todo(title=title, desc=desc)#yaha todo ke title me title assign kar diye
        db.session.add(todo)#here we have added it into data base
        db.session.commit()
    allTodo=Todo.query.all()#complete todo allTodo me aa gaya
    return render_template('index.html',allTodo=allTodo)#all this will be available in our index.html
    # return 'Hello, Ravi!'

@app.route('/update/<int:Sno>',methods=['GET','POST'])
def upodate(Sno):
    if request.method=='POST':
        title=request.form['title']
        desc=request.form['desc']
        todo= Todo.query.filter_by(Sno=Sno).first() #coz exiting todo ko update karna hai
        todo.title=title
        todo.desc=desc
        db.session.add(todo)
        db.session.commit()
        return redirect('/')
    todo= Todo.query.filter_by(Sno=Sno).first() #this will paas the selected Sno data to todo
    return render_template('update.html',todo=todo)

@app.route('/delete/<int:Sno>')
def delete(Sno):
    todo= Todo.query.filter_by(Sno=Sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")


if __name__=="__main__":
    app.run(debug=True)
    