from passlib.context import CryptContext
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Users  # تأكد إنك معدل المسار حسب مشروعك
from database import Base  # لو عندك Base من declarative_base()

# إنشاء السيشن
DATABASE_URL = "sqlite:///todosapp.db"  # المسار الكامل لقاعدة البيانات

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# إنشاء الباسورد المشفر
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
hashed_password = pwd_context.hash("1234")  # غير الباسورد لو حبيت

# إنشاء المستخدم
admin_user = Users(
    email="scimahmoud@example.com",
    username="ahmed_magdy",
    first_name="ahmed_magdy",
    last_name="magdy_ahmed",
    hashed_password=hashed_password,
    is_active=1,
    role="admin",
    phone_number="01000000000"  # لو مطلوب، ممكن تسيبه فاضي أو تزوده
)

# إضافة المستخدم للـ DB
db = SessionLocal()
db.add(admin_user)
db.commit()
db.refresh(admin_user)
db.close()

print("✅ Admin added to database with ID:", admin_user.id)
