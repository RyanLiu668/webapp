from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
ENV = ''

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:453v7v8a@localhost/web-app'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://mghjwjsadynqag:0a932625c9c1c4081b42f1e128b8df1f72fa969ac3a2195a6f1376f7c214e732@ec2-54-83-9-169.compute-1.amazonaws.com:5432/dvm5tfpkqqa1m'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Feedback(db.Model):
    __tablename__ = 'feedback'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=False)
    number = db.Column(db.Integer, unique=False)

    def __init__(self, name,number):
        self.name = name
        self.number = number

#SETTING THE ROUTES 
@app.route('/')
def index():
    dbd= Feedback.query.all()
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        name = request.form['name']
        number = request.form["rannumber"]
        if name == '':
            return render_template('index.html', message='Please enter required fields')

        if number.isnumeric() == False:
            return render_template('index.html', message='Please enter a number')
        
        number = int(number)
        if db.session.query(Feedback).filter(Feedback.name == name).count() == 0:
            data = Feedback(name, number)
            db.session.add(data)
            db.session.commit()
            return render_template('success.html')

        return render_template('index.html', message='You have already submitted ')
        
@app.route('/pic')
def pic():
    return render_template('pic.html')
#To run the program
if __name__ == '__main__':
    app.run()