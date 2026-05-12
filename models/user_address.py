from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from data.base import SqlAlchemyBase


class UserAddress(SqlAlchemyBase):
    __tablename__ = 'user_addresses'

    id = Column(Integer, primary_key=True, autoincrement=True)
    person_id = Column(Integer, ForeignKey('persons.id'), nullable=False)
    address = Column(String(200), nullable=False)
    formatted_address = Column(String(300))
    latitude = Column(Float)
    longitude = Column(Float)
    is_default = Column(Boolean, default=False)

    person = relationship("Person", back_populates="addresses")