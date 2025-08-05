
# 🤖 Nexo - Discord Assistant Bot

**Nexo**, Python ile geliştirilen, `discord.py` kütüphanesini kullanan interaktif bir Discord asistan botudur. Kullanıcılara sistem bilgisi, eğlenceli komutlar, sunucu yönetimi gibi birçok özellik sunar. Hem kişisel hem de topluluk sunucularınızda yardımcı olmak için tasarlandı.

---

## 🚀 Başlangıç

### Gereksinimler

- Python 3.8+
- `discord.py` kütüphanesi
- `config.py` dosyasında `token` tanımı
- `homework.py` dosyasında tanımlanmış `PC` sınıfı

### Kurulum

1. Bu repoyu klonlayın:
   ```bash
   git clone https://github.com/kullanici/nexo-bot.git
   cd nexo-bot
   ```

2. Gerekli kütüphaneleri yükleyin:
   ```bash
   pip install discord.py
   ```

3. `config.py` adında bir dosya oluşturun ve bot token’ınızı ekleyin:
   ```python
   token = "YOUR_DISCORD_BOT_TOKEN"
   ```

4. `homework.py` dosyasının içinde `PC` sınıfını barındırdığınızdan emin olun. Bu sınıf sistem bilgisi ve mini oyun komutları için gereklidir.

---

## 📚 Komutlar

Aşağıdaki komutları botla etkileşime geçmek için kullanabilirsiniz:

### Genel Komutlar
```
/about         - Bot hakkında bilgi verir.
/hello         - Merhaba mesajı gönderir.
/info          - Bilgilendirici mesaj döner.
/ping          - Botun gecikmesini gösterir.
/avatar        - Kullanıcının avatarını gösterir.
/kullanici     - Kullanıcı adını ve ID’sini gösterir.
/sunucu        - Sunucu adı ve üye sayısını gösterir.
/sunucuinfo    - Sunucunun oluşturulma tarihini gösterir.
/davet         - Sunucuya davet linki oluşturur.
/temizle [n]   - Belirtilen kadar mesajı siler.
/rastgele      - İki rastgele sayının toplamını verir.
/tahmin        - Sayı tahmin oyunu oynatır.
```

### PC Yönetim Komutları
```
/pc_about      - PC donanım bilgilerini gösterir.
/pc_status     - Kaynak kullanımını rastgele gösterir.
/pc_antivirus  - Antivirüs taraması yapar (simülasyon).
/pc_update     - Güncelleme kontrolü yapar.
/pc_processes  - Çalışan işlemleri listeler.
```

---

## 🖼️ Otomatik Resim Algılama

Bot gönderilen mesajları tarar, ek olarak bir **görsel dosyası** (png, jpg, gif...) içeriyorsa kullanıcıyı bilgilendirir:

> "Sanırım bir resim gönderdiniz! Dosya türü: PNG"

---

## ⚠️ Hata Yönetimi

Bot aşağıdaki hatalara karşı kullanıcı dostu yanıtlar verir:

- Komut eksik argüman içeriyorsa
- Tanımlanmamış komut girildiyse
- Yetki gerektiren komutlarda kullanıcı yetkisi yoksa
- Diğer bilinmeyen hatalarda hata mesajı gösterir

---

## 🛡️ Güvenlik Notu

Token’ınızı **asla** herkese açık bir yerde paylaşmayın! `config.py` dosyasını `.gitignore` dosyasına ekleyin.

---

## 👤 Geliştirici

> Developed by [Senin Adın]  
> Discord: `nexo#1234`  
> Github: [github.com/seninprofilin](https://github.com/seninprofilin)

---

## 📄 Lisans

MIT License © 2025
