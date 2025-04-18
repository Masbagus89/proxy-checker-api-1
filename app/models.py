from sqlalchemy import Column, String, Integer
from app.database import Base, SessionLocal

class Proxy(Base):
    __tablename__ = "proxies"
    id = Column(Integer, primary_key=True, index=True)
    ip = Column(String, index=True)
    port = Column(String)
    country = Column(String)
    org = Column(String)

def save_proxy(ip, port, country, org):
    db = SessionLocal()
    proxy = Proxy(ip=ip, port=port, country=country, org=org)
    db.add(proxy)
    db.commit()
    db.close()

def get_all_proxies():
    db = SessionLocal()
    proxies = db.query(Proxy).all()
    db.close()
    return [
        {"ip": p.ip, "port": p.port, "country": p.country, "org": p.org}
        for p in proxies
    ]
