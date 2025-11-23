````markdown
# 💬 Chatingen

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Flask](https://img.shields.io/badge/Flask-2.0%2B-green)
![Socket.IO](https://img.shields.io/badge/Socket.IO-Realtime-black)
![License](https://img.shields.io/badge/License-MIT-yellow)

**Chatingen**, Python (Flask) ve Socket.IO teknolojileri kullanılarak geliştirilmiş, modern arayüze sahip, gerçek zamanlı bir mesajlaşma uygulamasıdır. Kullanıcıların anlık olarak mesajlaşmasına, dosya paylaşmasına ve birbirlerinin durumlarını (yazıyor...) görmesine olanak tanır.

---

## 🚀 Özellikler

Bu proje aşağıdaki temel özellikleri barındırır:

* **Gerçek Zamanlı İletişim:** WebSocket protokolü sayesinde sayfa yenilemeye gerek kalmadan anlık mesajlaşma.
* **Dosya Paylaşımı:** Görsel (JPG, PNG, GIF) ve belge (PDF, TXT, DOC) yükleme desteği (Max 5MB).
* **Görsel Önizleme:** Sohbet penceresi içinde görsellere tıklandığında açılan şık bir modal (popup) görüntüleyici.
* **Yazıyor İndikatörü:** Karşı taraf mesaj yazarken "X yazıyor..." bildirimi.
* **Kalıcı Mesajlar:** SQLite veritabanı entegrasyonu sayesinde sunucu yeniden başlatılsa bile son 100 mesajın korunması.
* **Otomatik Emoji Dönüştürücü:** `:)`, `<3` gibi ifadelerin otomatik olarak emojiye (😊, ❤️) dönüşmesi.
* **Kullanıcı Yönetimi:**
    * Nick belirleyerek giriş yapma.
    * Rastgele kullanıcı rengi ataması.
    * Giriş/Çıkış logları.
* **Responsive Tasarım:** Mobil ve masaüstü uyumlu arayüz.

---

## 📂 Proje Yapısı

```text
Chatingen/
├── app.py               # Ana Flask uygulaması ve Socket.IO olayları
├── messages.db          # SQLite veritabanı (İlk çalıştırmada otomatik oluşur)
├── static/
│   ├── style.css        # CSS Stil dosyaları
│   └── uploads/         # Yüklenen dosyaların tutulduğu klasör
├── templates/
│   ├── login.html       # Giriş ekranı
│   └── chat.html        # Sohbet arayüzü
└── README.md            # Proje dokümantasyonu
````

-----

## 🛠️ Kurulum

Projeyi yerel makinenizde çalıştırmak için aşağıdaki adımları izleyin.

### 1\. Repoyu Klonlayın veya İndirin

Dosyaları bir klasöre çıkarın ve terminali o klasörde açın.

### 2\. Sanal Ortam Oluşturun (Opsiyonel)

```bash
# Windows için
python -m venv venv
venv\Scripts\activate

# Mac/Linux için
python3 -m venv venv
source venv/bin/activate
```

### 3\. Gerekli Kütüphaneleri Yükleyin

```bash
pip install flask flask-socketio
```

### 4\. Uygulamayı Başlatın

```bash
python app.py
```

Uygulama başladığında terminalde bir adres göreceksiniz. Tarayıcınızdan **`http://127.0.0.1:5000`** adresine giderek uygulamayı kullanmaya başlayabilirsiniz.

-----

## ⚙️ Veritabanı Yönetimi (Sıfırlama)

Mesajlar `messages.db` dosyasında saklanır. Sohbet geçmişini tamamen temizlemek isterseniz, proje dizininde yeni bir python dosyası (örn: `reset_db.py`) oluşturup şu kodları çalıştırabilirsiniz:

```python
import sqlite3

con = sqlite3.connect('messages.db')
cur = con.cursor()
cur.execute("DELETE FROM messages")  # Tablodaki tüm satırları siler
con.commit()
con.close()
print("Veritabanı temizlendi.")
```

-----

## 🤝 Katkıda Bulunma

1.  Bu repoyu forklayın.
2.  Yeni bir özellik dalı (feature branch) oluşturun (`git checkout -b yeni-ozellik`).
3.  Değişikliklerinizi commitleyin (`git commit -m 'Yeni özellik eklendi'`).
4.  Dalınızı pushlayın (`git push origin yeni-ozellik`).
5.  Bir Pull Request oluşturun.

-----

## 📄 Lisans

Bu proje MIT Lisansı ile lisanslanmıştır.

```

