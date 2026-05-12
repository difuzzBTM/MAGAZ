from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from data.base import SqlAlchemyBase


class ProductType(SqlAlchemyBase):
    __tablename__ = 'product_types'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)

    products = relationship("Product", back_populates="type")