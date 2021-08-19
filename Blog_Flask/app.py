
from flask import Flask, render_template, redirect, request,url_for, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/blog'
db = SQLAlchemy(app)




class OJBlog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False, unique=False)
    content = db.Column(db.Text, nullable=False)
    posted_by = db.Column(db.String(20), nullable=False, default='N/A')
    posted_on = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return self.title

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username  = db.Column(db.String(30), nullable=True)
    phoneno = db.Column(db.BigInteger, nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
 
    def __repr__(self):
        return f"User('{self.email}')"



db.create_all()
db.session.commit()

@app.route('/')
@app.route('/home')
@app.route('/OJ')
def Welcome():
    return render_template('index.html')

@app.route('/posts',  methods=['GET', 'POST'])
def posts():
    if request.method == 'POST':
        post_title = request.form['title']
        if post_title =='':
            message='fields must be entered!'
            return render_template('new_posts.html',msg=message)
        post_content = request.form['post']
        post_author = request.form['author']
        new_post = OJBlog(title=post_title,
                        content=post_content, posted_by=post_author)
        db.session.add(new_post)
        db.session.commit()

        return redirect('/posts')
    else:
        all_posts = OJBlog.query.order_by(OJBlog.posted_on).all()
        return render_template('posts.html', posts=all_posts)

@app.route('/posts/delete/<int:id>')
def delete(id):
    to_delete = OJBlog.query.get_or_404(id)
    db.session.delete(to_delete)
    db.session.commit()
    return redirect('/posts')     

@app.route('/posts/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    to_edit = OJBlog.query.get_or_404(id)
    if request.method == 'POST':
        to_edit.title = request.form['title']
        to_edit.posted_by = request.form['author']
        to_edit.content = request.form['post']
        db.session.commit()
        return redirect('/posts')

    else:
        return render_template('edit.html', post=to_edit)

@app.route('/posts/new', methods=['GET', 'POST'])
def new_post():
    if request.method == 'POST':
        post_title = request.form['title']
        post_content = request.form['post']
        post_author = request.form['author']
        new_post = OJBlog(title=post_title,
                        content=post_content, posted_by=post_author)
        db.session.add(new_post)
        db.session.commit()
        return redirect('/posts')
    else:
        return render_template('new_posts.html')


@app.route('/register', methods =['GET', 'POST'])
def register():
    title = "Create Account"
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        phoneno = request.form['phoneno']
        user = Users(username = username,password = password,email = email,phoneno=phoneno)
        db.session.add(user)
        db.session.commit()
        return redirect('/login')
    else:
        return render_template('registration.html')

#login
@app.route("/login",methods=["GET", "POST"])
def login():
    if request.method == "POST":
        uname = request.form["username"]
        passw = request.form["password"]
        login = Users.query.filter_by(username=uname, password=passw).first()
        if login:
            # session['uname']= uname
            return redirect(url_for("dashboard"))
        else:
            message='invalid credentials'
            return render_template("login.html",message=message)

    return render_template("login.html")

@app.route("/dashboard",methods=["GET", "POST"])
def dashboard():
    return render_template('dashboard.html')

if __name__ == "__main__":
    app.run(debug=True)




