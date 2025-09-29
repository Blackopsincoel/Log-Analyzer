from flask import Flask
import os

# Modülleri import ediyoruz (Blueprint yapısı)
from auditor_module.views import auditor_bp
from log_analyzer_module.models import db, SecurityLog
from log_analyzer_module.views import log_bp 

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    
    # Veritabanı yapılandırması (SQLite ile hızlı prototipleme)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(app.instance_path, 'log_data.db')
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = 'guvenli_anahtar'

    # Veritabanı ve Blueprint entegrasyonu
    db.init_app(app)

    # Blueprint'leri kaydet (Modüller arası veri akışı)
    app.register_blueprint(auditor_bp, url_prefix='/auditor')
    app.register_blueprint(log_bp, url_prefix='/logs') # Log Analiz ve Raporlama

    # Uygulama bağlamında veritabanını oluştur
    with app.app_context():
        # instance klasörünün varlığını kontrol et
        try:
            os.makedirs(app.instance_path)
        except OSError:
            pass
            
        db.create_all()
        
        # Örnek bir sistem logu ekleme
        if not SecurityLog.query.filter_by(source='System').first():
            db.session.add(SecurityLog(level='INFO', source='System', message='Unified Security Auditor başlatıldı.'))
            db.session.commit()

    @app.route('/')
    def index():
        return ('<h1>Unified Web Security Auditor & Log Analyzer Çalışıyor</h1>'
                '<p>Auditor API: <a href="/auditor/logs">/auditor/logs</a> (Bulguları Gör)</p>'
                '<p>Log Analiz Arayüzü: <a href="/logs">/logs</a> (Raporlama)</p>')

    return app

if __name__ == '__main__':
    # Flask ile ilgili dosyaların bulunduğu instance klasörünü oluştur
    if not os.path.exists('instance'):
        os.makedirs('instance')
    
    app = create_app()
    app.run(debug=True, port=5000)