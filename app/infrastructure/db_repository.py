from sqlalchemy.orm import Session
from app.core.interfaces import ILoanRepository
from app.core.entities import LoanApplication,PredictionResults
from app.infrastructure.db_models import LoanApplicationModel

class MySQLRepository(ILoanRepository):
    def __init__(self,db:Session):
        self.db=db
    def save(self, application:LoanApplication,result:PredictionResults)->int:
        db_record = LoanApplicationModel(
            annual_income=application.annual_income,
            debt_to_income_ratio = application.debt_to_income_ratio,
            credit_score = application.credit_score,
            loan_amount = application.loan_amount,
            interest_rate = application.interest_rate,

            gender = application.gender,
            marital_status = application.marital_status,
            education_level = application.education_level,
            employment_status = application.employment_status,
            loan_purpose = application.loan_purpose,
            grade_subgrade = application.grade_subgrade,

            # Modelin ne cevap verdiğini de kaydediyoruz
            prediction_probability =   result.probability,
            prediction_decision =  result.decision,
            threshold_used = result.threshold_used,

            created_at = result.created_at
        )
        self.db.add(db_record)
        self.db.commit()
        self.db.refresh(db_record)
        return db_record.id