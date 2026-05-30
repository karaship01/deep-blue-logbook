# Deep Blue - Dalış ve Proje Günlüğü

Bu proje, Gazi Üniversitesi TUSAŞ Kazan MYO İnternet Programcılığı dersi kapsamında "AI Ajan Destekli Vibe Coding" yaklaşımıyla geliştirilmiş bir web uygulamasıdır.

## 🎥 Proje Demo Videosu
[Buraya yarın çekeceğin YouTube veya Google Drive video linkini yapıştıracaksın]

## 🚀 Kullanılan Teknolojiler
* **Backend:** Python, Flask 3.x, Blueprint Mimari
* **Veritabanı:** SQLAlchemy, PostgreSQL (Docker ile), SQLite (Geliştirme)
* **Frontend:** Jinja2, Bootstrap, Flask-WTF
* **Dağıtım:** Docker, Gunicorn, Docker-Compose

## 🛠️ Kurulum ve Çalıştırma (Docker ile)
Bilgisayarınızda Docker ve Docker Desktop kuruluysa, projeyi tek komutla ayağa kaldırabilirsiniz:
1. Repoyu klonlayın: `git clone [Senin-Repo-Linkin]`
2. Klasöre girin: `cd 06_profil_sayfasi_ve_avatarlar`
3. Docker ile başlatın: `docker-compose up -d --build`
4. Tarayıcınızda `http://localhost:5000` adresine gidin.

Geliştirme Ortamı ve Süre Tahmini Değerlendirmesi
Bu projede Antigravity geliştirme ortamının en faydalı bulduğum iki özelliği "Plan Modu" ve "Manager View" oldu. Plan modu sayesinde AI'ın doğrudan kod yazıp projeyi bozmasını engelleyerek önce mimariyi tartışabildim. Manager View ise arka planda büyük klasör yapılarını kurarken bana zaman kazandırdı. Tüm bu projeyi yapay zeka desteği olmadan, baştan sona dokümantasyon okuyarak tek başıma yazsaydım, özellikle Blueprint mimarisine geçiş ve Dockerize etme aşamalarındaki hataları çözmek haftalarımı alabilirdi. AI sayesinde bu süreyi çok verimli bir şekilde birkaç güne sığdırmış oldum.