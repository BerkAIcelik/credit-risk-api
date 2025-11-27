from datetime import datetime
from dataclasses import dataclass,field
from typing import Optional

@dataclass

#Ham veri dataclas burada bizim yerimize init,repr,eq,hash oluşturuyor 
class LoanApplication:
    annual_income:float
    debt_to_income_ratio:float
    credit_score:int
    loan_amount:float
    interest_rate:float
    gender:str
    marital_status:str
    education_level:str
    employment_status:str
    loan_purpose:str
    grade_subgrade:str

@dataclass
#Çıktımız,çıktı verisi
class PredictionResults:
    probability: float          # Ödeme olasılığı 0.85 gibi
    decision: str               # "ONAY" veya "RED"
    threshold_used: float       # Hangi eşik değerini kullandık? 0.7079=bu modelindeki en kararlı eşik değeri
    application_id: Optional[int] = None  # Veritabanına yazılınca ID alacak, başta yok None derken ,tahmin anında henüz veritabanına kayıt yapmadık, ID'miz yok.
    #Bu yüzden diyoruz ki: Bu alan tamsayı int olacak ama başlangıçta boş None olabilir.


    #created_at: datetime = datetime.now fonskiyonunu kullanmak  neden mantıklı değil çünkü bu ilk Loan application nesnesi oluşturduğunda bundan sonraki hepsine onu atayacak, bu bir class attribute gibi davranır.
    #İnstance attribute gibi davranmasını istiyorsak şu:
    created_at: datetime = field(default_factory=datetime.now)


    
   
    