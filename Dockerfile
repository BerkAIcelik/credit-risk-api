# imaj lazım aşağıdaki şunu diyor: içinde Python kurulu hazır bir Linux ver.
FROM python:3.12.2-slim

# workdir adı üstünde : Linux'un içinde "/app" diye bir klasör aç ve oraya gir.
# Bundan sonraki tüm komutlar bu klasörün içinde çalışacak.
WORKDIR /app

# BAĞIMLILIKLAR: Önce SADECE requirements.txt dosyasını kopyala.
# NEDEN? Docker "Cache" mantığıyla çalışır. Eğer requirements değişmediyse,
# aşağıdaki "pip install" adımını tekrar yapmaz, hafızadan kullanır. Hız kazandırır.
COPY requirements.txt .

# --no-cache-dir: İndirilen kurulum dosyalarını sil ki imajın boyutu şişmesin.
RUN pip install --no-cache-dir -r requirements.txt

# bilgisayarındaki geri kalan tüm dosyaları içeri al
COPY . .

#  Bu kutunun-konteynırın 8000 numaralı kapısını dış dünyaya aç,portu açıyoruz
EXPOSE 8000

# Konteyner "Run" edildiğinde bu komutu çalıştır.
# 0.0.0.0: "Bana her yerden ulaşabilirsiniz" demektir 
CMD ["uvicorn", "app.api.main:app", "--host", "0.0.0.0", "--port", "8000"]