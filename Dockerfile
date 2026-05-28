# Hocanın istediği 3.12-slim tabanını kullanıyoruz
FROM python:3.12-slim

# Çalışma dizinini belirliyoruz
WORKDIR /app

# Önce sadece gereksinimleri kopyalayıp kuruyoruz
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Şimdi tüm proje dosyalarını kopyalıyoruz
COPY . .

# Production ayarlarını belirliyoruz
ENV FLASK_APP=microblog.py
ENV FLASK_DEBUG=False

# Uygulamanın dışarıya açılacağı port
EXPOSE 5000

# Gunicorn ile uygulamayı 4 worker (işçi) çalıştırarak başlatıyoruz
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "microblog:app"]