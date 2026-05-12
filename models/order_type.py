from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from data.base import SqlAlchemyBase


class OrderType(SqlAlchemyBase):
    __tablename__ = 'order_types'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)

    orders = relationship("Order", back_populates="order_type_rel")