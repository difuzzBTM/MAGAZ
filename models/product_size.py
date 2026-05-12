from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from data.base import SqlAlchemyBase


class ProductSize(SqlAlchemyBase):
    __tablename__ = 'product_sizes'

    product_id = Column(Integer, ForeignKey('products.id'), primary_key=True)
    size_id = Column(Integer, ForeignKey('sizes.id'), primary_key=True)

    product = relationship("Product", back_populates="product_sizes")
    size = relationship("Size", back_populates="product_sizes")