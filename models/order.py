from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from data.base import SqlAlchemyBase


class Order(SqlAlchemyBase):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, autoincrement=True)
    person_id = Column(Integer, ForeignKey('persons.id'), nullable=False)
    payment_type_id = Column(Integer, ForeignKey('payment_types.id'), nullable=True)
    order_type_id = Column(Integer, ForeignKey('order_types.id'), nullable=True)
    delivery_address = Column(String(300))

    person = relationship("Person", back_populates="orders")
    payment_type_rel = relationship("PaymentType", back_populates="orders")
    order_type_rel = relationship("OrderType", back_populates="orders")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")