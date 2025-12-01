#Python ve mysql arasında bir tercüman inşaa ediyoruz burada

from sqlalchemy import Column,Float,Integer,String,DateTime
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

     # Modelin ne cevap verdiğini de kaydediyoruz
    prediction_probability = Column(Float)  
    prediction_decision = Column(String(10)) 
    threshold_used = Column(Float)          

    created_at = Column(DateTime, default=datetime.now)