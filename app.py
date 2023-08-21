from flask import Flask,render_template,request,redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime



app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///blogs.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)




app.app_context().push()

def create_app():
    app = Flask(__name__)

    with app.app_context():
        init_db()

    return app



class Blog(db.Model):
    sno=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(30),nullable=False)
    content=db.Column(db.String(1000),nullable=False)
    author=db.Column(db.String(30),nullable=False)
    date=db.Column(db.DateTime,default=datetime.utcnow)

    def __repr__(self)->str:
        return f"{self.sno}-{self.title}"








@app.route('/')
def home():
    ob=Blog.query.all()
    print(ob)
    return render_template('index.html',ob=ob)



@app.route('/about')
def about():
    return "<h2 style='text-align:center;color:blue'>This is about page</h2>"



@app.route('/post')
def post():
    return render_template('postBlog.html')



@app.route('/submitBlog',methods=['POST','GET'])
def submitBlog():
    if request.method=='POST':
        title=request.form['title']
        content=request.form['blogContent']
        author=request.form['author']

        ob=Blog(title=title,content=content,author=author)
        db.session.add(ob)
        db.session.commit()
    return redirect(url_for('home'))



@app.route('/deletedata/<int:sno>')
def deletedate(sno):
    ob=Blog.query.filter_by(sno=sno).first()
    db.session.delete(ob)
    db.session.commit()
    return redirect(url_for('home'))



if __name__=="__main__":
    app.run(debug=True,port=8000)