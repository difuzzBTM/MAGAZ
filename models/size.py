from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from data.base import SqlAlchemyBase


class Size(SqlAlchemyBase):
    __tablename__ = 'sizes'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(20), nullable=False)

    product_sizes = relationship("ProductSize", back_populates="size")