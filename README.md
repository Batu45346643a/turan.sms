<div align="center">
  <img src="logo.svg" alt="TURAN.SMS Logo" width="400">
</div>

# Turan SMS - Deprem İletişim Sistemi 🚨

Deprem ve afet durumlarında SMS ve offline mesh ağı üzerinden iletişim kurabilecek kapsamlı bir sistem.

## ✨ Özellikler

### 📋 To-Do List Yönetimi
- ✅ Görev ekleme/silme/güncelleme
- ✅ Lokal JSON depolama (kalıcı veri)
- ✅ Tamamlanma durumu takibi
- ✅ Öncelik seviyeleri (Düşük/Normal/Yüksek)
- ✅ İstatistikler ve raporlar
- ✅ Tamamlanmış görevleri temizleme

### 📱 SMS Gönderimi
- ✅ Twilio API ile SMS gönderme
- ✅ Tekil ve toplu SMS gönderimi
- ✅ Mesaj durumu kontrolü
- ✅ Hata yönetimi

### 🚨 Acil Durum Bildirimleri
- ✅ Acil durum kişileri yönetimi
- ✅ Acil durum uyarıları gönderme
- ✅ Deprem uyarıları gönderme
- ✅ Otomatik SMS dağıtımı
- ✅ Lokasyon bilgisi ile entegrasyon

### 📍 Lokasyon Yönetimi
- ✅ Konumu kaydetme/güncelleme
- ✅ Yakındaki kullanıcıları bulma
- ✅ Mesafe hesaplama (Haversine formülü)
- ✅ Konumu kişilerle paylaşma
- ✅ **SOS Sistemi** - Acil durum tetikleme
- ✅ Aktif SOS uyarılarını görüntüleme

### 🌐 Mesh Network (Offline İletişim)
- ✅ Cihazlar arası doğrudan iletişim
- ✅ Ağ topolojisini yönetme
- ✅ Mesaj yönlendirme (routing)
- ✅ Offline senkronizasyon kuyruğu
- ✅ Düğüm durumu yönetimi (online/offline)

## 🚀 Kurulum

### Gereksinimler
- Python 3.8+
- pip (Python paket yöneticisi)

### Adımlar

1. **Repository'yi İndir**
```bash
git clone https://github.com/Batu45346643a/turan.sms.git
cd turan.sms
```

2. **Sanal Ortam Oluştur**
```bash
# Windows:
python -m venv venv
venv\Scripts\activate

# Linux/Mac:
python3 -m venv venv
source venv/bin/activate
```

3. **Gerekli Paketleri Yükle**
```bash
pip install -r requirements.txt
```

4. **Ortam Değişkenlerini Ayarla**
```bash
# .env.example dosyasını .env olarak kopyala
cp .env.example .env

# .env dosyasını düzenle ve Twilio bilgilerini ekle
# (Twilio olmadan SMS hariç diğer özellikler çalışır)
```

## 💻 Çalıştırma

```bash
python src/main.py
```

Uygulama başladığında ana menü görüntülenecektir:

```
==================================================
🚨 TURAN SMS - Deprem İletişim Sistemi 🚨
==================================================

1. 📋 To-Do List Yönetimi
2. 📱 SMS Gönderi
3. 🚨 Acil Durum Bildirimleri
4. 📍 Lokasyon Yönetimi
5. 🌐 Mesh Network (Offline İletişim)
6. ℹ️  Sistem Bilgisi
7. 🔚 Çıkış
```

## 📋 Menü Açıklamaları

### 1. To-Do List Yönetimi
- Görevleri ekleyebilir, silebilir, güncelleyebilirsiniz
- Her görev öncelik seviyesine sahiptir
- Tamamlanmış görevleri takip edebilirsiniz
- İstatistikleri görüntüleyebilirsiniz

### 2. SMS Gönderi
- Tek bir kişiye SMS gönderin
- Twilio API gereklidir (.env dosyasına ayarları ekleyin)
- Format: +90XXXXXXXXXX

### 3. Acil Durum Bildirimleri
- Acil durum kişileri ekleyin/silin
- Acil durum uyarıları gönderin
- Deprem uyarıları gönderin
- Tüm kişilere otomatik SMS iletilir

