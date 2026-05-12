from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from data.base import SqlAlchemyBase


class OrderItem(SqlAlchemyBase):
    __tablename__ = 'order_items'

    order_id = Column(Integer, ForeignKey('orders.id'), primary_key=True)
    product_id = Column(Integer, ForeignKey('products.id'), primary_key=True)
    size_id = Column(Integer, ForeignKey('sizes.id'), primary_key=True)
    amount = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)

    order = relationship("Order", back_populates="items")
    product = relationship("Product", back_populates="order_items")
    size = relationship("Size")