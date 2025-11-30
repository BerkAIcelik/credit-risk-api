#Python ve mysql arasında bir tercüman inşaa ediyoruz burada

from sqlalchemy import Column,Float,Integer,String
from app.infrastructure.database import Base
from datetime import datetime

class LoanApplicationModel(Base):
    __tablename__= "loan_applications"
    id= Column(Integer,primary_key=True,index=True,autoincrement=True)

    annual_income = Column(Float, nullable=False)
    debt_to_income_ratio = Column(Float, nullable=False)
    credit_score = Column(Integer, nullable=False)
    loan_amount = Column(Float, nullable=False)
    interest_rate = Column(Float, nullable=False)

    gender = Column(String(10))
    marital_status = Column(String(20))
    education_level = Column(String(20))
    employment_status = Column(String(30))
    loan_purpose = Column(String(25))
    grade_subgrade = Column(String(10))

     # Modelin ne cevap verdiğini de kaydediyoruz (Denetim/Audit için).
    prediction_probability = Column(Float)  # Örn: 0.85
    prediction_decision = Column(String(10)) # "ONAY" / "RED"
    threshold_used = Column(Float)          # O an kullanılan eşik (0.7079)
    

    