### 4. Lokasyon Yönetimi
- Konumunuzu GPS koordinatları ile kaydedin
- Yakındaki kullanıcıları bulun
- SOS tetikleyin (yakındaki kişilere bildir)
- Tüm konumları görüntüleyin

### 5. Mesh Network
- Offline iletişim için düğümler ekleyin
- Düğümleri birbirine bağlayın
- İnternetsiz mesaj gönderin
- Çevrimdışı verileri senkronize edin

## 📊 Proje Yapısı

```
turan.sms/
├── src/
│   ├── __init__.py
│   ├── main.py                 # Ana uygulama menüsü
│   ├── todo_manager.py         # To-Do List yönetimi
│   ├── sms_handler.py          # SMS ve Acil Durum
│   ├── location.py             # Lokasyon ve SOS
│   └── mesh_network.py         # Mesh Network iletişimi
├── tests/
│   ├── __init__.py
│   └── test_todo.py            # To-Do List testleri
├── data/                       # Lokal veri depolama
│   ├── todos.json
│   ├── locations.json
│   ├── sos_alerts.json
│   ├── mesh_network.json
│   ├── mesh_messages.json
│   └── sync_queue.json
├── .env.example                # Ortam değişkenleri şablonu
├── .gitignore
├── requirements.txt
├── README.md
├── logo.svg
└── LICENSE
```

## 🔧 Konfigürasyon

### SMS (Twilio) Kurulumu

1. https://www.twilio.com/ adresine gidin
2. Hesap oluşturun veya giriş yapın
3. Console'dan şu bilgileri alın:
   - Account SID
   - Auth Token
   - Telefon numarası

4. `.env` dosyasını düzenleyin:
```env
TWILIO_ACCOUNT_SID=your_sid_here
TWILIO_AUTH_TOKEN=your_token_here
TWILIO_PHONE_NUMBER=+90XXXXXXXXXX
```

## 🧪 Testleri Çalıştırma

```bash
# Tüm testleri çalıştır
pytest tests/ -v

# Yalnızca To-Do testlerini çalıştır
pytest tests/test_todo.py -v

# Kapsam raporunu göster
pytest tests/ --cov=src
```

## 📱 API Örnekleri

### To-Do List Kullanımı
```python
from src.todo_manager import TodoManager

manager = TodoManager()

# Görev ekle
todo = manager.add_todo("Deprem Hazırlığı", "Acil çanta hazırla", "high")

# Tüm görevleri listele
todos = manager.get_all_todos()

# İstatistikler
stats = manager.get_stats()
```

### SMS Gönderme
```python
from src.sms_handler import SMSHandler

sms = SMSHandler()

# SMS gönder
result = sms.send_sms("+905551234567", "Merhaba!")
```

### Lokasyon Yönetimi
```python
from src.location import LocationManager

location = LocationManager()

# Konumu kaydet
location.add_user_location("user1", 41.0082, 28.9784, "Istanbul")

# Yakındaki kullanıcıları bul
nearby = location.find_nearby_users("user1", radius_km=5)
```

### Mesh Network
```python
from src.mesh_network import MeshNetwork

mesh = MeshNetwork()

# Düğüm ekle
mesh.add_node("node1", "Cihaz 1")
mesh.add_node("node2", "Cihaz 2")

# Düğümleri bağla
mesh.connect_nodes("node1", "node2")

# Mesaj gönder
msg = mesh.send_mesh_message("node1", "node2", "Merhaba")
```

## 🤝 Katkı Yapma

Pull request'ler memnuniyetle karşılanır! Büyük değişiklikler için lütfen önce bir issue açın.

## 📝 Lisans

MIT License - Detaylar için LICENSE dosyasına bakın

## 📞 İletişim & Destek

Sorularınız, önerileriniz veya hata raporları için:
- GitHub Issues açabilirsiniz
- Pull Request gönderebilirsiniz

## 🎯 Gelecek Planlar

- [ ] Web arayüzü
- [ ] Mobil uygulama
- [ ] Daha gelişmiş mesh routing algoritmaları
- [ ] Harita entegrasyonu
- [ ] Gerçek zamanlı bildirimler
- [ ] Veritabanı desteği (SQLite, PostgreSQL)

---

**Turan SMS** - Afetlere karşı bağlantıda kalın! 🚨
