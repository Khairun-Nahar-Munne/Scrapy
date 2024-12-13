from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import os
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Hotel(Base):
    __tablename__ = 'hotels'

    id = Column(Integer, primary_key=True, autoincrement=True)
    city_id = Column(Integer, nullable=False)
    hotel_name = Column(String, nullable=False)
    hotel_address = Column(String, nullable=False)
    hotel_img = Column(String, nullable=False)  # This will store the image path
    price = Column(Float, nullable=True)
    comment_score = Column(Float, nullable=True)
    physical_room_name = Column(String, nullable=True)
    lat = Column(Float, nullable=True)
    lng = Column(Float, nullable=True)

    def __repr__(self):
        return f"<Hotel(name={self.hotel_name}, city_id={self.city_id})>"

def create_tables():
    engine = create_engine(os.getenv("DATABASE_URL"))
    Base.metadata.create_all(engine)

Session = sessionmaker(bind=create_engine(os.getenv("DATABASE_URL")))
