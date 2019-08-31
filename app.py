from flask import Flask, render_template, session, redirect, request, url_for, flash
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data1.db'
app.secret_key = 'heremykey'
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), nullable=False)
    password = db.Column(db.String(250), nullable=False)
    Class = db.Column(db.String(250), nullable=False)
    year = db.Column(db.String(250), nullable=False)
    city = db.Column(db.String(250), nullable=False)
    country = db.Column(db.String(250), nullable=False)
    middlename = db.Column(db.String(250), nullable=True)
    mobileno = db.Column(db.String(250), nullable=True)

# def __init__(self, name, email, password, Class, year, city, country, middlename, mobileno):
#     self.name = name
#     self.email = email
#     self.password = password
#     self.Class = Class
#     self.year = year
#     self.city = city
#     self.country = country
#     self.middlename = middlename
#     self.mobileno = mobileno

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/auth', methods = ["POST", "GET"])
def auth():
    logemail = request.form['email']
    logpassword = request.form['password']

    data = User.query.filter_by(email = logemail, password = logpassword).first()
    if data is not None:
        session['logged_in'] = True
        return redirect('/user')
    else:
        return "Login Failed"    


@app.route('/up', methods = ["POST", "GET"])
def up():
    return render_template('signup.html')

@app.route('/add', methods = ["POST", "GET"])
def add():
    if request.method == 'POST':
        if not request.form['email'] or not request.form['password'] or not request.form['mobileno']:
            flash("All are required fields")
        else:
            newname = request.form['name']
            newemail = request.form['email']
            newpassword = request.form['password']
            newmobileno = request.form['mobileno']
            new_user = User(name = newname, email = newemail, password = newpassword, mobileno = newmobileno)

            db.session.add(new_user)
            db.session.commit()
            flash('Success')
    return redirect('/login') 

@app.route('/user')
def user():
    tasks = User.query.order_by(User.id).all()
    return render_template('user.html', tasks=tasks)


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    task = User.query.get_or_404(id)

    if request.method == 'POST':
        task.name = request.form['name']
        task.Class = request.form['class']
        task.year = request.form['year']
        task.city = request.form['city']
        task.country = request.form['country']

        try:
            db.session.commit()
            return redirect('/user')
        except:
            return 'There was an issue updating your task'

    else:
        return render_template('update.html', task=task)




@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    task = User.query.get(id)
    db.session.delete(task)
    db.session.commit()
    return redirect('/user')

    # else:
    #     return render_template('user.html')


if __name__ == "__main__":
    app.run(debug=True)
