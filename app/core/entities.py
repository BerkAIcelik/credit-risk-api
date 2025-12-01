from datetime import datetime
from dataclasses import dataclass,field
from typing import Optional
from enum import Enum

class GenderType(str, Enum):
    MALE = "Male"
    FEMALE = "Female"
    OTHER = "Other"

class MaritalStatus(str, Enum):
    SINGLE = "Single"
    MARRIED = "Married"
    DIVORCED = "Divorced"
    WIDOWED = "Widowed"

class EducationLevel(str, Enum):
    HIGH_SCHOOL = "High School"
    BACHELOR = "Bachelor's"
    MASTER = "Master's"
    PHD = "PhD"
    OTHER = "Other"

class EmploymentStatus(str, Enum):
    EMPLOYED = "Employed"
    UNEMPLOYED = "Unemployed"
    SELF_EMPLOYED = "Self-employed"
    RETIRED = "Retired"
    STUDENT = "Student"

class LoanPurpose(str, Enum):
    BUSINESS = "Business"
    CAR = "Car"
    DEBT_CONSOLIDATION = "Debt consolidation"
    EDUCATION = "Education"
    HOME = "Home"
    MEDICAL = "Medical"
    OTHER = "Other"
    VACATION = "Vacation"

class GradeType(str, Enum):
    A1 = "A1"
    A2 = "A2"
    A3 = "A3"
    A4 = "A4"
    A5 = "A5"
    B1 = "B1"
    B2 = "B2"
    B3 = "B3"
    B4 = "B4"
    B5 = "B5"
    C1 = "C1"
    C2 = "C2"
    C3 = "C3"
    C4 = "C4"
    C5 = "C5"
    D1 = "D1"
    D2 = "D2"
    D3 = "D3"
    D4 = "D4"
    D5 = "D5"
    E1 = "E1"
    E2 = "E2"
    E3 = "E3"
    E4 = "E4"
    E5 = "E5"
    F1 = "F1"
    F2 = "F2"
    F3 = "F3"
    F4 = "F4"
    F5 = "F5"
    G1 = "G1"
    G2 = "G2"
    G3 = "G3"
    G4 = "G4"
    G5 = "G5"


@dataclass

#Ham veri dataclas burada bizim yerimize init,repr,eq,hash oluşturuyor 
class LoanApplication:
    annual_income:float
    debt_to_income_ratio:float
    credit_score:int
    loan_amount:float
    interest_rate:float
    gender: GenderType
    marital_status: MaritalStatus
    education_level: EducationLevel
    employment_status: EmploymentStatus
    loan_purpose: LoanPurpose
    grade_subgrade: GradeType



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


    
   
    