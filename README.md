# Turan SMS - Deprem İletişim Sistemi

Deprem ve afet durumlarında internet bağlantısı olmadan SMS üzerinden iletişim kurabilecek bir sistem.

## Özellikler

- ✅ Offline SMS iletişimi
- ✅ Mesh ağı desteği
- ✅ Lokasyon paylaşımı
- ✅ Acil durum bildirimleri
- ✅ Basit ve kullanıcı dostu arayüz

## Gereksinimler

- Python 3.8+
- pip (Python paket yöneticisi)

## Kurulum

```bash
# Repository'yi klonlayın
git clone https://github.com/Batu45346643a/turan.sms.git
cd turan.sms

# Sanal ortam oluşturun
python -m venv venv

# Sanal ortamı etkinleştirin
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Gerekli paketleri yükleyin
pip install -r requirements.txt
```

## Kullanım

```bash
python main.py
```

## Proje Yapısı

```
turan.sms/
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── sms_handler.py
│   ├── mesh_network.py
│   ├── location.py
│   └── emergency.py
├── tests/
│   ├── __init__.py
│   └── test_sms.py
├── requirements.txt
├── .gitignore
├── README.md
└── LICENSE
```

## Katkı Yapma

Pull request'ler memnuniyetle karşılanır. Büyük değişiklikler için önce bir issue açın.

## Lisans

MIT

## İletişim

Sorularınız ve önerileriniz için issue açabilirsiniz.
