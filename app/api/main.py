from fastapi import FastAPI,HTTPException,Depends
from sqlalchemy.orm import Session

from app.infrastructure.database import get_db,engine,Base
from app.api.schemas import LoanRequest,LoanResponse
from app.infrastructure.adapters import CatBoostAdapter
from app.infrastructure.db_repository import MySQLRepository
from app.core.entities import LoanApplication
from app.use_cases.loan_processor import ProcessLoanApplication

app = FastAPI(title='Credit Risk API')
Base.metadata.create_all(bind=engine)

MODEL_DIR= "app/infrasturcture/model_artifacts"

try:
    # Model servisini global bir değişken olarak tutuyoruz
    model_service = CatBoostAdapter(MODEL_DIR)
except Exception as e:
    print(f"🚨 KRİTİK HATA: Model yüklenemedi! {e}")


#kullanıcı verileri doldurdu ve gönderdi post isteği olarak biz bunu aldık /predict ile karşıladık
#/predict hemen altındaki predict_endpoint fonksiyonu ile eşleşir ve gelen post istekleri buraya gelir.
#post iburada çift yönlüdür response da verecektir ve vereceği response formatı Loan responsedur
@app.post("/predict", response_model=LoanResponse)

#get_db deki yield ifadesi sayeesinde predict_endpoint tamamlanana kadar session oturum açık duruyor.
#depeneds predict endpoint çalışmadan önce gerekli kaynaklar için get_dbyi çağırır

def predict_endpoint(request: LoanRequest, db: Session = Depends(get_db)):
    try:
        #db Bu işlem için ayrılmış, şu anda aktif olan, veritabanına veri gönderip alabilen özel işlem kanalı ve yönetim nesnesi.
        #MySQL sunucusu ile uygulama arasında yeni bir ağ bağlantısı TCP/IP socket kurar.
        #SQLAlchemy Oturumu Session nesnesidir.
        #Bu oturum, sizin tüm veritabanı işlemlerinizi Transaction kapsayan bir konteynerdir.
        #db o anki veritabanı işlemlerini yönetme sorumluluğu taşır.

        # "Bu işlem için şu veritabanı oturumunu kullan" diyoruz.
        repository = MySQLRepository(db)
        
        # Use Case'i Hazırla Dependency Injection
        # Al sana yüklü model, al sana canlı veritabanı bağlantısı. constructor ile oluştur bunları.
        use_case = ProcessLoanApplication(model_service, repository)
        
        # DTO Pydanticten Entitye Domain Dönüşümü
        # Kullanıcıdan gelen JSON verisini, bizim iç dünyamızdaki Entity'e çeviriyoruz.
        # **request.dict : JSON'daki alanları otomatik olarak eşleştirir.
        application_entity = LoanApplication(**request.dict())
        
        
        # Tüm iş mantığı, kurallar, tahmin ve kayıt burada olur.
        result_entity = use_case.execute(application_entity)
        
        # Cevabı Dön Entityden DTO ya
        return LoanResponse(
            probability=result_entity.probability,
            decision=result_entity.decision,
            application_id=result_entity.application_id,
        )
        
    except ValueError as e:
        # İş kuralı hatası örn: Gelir negatif -> 400 Bad Request
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # Beklenmedik hata -> 500 Internal Server Error
        print(f"Sunucu Hatası: {e}")
        raise HTTPException(status_code=500, detail="Sunucu tarafında bir hata oluştu.")

