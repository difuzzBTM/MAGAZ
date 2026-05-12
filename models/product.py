from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey
from sqlalchemy.orm import relationship
from data.base import SqlAlchemyBase


class Product(SqlAlchemyBase):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(200), nullable=False)
    photos = Column(Text)
    cost = Column(Float, nullable=False)
    description = Column(Text)

    type_id = Column(Integer, ForeignKey('product_types.id'), nullable=True)

    type = relationship("ProductType", back_populates="products")
    product_sizes = relationship("ProductSize", back_populates="product")
    storages = relationship("Storage", back_populates="product")
    carts = relationship("Cart", back_populates="product")
    order_items = relationship("OrderItem", back_populates="product")