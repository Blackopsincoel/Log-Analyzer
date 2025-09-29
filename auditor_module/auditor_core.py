from playwright.sync_api import sync_playwright
import json 
import time
#Regex desenlerimiz içiren modlülümüzü import ediyoruz.
from .data_analyzer import analyze_data

def audit_website(url: str) -> list:
    """
    Belirtilen URL'yi ziyaret eder, tarayıcının Local/Session Stroge verilerini çeker, analiz eder ve bulguları döndürür.
    """
    audit_results = []

    with sync_playwright() as p:
        #Görünmez (headless) bir Chromium tarayıcısı başlatıyoruz.
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        print(f"-> Denetim Başladı: {url}")

        try:
            #siteye git ve ağ trafiği durana kadar bekle
            page.goto(url, timeout=30000)  # 30 saniye zaman aşımı
            page.wait_for_load_state("networkidle")
            time.sleep(2)  # Esktra bekleme, tüm JS yüklemesi için 

            # Local Storage verilerini al
            local_storage_data = page.evaluate('JSON.stringify(window.localStorage);')
            # Session Storage verilerini al
            session_storage_data = page.evaluate('JSON.stringify(window.sessionStorage);')

            browser.close()

            # Analaiz ve Log oluştruma

            #Local Storage analizi 
            audit_results.extend(
                process_stroge_data(local_storage_data, url, "Local Storage")
            )
            #Session Storage analizi
            audit_results.extend(
                process_stroge_data(session_storage_data, url, "Session Storage")
            )

        except Exception as e:
            print(f"Hata oluştu ({url}): {e}")
            audit_results.append({
                "source": "Auditor Core",
                "level": "ERROR",
                "message": f"Site ziyareti veya veri çekme başarısızoldu: {e}",
                "url": url 
            })
    return audit_results

def process_stroge_data(storage_json: str, url: str, storage_type: str) -> list:
    """Çekilen JSON verisini ayrıştırır, hassas veri tespiti yapar ve log formatına dönüştürür."""
    
    results = []
    try:
        storage_dict = json.loads(storage_json)
    except json.JSONDecodeError:
        return results # Geçersiz JSON ise atla
    
    for key, value in storage_dict.items():
        #data_analayzer modülündeki Regex fonksiyonu ile analiz yap
        findings = analyze_data(key, value)

        if findings:
            for finding in findings:
                #Veritabanına kaydedilecek güvenlik logu formatı
                results.append({
                    "timestamp": time.time(),
                    "url": url,
                    "storage_type": storage_type,
                    "level": "CRITICAL_SECURITY",
                    "key_name": key,
                    #Değerin sadece ilk 50 karakterini saklıyoruz.
                    "value_snippet": value[:50] + "..." if len(value) > 50 else value,
                    "finding_type": finding['type'],
                    "description": finding['desc'],      
                })
    return results

if __name__ == '__main__':
    #Modüün bağımsız test edilebilmesi için örnek kullanım:
    test_results = audit_website("https://example.com")
    for results in test_results:
        print(json.dumps(results, indent=4))        

