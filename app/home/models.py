from sqlalchemy import Binary, Column, Integer, String, DateTime
from sqlalchemy.dialects.mysql import TINYINT, MEDIUMTEXT

from app import db, login_manager

class Hotel(db.Model):

    seq_id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    id = Column(String(20))
    order_id = Column(Integer)
    name = Column(String(100))
    rating = Column(String(20))
    address = Column(String(100))
    zip = Column(String(10))
    town = Column(String(50))
    sidecode = Column(String(11))
    country = Column(String(50))
    hotel_description = Column(MEDIUMTEXT)
    hotel_smalldesc = Column(String(255))
    hotel_services = Column(MEDIUMTEXT)
    arrival = Column(String(50))
    departure = Column(String(50))
    location = Column(String(50))
    website = Column(String(500))
    phone = Column(String(100))
    mails1 = Column(MEDIUMTEXT)
    mails2 = Column(MEDIUMTEXT)
    mails3 = Column(MEDIUMTEXT)
    numero_stelle = Column(String(50))
    tipologia_struttura = Column(String(50))
    author = Column(Integer, nullable=False)
    cover_image = Column(String(200))
    additional_rules = Column(MEDIUMTEXT)
    services = Column(MEDIUMTEXT)

class Images(db.Model):

    id = Column(Integer, primary_key=True, nullable=False, unique=True, autoincrement=True)
    hotel_id1 = Column(String(50))
    filepath = Column(String(255))
    hotel_id = Column(Integer, nullable=False)
