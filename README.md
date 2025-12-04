# Kredi Risk Tahmin Sistemi (Credit Risk Prediction System)

Bu proje, bankacılık süreçlerinde kredi değerlendirmelerini otomatize etmek için geliştirilmiş, Yapay Zeka destekli, **Clean Architecture (Onion Architecture)** prensiplerine uygun, ölçeklenebilir bir backend API servisidir. Frontend sadece güzel görsellik için eklenmiştir.

## 🚀 Proje Hakkında

Sistem, kullanıcıdan gelen finansal ve demografik verileri (Gelir, Borç Oranı, Kredi Geçmişi vb.) alır ve arka planda çalışan optimize edilmiş **CatBoost** makine öğrenmesi modeli ile anlık kredi risk değerlendirmesi yapar.Yani amaç, bir makine öğrenmesi modelinin eğitiminden (Training) canlıya alınmasına (Deployment) kadar olan ML Engineering sürecini uçtan uca yönetmektir.

**Temel Özellikler:**
*   **Yapay Zeka Destekli:** Yüksek doğruluklu CatBoost modeli ile kredi onay/ret tahminleri.
*   **Clean Architecture:** Core, Use Cases, Infrastructure ve API katmanları ile modüler, test edilebilir ve bakımı kolay yapı.
*   **Yüksek Performans:** **FastAPI** framework'ü ile hızlı ve asenkron API yanıtları.
*   **Veri Kalıcılığı:** Değerlendirme sonuçlarının ve başvuru verilerinin **MySQL** veritabanında saklanması.
*   **Konteynerizasyon:** Docker ve **Docker** Compose ile API ve Veritabanı servislerinin tek komutla yönetilmesi.

## 🔬 Model Geliştirme Süreci (Research & Training)

**Bu notebook şunları içerir:**
* Veri Görselleştirme
* Feature Engineering 
* Optuna ile Hiperparametre Optimizasyonu
* SHAP ile Model Açıklanabilirliği (Explainability)
* Threshold Tuning (Recall Optimizasyonu)

Bu projenin arkasındaki veri analizi, özellik mühendisliği (Feature Engineering) ve model eğitim süreçlerini incelemek isterseniz, Jupyter Notebook dosyalarını inceleyebilirsiniz:
👉 **[Model Eğitim ve Analiz Notları](notebooks)**



## 🏗 Mimari Yapı (Clean Architecture)

Proje, bağımlılıkların dıştan içe doğru olduğu soğan mimarisi (Onion Architecture) prensiplerine göre tasarlanmıştır. Bu sayede iş mantığı framework ve dış kaynaklardan bağımsızdır.

*   **Core (Domain):** İş mantığının kalbi. Hiçbir dış kütüphaneye veya framework'e bağımlı değildir. (`app/core`)
    *   *Entities:* `LoanApplication`, `PredictionResults` gibi temel veri yapıları.
*   **Use Cases (Application):** Uygulama senaryolarını içerir. (`app/use_cases`)
    *   *Loan Processor:* Veriyi işler, modelden tahmin alır ve sonucu kaydeder.
*   **Infrastructure:** Veritabanı, ML modeli gibi dış dünya adaptörlerini içerir. (`app/infrastructure`)
    *   *CatBoostAdapter:* Model dosyalarını yükler ve tahmin yapar.
    *   *MySQLRepository:* Veritabanı işlemlerini yönetir.
*   **API (Presentation):** Dış dünya ile iletişim kuran REST API katmanı. (`app/api`)
    *   *Main:* Endpoint tanımları ve dependency injection.
    *   *Schemas:* İstek ve yanıt modelleri (DTOs).

## 🛠 Teknolojiler

*   **Dil:** Python 3.12+
*   **Web Framework:** FastAPI
*   **ML Model:** CatBoost
*   **ORM:** SQLAlchemy
*   **Veritabanı:** MySQL (PyMySQL sürücüsü ile)
*   **Veri Doğrulama:** Pydantic

## 📂 Proje Yapısı

