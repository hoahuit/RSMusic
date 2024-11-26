from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URI = 'mssql+pyodbc://sa:123@minhhoa/re?driver=ODBC+Driver+17+for+SQL+Server'

# Tạo kết nối đến cơ sở dữ liệu
engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)

def get_session():
    """Hàm trả về một phiên làm việc mới (session)"""
    return Session()
