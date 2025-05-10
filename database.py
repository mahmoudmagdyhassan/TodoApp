from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATABASE_URL='sqlite:///./todosapp.db'
#create_engine: بيقوم بإنشاء الاتصال بقاعدة البيانات.

engine=create_engine(SQLALCHEMY_DATABASE_URL,connect_args={'check_same_thread':False})
#SessionLocal: هو session maker بيستخدم لإنشاء جلسات اتصال مع قاعدة البيانات.


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#يحدد الكائن الأساسي الذي يجب أن يرث منه جميع النماذج. عند إنشاء نموذج (Model) جديد، يجب أن يرث من Base ليكون جزءاً من قاعدة البيانات.

Base = declarative_base()