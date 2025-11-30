from abc import ABC, abstractmethod
from app.core.entities import LoanApplication, PredictionResults

#bir tane abstractclass oluşturdum. Bu bir sözleşme oluşturdu ve kontrolü sağladı. artık bu classtan oluşturulmuş subclassların bu methodu olmak zorunda
#alt sınıflar bunu implement ederken anlarsın ztn

class IModelService(ABC):
    @abstractmethod
    #diyor ki bağlandığım nesnede yani beni çağırdığında loanapplication türünden bir değer atanıcak içime ve çıktı türü prediction results dan gelicek
    #fakat içerde ne yaptığın hangi işlem olduğu beni ilgilendirmez ben sadece ismini koyuyorum.
    #Arka planda CatBoost mu var, XGBoost mu var, yoksa yazı tura mı atılıyor?
    #katmanı bunu bilmez ve umursamaz.
    def predict(self, apllication:LoanApplication)-> PredictionResults:
        pass

class ILoanRepository(ABC):
    @abstractmethod
    #Veritabanının uyması gereken sözleşme.
    #Verinin MySQL'e mi, Excel'e mi yoksa Buluta mı kaydedildiği buradaki iş mantığını ilgilendirmez.Çünkü sadece kuraldır
    def save(self,application:LoanApplication,prediction:PredictionResults)->int:
        pass
