İnternet Programcılığı Proje Raporu: Yapay Zeka Destekli Web Geliştirme Süreci
Öğrenci Adı Soyadı: Ahmet Yağız KARA
Öğrenci Bölüm: Bilişim Güvenliği Teknolojisi 2.Şube
Öğrenci Numarası: 25380102014
Proje Adı: Deep Blue (Dalış/Proje Günlüğü Uygulaması)
Kullanılan AI Modeli: Gemini (Mod: Plan / Fast)

1. Giriş ve Proje Özeti
Bu proje, modern web geliştirme mimarilerine uygun, dinamik ve ölçeklenebilir bir web uygulaması geliştirmek amacıyla ortaya çıkmıştır. Flask mikro web çerçevesi kullanılarak inşa edilen "Deep Blue" adlı bu uygulama, kullanıcıların kayıt olup giriş yapabildiği, profillerini düzenleyebildiği, yeni projeler/dalışlar ekleyebildiği ve bunlara yorum yapabildiği kapsamlı bir platformdur.

Projenin temel amacı, sadece çalışan bir kod yazmak değil; aynı zamanda Blueprint (Application Factory) mimarisi, veritabanı ilişkileri (One-to-Many), yetkilendirme (Authentication), form doğrulama, çoklu dil desteği (Babel) ve konteynerizasyon (Docker) gibi endüstri standartlarındaki konseptleri uygulamalı olarak öğrenmektir. Geliştirme süreci tamamen bir Yapay Zeka (AI) asistanı ile "Pair Programming" (Eşli Programlama) mantığında yürütülmüş, kodun yazımından hataların ayıklanmasına kadar her aşamada AI araçlarından aktif olarak faydalanılmıştır.

2. Geliştirme Süreci ve Yapay Zeka İşbirliği
Proje geliştirme süreci, planlı ve kademeli olarak toplam 7 oturumda gerçekleştirilmiştir. Bu süreçte yapay zeka sadece bir "kod üretici" olarak değil, aynı zamanda bir mentor ve mimari danışman olarak kullanılmıştır.

İlk oturumlarda projenin temel iskeleti, Flask-WTF ile web formları ve SQLAlchemy ile veritabanı modelleri oluşturulmuştur. Bu aşamalarda yapay zekaya verilen promptlar genellikle "X özelliğini nasıl eklerim?" şeklinde daha basit düzeydeyken, proje karmaşıklaştıkça prompt mühendisliği yeteneklerim de gelişmiştir. Örneğin; form çevirileri (Babel) veya Blueprint mimarisine geçiş aşamalarında, mevcut kod dosyasının tamamını yapay zekaya vererek "Mevcut değişkenlerimi ve çeviri etiketlerimi bozmadan bu dosyayı auth ve main olarak ikiye böl" şeklinde çok daha spesifik, sınırları çizilmiş ve bağlamı koruyan promptlar kullanmaya başladım.

Yapay zeka ile çalışmanın en büyük avantajı, hata loglarını (traceback) okuma ve anlama konusundaki hızı oldu. Terminalde karşılaştığım karmaşık hataları doğrudan yapay zekaya ileterek, hatanın kaynağının kodda mı, yoksa işletim sisteminin (Windows) sanal ortam (venv) yönetiminde mi olduğunu hızlıca tespit edip çözüme kavuşturabildim.

3. Mimari Yapı ve Kullanılan Teknolojiler
Projenin mimarisi, sürdürülebilirliği sağlamak adına modüler bir yapıda kurgulanmıştır.

Backend: Python tabanlı Flask framework'ü tercih edilmiştir. Başlangıçta tüm uygulamanın tek bir app nesnesine bağlı olduğu monolitik bir yapı kullanılırken, 6. oturumda "Application Factory" ve "Blueprint" mimarisine geçiş yapılmıştır. Bu sayede auth (kimlik doğrulama), main (ana akış) ve errors (hata sayfaları) modülleri birbirinden bağımsız hale getirilmiştir.

