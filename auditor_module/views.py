from flask import Blueprint, request, jsonify
import threading
from .auditor_core import audit_website 
from log_analyzer_module.models import db, SecurityLog 
from .__init__ import auditor_bp 

def run_audit_in_thread(url, app):
    """
    Auditor'ı ayrı bir thread'de çalıştırır. 
    Veritabanı işlemleri için Flask uygulama bağlamını kullanır.
    """
    print(f"THREAD BAŞLATILDI: {url} denetleniyor...")
    
    # Veritabanı işlemleri için uygulama bağlamı zorunludur.
    with app.app_context():
        results = audit_website(url)
        
        # Sonuçları veritabanına kaydet
        for result in results:
            new_log = SecurityLog(
                level=result.get('level', 'INFO'),
                source=result.get('source', 'Auditor'),
                url=result.get('url'),
                key_name=result.get('key_name'),
                finding_type=result.get('finding_type'),
                message=result.get('description', 'Hassas veri bulgusu.') + 
                        f" Key: {result.get('key_name')}, Value: {result.get('value_snippet')}"
            )
            db.session.add(new_log)
        
        db.session.commit()
        
        print(f"THREAD BİTTİ: {url} için {len(results)} bulgu veritabanına kaydedildi.")


@auditor_bp.route('/start', methods=['POST'])
def start_audit():
    """Web denetimini tetikleyen API rotası (POST isteği ile URL beklenir)."""
    
    data = request.get_json()
    target_url = data.get('url')
    
    if not target_url:
        return jsonify({"status": "error", "message": "Lütfen denetlenecek bir 'url' sağlayın."}), 400

    # Thread'e göndermek için ana Flask uygulamasını al
    app = auditor_bp.app 
    
    # Denetimi arka planda başlat
    thread = threading.Thread(target=run_audit_in_thread, args=(target_url, app))
    thread.start()
    
    return jsonify({
        "status": "success",
        "message": f"Denetim başarıyla başlatıldı: {target_url}. Sonuçlar veritabanına kaydedilecektir.",
        "url": target_url
    }), 202 # Kabul edildi, işlem devam ediyor


@auditor_bp.route('/logs', methods=['GET'])
def get_security_logs():
    """Denetimden gelen hassas veri bulgularını (logları) JSON formatında gösteren rota."""
    
    # Sadece CRITICAL_SECURITY loglarını veritabanından çek
    logs = SecurityLog.query.filter_by(level='CRITICAL_SECURITY').all()
    
    # Logları JSON formatına dönüştür
    logs_json = [{
        "id": log.id,
        "timestamp": log.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
        "url": log.url,
        "finding_type": log.finding_type,
        "key_name": log.key_name,
        "message": log.message
    } for log in logs]

    return jsonify({
        "status": "success",
        "total_findings": len(logs_json),
        "logs": logs_json
    })