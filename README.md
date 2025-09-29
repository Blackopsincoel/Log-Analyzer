# Log Analyzer (Güvenlik Odaklı Log Yönetim Sistemi)

## 📌 Projenin Amacı
Bu proje, sistem loglarını kaydetme, analiz etme ve izlemenin yanı sıra, **kritik bir güvenlik denetimi modülü** içerir. 

Amaç; sistemdeki kullanıcı etkinliklerini, hata mesajlarını ve performans verilerini merkezi bir yerde toplarken, **çalışanların kullandığı web sitelerinin istemci taraflı depolama (Local/Session Storage) alanlarında hassas verilerin (parola, API anahtarı, JWT) saklanıp saklanmadığını otomatik olarak kontrol etmek ve raporlamaktır.**

Bu sayede:
- Olası güvenlik ihlallerini erken tespit etmek,
- Ağ trafiğini ve cihaz durumlarını izlemek,
- Arıza ve hata durumlarında hızlı aksiyon almak,
- Web uygulamalarının istemci tarafı güvenlik açıklarını proaktif olarak denetlemek hedeflenmiştir.

---

## 🛠️ Kullanılan Teknolojiler
Proje, verimli, ölçeklenebilir ve güvenilir bir yönetim sunmak için aşağıdaki teknolojileri kullanmaktadır:

### 🔹 Programlama Dili
- **Python 3.x**: Kolay geliştirme ve geniş kütüphane desteği için tercih edildi.

### 🔹 Veri Tabanı
- **SQLite / PostgreSQL**: Logların saklanması için kullanıldı. (Hızlı prototipleme için SQLite, ölçeklenebilirlik için PostgreSQL önerilir.)

### 🔹 API ve Kütüphaneler
- **Flask**: Web tabanlı arayüz ve API entegrasyonu için modüler (Blueprint) yapı sağlayan ana iskelet.
- **Playwright**: Web Security Auditor modülü için tarayıcı otomasyonu ve Local Storage verisi çekme.
- **Regex**: Çekilen verilerde hassas desenleri (Token, Parola, API Key) tespit etme.
- `SQLAlchemy`: Veritabanı yönetimini kolaylaştırmak için.
- `logging` (Python standart kütüphanesi): Sistem olaylarını kaydetmek için.

### 🔹 Güvenlik
- HTTPS (Üretimde), JWT (JSON Web Token) ile kimlik doğrulama.

---

## ⚙️ Özellikler
- **Web Security Denetimi:** Belirtilen URL'lerde `localStorage` ve `sessionStorage` denetimi.
- **Hassas Veri Tespiti:** JWT, API Anahtarı ve Parola gibi kilit bilgilerin Regex ile taranması.
- 📁 Log toplama ve merkezi kayıt (Sistem logları ve Güvenlik bulguları).
- 🔍 Filtreleme ve arama (Bulgu tipine ve URL'ye göre).
- 📊 Görselleştirme (Bulgu dağılımı grafikleri).

---

## 🚀 Çalıştırma
1. **Ortam Hazırlığı:** Python sanal ortamını (venv) oluşturun ve etkinleştirin.
2. **Kütüphaneleri Yükleyin:**
   ```bash
   pip install -r requirements.txt
   playwright install