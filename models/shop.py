from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from data.base import SqlAlchemyBase


class Shop(SqlAlchemyBase):
    __tablename__ = 'shops'

    id = Column(Integer, primary_key=True, autoincrement=True)
    address = Column(String(200), nullable=False)
    from_shop = Column(String(100))
    schedule = Column(String(200))
    latitude = Column(Float)
    longitude = Column(Float)

    persons = relationship("Person", back_populates="shop")
    storages = relationship("Storage", back_populates="shop")