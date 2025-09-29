from flask import render_template, request
from .__init__ import log_bp
from .models import db, SecurityLog 
from sqlalchemy import func

# Basit Görselleştirme (Simülasyon): Log seviyesine göre sayım yapar

def get_log_counts():
    """Veritabanındaki log seviyelerini sayısını döner."""
    counts = db.session.query(
        SecurityLog.level,
        func.count(SecurityLog.level)
    ).group_by(SecurityLog.level).all()
    
    # [('INFO', 5), ('CRITICAL_SECURITY', 12)] formatını döndürür.
    return counts  

@log_bp.route('/', methods=['GET'])
def log_dashboard():
    """Genel Log ve Güvenlik Bulguları Raporlama Ekranı."""

    # Filtreleme: Sadece CRITICAL_SECURITY veya tüm logları çek. <- Hata 2 düzeltildi
    filter_level = request.args.get('level', 'CRITICAL_SECURITY')

    if filter_level == 'ALL':
        logs = SecurityLog.query.order_by(SecurityLog.timestamp.desc()).limit(100).all()
    else:
        logs = SecurityLog.query.filter_by(level=filter_level).order_by(SecurityLog.timestamp.desc()).all()
    
    # Görselleştirme Verisi
    log_counts = get_log_counts()

    return render_template('log_dashboard.html', logs=logs, log_counts=log_counts, current_filter=filter_level)

@log_bp.route('/security', methods=['GET'])
def security_report():
    """Sadece Web Security Auditor bulgularını gösteren özel rapor."""

    security_logs = SecurityLog.query.filter_by(level='CRITICAL_SECURITY').order_by(SecurityLog.timestamp.desc()).all()
    
    # Bulgu tipine göre gruplama (Görselleştirme verisi için) <- Hata 3 düzeltildi
    finding_counts = db.session.query(
        SecurityLog.finding_type,
        func.count(SecurityLog.finding_type)
    ).filter_by(level='CRITICAL_SECURITY').group_by(SecurityLog.finding_type).all()

    return render_template('security_report.html', logs=security_logs, finding_counts=finding_counts)