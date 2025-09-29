import regex as re

#Hassas verii türlerini ve bunları tespit edecek Regex desenleri içeren sözlük 


SENSITIVE_DATA_PATTERNS = {
    #Örn: 24-64 karakterli alfasayısal dize (API/Gizli Anahtar şüphesi)
    "API_KEY": {"pattern": re.compile(r'(?:api_key|secret|token)[\'"]?\s*[:=]\s*[\'"]?([a-zA-Z0-9]{24,64})[\'"]?'), "desc": "Uzun alfasayısal dize (API/Gizli Anahtar şüphesi)"},
    #JWT formatı(Header.Payload.Signature)
    "JWT_TOKEN": {"pattern": re.compile(r'eyJ[A-Za-z0-9-_=]+\.[A-Za-z0-9-_=]+\.[A-Za-z0-9-_.+/=]+'), "desc": "JSON Web Token (Oturum/Kimlik Doğrulama Bilgisi)"},
     # Parola anahtar kelimesi (Anahtar olarak saklanıyorsa)
    "PASSWORD_FIELD": {"pattern": re.compile(r'(?:parola|password|sifre|pass|pwd)'), "desc": "Parola/Şifre anahtar kelimesi kullanılmış"},
    #Kullanıcı Kimlikleri
    "USER_ID": {"pattern": re.compile(r'(?:user_id|kullanici_id)[\'"]?\s*[:=]\s*[\'"]?([0-9a-fA-F\-]{8,36})[\'"]?'), "desc": "UUID veya kullanıcı kimliği tespit edildi"}
}

def analyze_data(key: str, value: str) -> list:
    """Veri anahtarı ve değeri üzerne Regex ile tarama yapar."""
    findings = []

    for name, data in SENSITIVE_DATA_PATTERNS.items():
        #Anahtar kelimenin kendisisni konrtrol et (örn: Anahtar 'password' içeriyor mu?)
        if re.search(data['pattern'], key.lower()):
            findings.append({"type": name, "desc": f"Anahtar kelime tespit edildi: {data['desc']}"})

        #Değerin içerğini kontrol et (örn: Değer bir JWT tokenı mı?)
        if re.search(data['pattern'], value):
            findings.append({"type": name, "desc": f"Değer içeriği tespit edildi: {data['desc']}"})

    return findings