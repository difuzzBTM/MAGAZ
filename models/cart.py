from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from data.base import SqlAlchemyBase


class Cart(SqlAlchemyBase):
    __tablename__ = 'carts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    person_id = Column(Integer, ForeignKey('persons.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    size_id = Column(Integer, ForeignKey('sizes.id'), nullable=False)
    amount = Column(Integer, nullable=False, default=1)

    person = relationship("Person", back_populates="carts")
    product = relationship("Product", back_populates="carts")
    size = relationship("Size")