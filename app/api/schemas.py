from pydantic import BaseModel
from app.core.entities import (
    GenderType, 
    MaritalStatus, 
    EducationLevel, 
    EmploymentStatus, 
    LoanPurpose, 
    GradeType
)

class LoanRequest(BaseModel):
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

class LoanResponse(BaseModel):
    probability: float        
    decision: str               
    application_id: int