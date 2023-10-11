from flask_sqlalchemy import SQLAlchemy
from flask import Flask


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:2345@localhost:5432/duka"


db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), unique=True)
    
with app.app_context():
    db.create_all()

@app.route("/")
def heloo():
    return "hi"

app.run(debug=True)
    