Veritabanı ve Modeller: Veritabanı yönetimi için SQLAlchemy (ORM) ve versiyon kontrolü için Flask-Migrate kullanılmıştır. Sistemde en az 3 model zorunluluğunu karşılamak üzere User (Kullanıcı), Project (Proje/Dalış) ve Comment (Yorum) sınıfları oluşturulmuştur. Bu modeller arasında One-to-Many (Bire-Çok) ilişkiler kurularak, bir kullanıcının birden fazla projesi olması ve bir projenin birden fazla yorumu olması sağlanmıştır.

Frontend: Arayüz tasarımında Bootstrap kullanılmış, şablon motoru olarak Jinja2'nin "Template Inheritance" (Şablon Mirası) özelliğinden faydalanılmıştır. Sayfalama (Pagination) özelliği eklenerek veri kalabalığı önlenmiştir.

Dağıtım (Deployment): Projenin canlı ortama taşınmaya hazır olması için son oturumda Docker mimarisi entegre edilmiştir. Dockerfile yazılarak uygulama python:3.12-slim imajı içine alınmış, Gunicorn web sunucusu yapılandırılmış ve docker-compose.yml ile PostgreSQL veritabanı servisine bağlanmıştır.

4. Karşılaşılan Zorluklar ve Çözüm Yaklaşımları
Bu projeyi geliştirirken, yapay zekanın sağladığı kodların her zaman ilk seferde çalışmadığı ve geliştiricinin sürece aktif müdahale etmesi gerektiği birçok durum yaşanmıştır:

1. Döngüsel İçe Aktarma (Circular Import) Sorunu: Projenin ortasında Blueprint mimarisine geçiş yaparken, sistemdeki global app nesnesi silinip yerine factory metodu (create_app) getirildi. Ancak models.py içindeki şifre sıfırlama (token) fonksiyonları eski app nesnesini çağırmaya devam ettiği için uygulama çöktü. Yapay zeka ile hata logunu analiz ettiğimizde, bu sorunu çözmek için Flask'ın current_app nesnesini kullanmamız gerektiğini keşfettik ve import yapılarını buna göre güncelledim.

2. Sanal Ortam (Virtual Environment) ve Yol (Path) Çatışmaları:
Flask-Migrate ile veritabanını güncellerken Windows terminalinde sık sık ModuleNotFoundError: No module named 'flask_sqlalchemy' hatası aldım. Halbuki paketler kuruluydu. Sorunun, Windows'un komutları proje içindeki venv yerine bilgisayardaki global Python sürümünde çalıştırmaya çalışmasından kaynaklandığını tespit ettik. Komutların başına .\venv\Scripts\python -m takısını ekleyerek sistemi sanal ortama kilitlemeyi başardım ve migrasyonları sorunsuz gerçekleştirdim.

3. HTML Yönlendirmelerinin (Routes) Çökmesi:
Uygulamayı modüllere ayırdıktan sonra şablonlardaki eski url_for('index') gibi rotalar çalışmamaya başladı. Çünkü artık rotaların hangi Blueprint'e ait olduğu (main.index veya auth.login) belirtilmeliydi. Bu aşamada yapay zeka bana rotaların yeni hallerini verdi, ben de VS Code'un toplu arama ve değiştirme özelliklerini kullanarak tüm şablonlardaki yönlendirmeleri manuel bir şekilde organize ettim.

5. Sonuç ve Kişisel Kazanımlar
Bu proje, modern bir web uygulamasının temelden başlayıp Docker konteynerine girecek seviyeye gelene kadar geçirdiği tüm evreleri anlamamı sağladı. Yapay zeka araçlarının yazılım geliştirme sürecindeki rolünün, sadece bir kod yazıcı değil; iyi yönlendirildiğinde mükemmel bir yol arkadaşı ve hata ayıklayıcı olduğunu deneyimledim.

En önemli kazanımlarımdan biri, AI'ın verdiği kodu körü körüne kopyalamak yerine, kodun ne işe yaradığını anlamak ve sistemin geneline (mimarisine) olan etkisini hesaplamak oldu. Bir hata çıktığında paniklemek yerine terminal loglarını (Traceback) okuma alışkanlığı kazandım. Sonuç olarak; yönergelerdeki tüm zorunlu teknik gereksinimleri barındıran, modüler, veritabanı ilişkileri güçlü ve her ortamda çalışmaya hazır (Dockerize edilmiş) bir web projesini başarıyla tamamladım.