```
D:\credit-risk-api\
├── app\
│   ├── api\            # API Endpoint ve Şemalar (Controller Layer)
│   │   ├── main.py
│   │   └── schemas.py
│   ├── core\           # Domain Varlıkları ve Arayüzler (Domain Layer)
│   │   ├── entities.py
│   │   └── interfaces.py
│   ├── infrastructure\ # Dış Kaynak Adaptörleri (Infrastructure Layer)
│   │   ├── model_artifacts\ # Eğitilmiş Model Dosyaları
│   │   ├── adapters.py      # ML Model Adaptörü
│   │   ├── database.py      # DB Bağlantısı
│   │   ├── db_models.py     # ORM Modelleri
│   │   └── db_repository.py # Veri Erişim Katmanı
│   ├── static\         # Frontend Arayüz Dosyaları
│   │   ├── css\
│   │   │   └── style.css
│   │   ├── js\
│   │   │   └── script.js
│   │   └── index.html
│   └── use_cases\      # İş Mantığı (Application Layer)
│       └── loan_processor.py
├── notebooks\          # Veri Analizi ve Model Eğitimi (Jupyter)
├── docker-compose.yml  # Docker Servis Tanımları
├── Dockerfile          # Docker İmaj Tanımı
├── Frontend_Specifications.md # Frontend Teknik Gereksinimleri
├── RULES.md            # Geliştirme Kuralları ve Kısıtlamalar
├── requirements.txt    # Proje Bağımlılıkları
└── README.md           # Proje Dokümantasyonu
```

## ⚙️ Kurulum

1.  **Depoyu Klonlayın:**
    ```bash
    git clone <repo-url>
    cd credit-risk-api
    ```

2.  **Sanal Ortam Oluşturun ve Aktifleştirin:**
    ```bash
    python -m venv venv
    # Windows için:
    .\venv\Scripts\activate
    # Linux/Mac için:
    source venv/bin/activate
    ```

3.  **Bağımlılıkları Yükleyin:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Veritabanı Ayarları:**
    `app/infrastructure/database.py` dosyasındaki veritabanı bağlantı dizesini (connection string) kendi yerel MySQL yapılandırmanıza göre düzenlediğinizden emin olun.

5.  **Uygulamayı Başlatın:**
    ```bash
    uvicorn app.api.main:app --reload
    ```

## 🔌 API Kullanımı

**Endpoint:** `POST /predict`

Kredi risk tahminini almak için bu endpoint'e aşağıdaki formatta bir JSON isteği gönderin.

**Örnek İstek (Request Body):**
```json
{
  "annual_income": 75000,
  "debt_to_income_ratio": 0.30,
  "credit_score": 720,
  "loan_amount": 15000,
  "interest_rate": 0.10,
  "education_level": "Bachelor's",
  "grade_subgrade": "B1",
  "gender": "Male",
  "marital_status": "Single",
  "employment_status": "Employed",
  "loan_purpose": "Car"
}
```

**Örnek Yanıt (Response):**
```json
{
  "probability": 0.85,
  "decision": "ONAY",
  "application_id": 1024
  
}
```

## Kurulum ve Çalıştırma (Docker ile)

Bu projeyi kendi bilgisayarınızda çalıştırmak için Python veya MySQL kurmanıza gerek yoktur. Sadece Docker Desktop yüklü olması yeterlidir.

1.  **Repoyu Klonlayın**
    ```bash
    git clone [https://github.com/KULLANICI_ADIN/credit-risk-api.git](https://github.com/KULLANICI_ADIN/credit-risk-api.git)
    cd credit-risk-api
    ```

2.  **Sistemi Başlatın**
    Docker Compose, API ve Veritabanı servislerini oluşturup birbirine bağlayacaktır.
    ```bash
    docker-compose up --build
    ```

3.  **Erişin**
    Sistem ayağa kalktığında aşağıdaki adreslerden erişebilirsiniz:
    *   API Dokümantasyonu (Swagger): `http://localhost:8000/docs` - Önerilen test yöntemi.
    *   Test Arayüzü (Web UI): `http://localhost:8000` - API yanıtlarını görselleştirmek için basit arayüz.