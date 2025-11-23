# 💬 Chatingen — Realtime Messaging Platform

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python)
![Flask](https://img.shields.io/badge/Flask-2.0%2B-green?style=for-the-badge&logo=flask)
![Socket.IO](https://img.shields.io/badge/Socket.IO-Realtime-black?style=for-the-badge&logo=socketdotio)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

**Chatingen**, Flask + Socket.IO altyapısı ile geliştirilen, gerçek zamanlı etkileşim sunan, modern arayüzlü bir mesajlaşma uygulamasıdır. Mesajların anlık iletilmesi, dosya paylaşımı, kullanıcı durum takibi ve kalıcı sohbet geçmişi gibi özelliklere sahip tam donanımlı, responsif bir sohbet deneyimi sunar.

---

## 🚀 Özellikler

**Chatingen** aşağıdaki güçlü özelliklere sahiptir:

- **⚡ Gerçek Zamanlı Mesajlaşma:** WebSocket yapısı sayesinde anında mesaj akışı.
- **📁 Dosya Paylaşımı:** JPG, PNG, GIF, PDF, TXT, DOC dosyaları (maks 5MB) yükleme desteği.
- **🖼️ Görsel Önizleme:** Mesaj içindeki görsellere tıklayınca açılan şık modal görüntüleyici.
- **⌨️ Yazıyor... İndikatörü:** Kullanıcı mesaj yazarken durum gösterimi.
- **🗃️ Kalıcı Mesajlar:** SQLite ile son 100 mesaj otomatik olarak saklanır.
- **😀 Emoji Dönüştürücü:** `:)`, `:(`, `<3` gibi ifadeler otomatik emojiye dönüşür.
- **👤 Kullanıcı Sistemi:**
  - Nickname ile giriş,
  - Rastgele kullanıcı rengi,
  - Giriş/çıkış logları.
- **📱 Responsive Tasarım:** Mobil & masaüstü uyumlu modern arayüz.

---

## 📂 Proje Yapısı

```text
Chatingen/
├── app.py               # Flask + Socket.IO ana uygulama
├── messages.db          # SQLite veritabanı
├── static/
│   ├── style.css        # Stil dosyaları
│   └── uploads/         # Yüklenen dosyalar
├── templates/
│   ├── login.html       # Giriş ekranı
│   └── chat.html        # Sohbet arayüzü
└── README.md            # Dokümantasyon
```

---

## 🛠️ Kurulum

Aşağıdaki adımlarla projeyi yerel ortamda çalıştırabilirsiniz.

### 1️⃣ Repoyu Klonlayın

Projeyi bilgisayarınıza indirin ve terminali proje klasöründe açın.

### 2️⃣ Sanal Ortam (Opsiyonel)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3️⃣ Gereksinimleri Yükleyin

```bash
pip install flask flask-socketio
```

### 4️⃣ Sunucuyu Başlatın

```bash
python app.py
```

Ardından tarayıcınızdan şu adresi açın:

**http://127.0.0.1:5000**

---

## ⚙️ Veritabanı Temizleme (Opsiyonel)

Mesaj geçmişini sıfırlamak için `reset_db.py` adlı yeni bir Python dosyası oluşturup aşağıdakini ekleyin:

```python
import sqlite3

con = sqlite3.connect('messages.db')
cur = con.cursor()
cur.execute("DELETE FROM messages")
con.commit()
con.close()
print("Veritabanı temizlendi.")
```

Çalıştırmanız yeterlidir.

---

## 🤝 Katkıda Bulunma

1. Repo'yu forklayın.
2. Yeni bir dal oluşturun:  
   `git checkout -b feature/yeni-ozellik`
3. Değişikliklerinizi commitleyin:  
   `git commit -m "Yeni özellik eklendi"`
4. Dalınızı pushlayın:  
   `git push origin feature/yeni-ozellik`
5. Pull Request açın.

---

## 📄 Lisans

Bu proje **MIT Lisansı** ile sunulmuştur.

