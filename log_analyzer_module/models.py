from flask_sqlalchemy import SQLAlchemy
from datetime import datetime 

#SQLChemy nesnesini oluştur.
db = SQLAlchemy()

#Hem normal sistem loglarını hem de Auditor bulgularını tutacak model
class SecurityLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    source = db.Column(db.String(100))  #Örn: 'Auditor Core', 'User Login'
    level = db.Column(db.String(50))     #Örn: 'INFO', 'WARNING', 'ERROR'
    
    #Genel Log Mesajı
    message = db.Column(db.Text, nullable=False)
    
    #Auditor Modülüne özgü alanlar(null olabilir)
    url = db.Column(db.String(255), nullable=True)
    key_name = db.Column(db.String(100), nullable=True)
    finding_type = db.Column(db.String(100), nullable=True)  #JWT_TOKEN, API_KEY vb.
    

   