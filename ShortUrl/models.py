#Flask’ta veritabanı işlemleri yapabilmek için SQLAlchemy modülünü import ediyorum.”
from flask_sqlalchemy import SQLAlchemy
#Daha sonra SQLAlchemy’den bir veritabanı nesnesi oluşturman gerekiyor.
db = SQLAlchemy()

class URL(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    original_url = db.Column(db.String(500), nullable = False)
    short_url = db.Column(db.String(10), nullable = False)
    visit_count = db.Column(db.Integer, default = 0)
    




