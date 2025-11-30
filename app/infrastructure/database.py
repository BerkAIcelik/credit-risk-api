from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker , declarative_base


#Veritabanı Bağlantı Adresi Connection String
# Bu adres, Python'un MySQL ile konuşması için gereken telefon numarası gibidir.
# Yapısı şöyledir: mysql+pymysql://<KULLANICI>:<SIFRE>@<ADRES>:<PORT>/<VERITABANI_ADI>

SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:password@localhost:3306/loan_db"

#Engine, veritabanı ile Python arasındaki fiziksel bağlantıyı yöneten nesnedir.
# echo=True yaptık ki, arka planda çalışan SQL sorgularını terminalde görebilelim
#
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=True
)

# Veritabanıyla her işlem yapacağımızda "Ekleme, Silme" bize yeni bir 'Session' "Oturum" lazım.
# Bu sınıf, o oturumları üreten fabrikadır.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# İleride oluşturacağımız Tablo Modelleri db_models.py, bu sınıftan miras alacak.
# Bu sayede SQLAlchemy, "Hangi sınıflar veritabanı tablosudur?" sorusunu cevaplayabilir.
Base = declarative_base()

# Bu fonksiyon, FastAPI Bağımlılık Dependency yönetimi için kullanılır.
# Temel amacı, her gelen API isteği için veritabanı bağlantısını güvenle açıp kapatmaktır.
def get_db():
    #session açtık

    db=SessionLocal()
    try:
        # 'yield' anahtar kelimesi, 'db' Session nesnesini çağıran FastAPI Endpoint'ine iletir.
        # FONKSİYON BU NOKTADA ASKIDA KALIR Suspended.
        # Session, HTTP Request'in alınmasından HTTP Response'un oluşturulmasına kadar AÇIK KALIR ve kullanılır.
        yield db
    finally:
        db.close()
# Bu, her Request için yeni ve temiz bir Session kullanılmasını sağlayan yüksek kararlılıklı robust bir mimaridir.
#çalışsın çalışmasın her türlü finally e uğrayacak.