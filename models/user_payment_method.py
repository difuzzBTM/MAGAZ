from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from data.base import SqlAlchemyBase


class UserPaymentMethod(SqlAlchemyBase):
    __tablename__ = 'user_payment_methods'

    id = Column(Integer, primary_key=True, autoincrement=True)
    person_id = Column(Integer, ForeignKey('persons.id'), nullable=False)
    card_number = Column(String(19), nullable=False)
    card_type = Column(String(20))
    is_default = Column(Boolean, default=False)

    person = relationship("Person", back_populates="payment_methods")