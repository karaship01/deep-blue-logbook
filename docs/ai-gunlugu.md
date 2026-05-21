## Oturum 1 - 04 Mayıs 2026

### Hedef
Projenin ana fikrini belirlemek, Flask Mega-Tutorial'ın ilk 9 bölümündeki yapıyı kendi "Dalış Günlüğü" (Deep Blue) konseptimize uyarlamak ve hocanın proje yönergesindeki teknik şartların analizini yapmak. İlk GitHub commit'ini (kaydını) başarıyla atmak.

### Kullandığım Mod ve Model
Model: Gemini 3 Pro (Ajanın yönlendirme, kod inceleme ve sorun giderme yeteneği için tercih ettim).
Görünüm: Manager ve Editor (Büyük resmi planlamak ve terminal komutlarını uygulamak için).

### Ajanın Önerdiği Plan
Ajan bana mevcut kodların hocanın 10 zorunlu maddesinden hangilerini karşıladığını (Auth, Pagination, vb.) ve hangilerinin eksik olduğunu (Blueprint mimarisi, 3. Veritabanı modeli, Deployment) listeledi. Buna göre 4 haftalık bir Sprint (Master Plan) çıkardık.

### Üretilen Kodda Düzelttiklerim
- Ana sayfadaki `Post` mantığını `Dalış Noktası` olarak güncelledim.
- Arayüzü Bootstrap ile denizaltı temasına uyarladık. Yeni tasarımda önbellek (cache) kaynaklı eski sayfaların görünmesi sorununu VS Code Simple Browser yerine Chrome gizli sekme kullanarak çözdüm.
- Gizli verilerimizin çalınmasını önlemek ve -10 puan ceza almamak için projeye `.gitignore` dosyası ekledim ve içine `venv/`, `.env`, `app.db` gibi kritik dosyaları yazdım.

### Karşılaştığım Hatalar ve Çözümler
1. **Hata:** Arayüzü güncelledikten sonra `ModuleNotFoundError: No module named 'flask_sqlalchemy'` hatası aldım.
   * **Çözüm:** Terminalde `(venv)` ortamının aktif olmadığını fark ettim. Sanal ortamı `.\venv\Scripts\activate` ile aktif edip sorunu çözdüm.
2. **Hata:** GitHub'a ilk commit'imi atmaya çalışırken terminalde `'git' is not recognized as an internal or external command` hatası aldım.
   * **Çözüm:** Ajan ile durumu analiz ettik. İşletim sistemimde Git'in kurulu olmadığını tespit ettik. Git'in resmi sitesinden Windows sürümünü kurup VS Code terminalini yeniden başlatarak sorunu aştım.
3. **Hata:** `git commit` atarken `Author identity unknown` hatası aldım.
   * **Çözüm:** Git'i sıfırdan kurduğum için global kullanıcı ayarlarım eksikti. Ajanın yönlendirmesiyle `git config --global user.email` ve `user.name` komutlarını kullanarak tanımlamalarımı yaptım. Klasörü `git init` ile yerel bir depoya çevirdikten sonra işlemi başarıyla tamamladım.

### Bu Oturumdan Öğrendiğim
Hata almanın aslında ortam (environment) ve sürüm kontrol (git) yönetimiyle ne kadar ilişkili olduğunu gördüm. Ayrıca hocanın yönergesini ajana analiz ettirmek, `.env` dosyasını gizlemek gibi hayati kuralları atlamamamı sağladı.

### Sonraki Oturum İçin Notlar
GitHub'da uzak bir depo (repository) oluşturup `git push` ile bu yerel kodları buluta taşıyacağım. Ardından 10. Bölüm'deki (Şifre Sıfırlama) e-posta entegrasyonu kodlarını yazmaya başlayacağız.