from . import db

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.String(50), nullable=False)
    contact = db.Column(db.String(15), nullable=False)
    treatment = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
