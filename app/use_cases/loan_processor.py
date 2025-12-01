#burada amac kredi basvurusunu al kurallardan gecırıp kaydet
#yeni kuralları buraya ekleyeceksin mesela maaşı 10000 altıysa çalıştırma diyebilirsin.  burası ethodun fonksiyonun hangi kurallarla çalışacağını söylüyor yani hangi şartlar sağlanırsa

from dataclasses import fields
from app.core.entities import LoanApplication, PredictionResults
from app.core.interfaces import IModelService, ILoanRepository

#başlarken diyo benden bir nesne oluşturmak istediğinde bana bi model ve bir depo alanı ver
class ProcessLoanApplication:
    def __init__(self, model_service: IModelService, loan_repository: ILoanRepository):
        self.model_service = model_service
        self.loan_repository = loan_repository
#aplplication bir loanapplication entities i yani loan application varlığı,result ise bir prediction result varlığı

    def _validate_application(self, application: LoanApplication):

        # dataclass'ın içindeki alanların listesini alıyoruz Reflection
        for field in fields(application):
            # O alanın o anki değerini alıyoruz örn: annual_income değeri 50000
            value = getattr(application, field.name)
            
            # Kural: Sayısal int/float ve Negatif ise HATA
            if isinstance(value, (int, float)):
                if value < 0:
                    raise ValueError(f"Hata: '{field.name}' alanı negatif olamaz! (Gelen: {value})")
            
            
        
        # Ekstra Özel Kurallar Sıfır Kontrolü vb.
        if application.loan_amount == 0:
             raise ValueError("Kredi miktarı 0 olamaz!")
        
    def execute(self, application:LoanApplication)->PredictionResults:

        self._validate_application(application)

        #resultun neden predicitonresults nesnesi olduğu buada kanıtlı prediction fonksiyonu sayesinde
        result=self.model_service.predict(application)

        save_id = self.loan_repository.save(application,result)

        result.application_id=save_id

        return result