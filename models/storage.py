from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from data.base import SqlAlchemyBase


class Storage(SqlAlchemyBase):
    __tablename__ = 'storages'

    shop_id = Column(Integer, ForeignKey('shops.id'), primary_key=True)
    product_id = Column(Integer, ForeignKey('products.id'), primary_key=True)
    amount = Column(Integer, nullable=False, default=0)

    shop = relationship("Shop", back_populates="storages")
    product = relationship("Product", back_populates="storages")