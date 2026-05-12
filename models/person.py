import hashlib
import os
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from data.base import SqlAlchemyBase


class Person(SqlAlchemyBase):
    __tablename__ = 'persons'

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(100), unique=True, nullable=False)
    surname = Column(String(50), nullable=False)
    name = Column(String(50), nullable=False)
    password = Column(String(255), nullable=False)
    login = Column(String(50), unique=True, nullable=False)
    address = Column(String(200))
    newsletter = Column(Boolean, default=False)
    save_history = Column(Boolean, default=False)

    id_shop = Column(Integer, ForeignKey('shops.id'), nullable=True)

    shop = relationship("Shop", back_populates="persons")
    carts = relationship("Cart", back_populates="person")
    orders = relationship("Order", back_populates="person")
    addresses = relationship("UserAddress", back_populates="person")
    payment_methods = relationship("UserPaymentMethod", back_populates="person")

    def set_password(self, password):
        salt = os.urandom(32)
        key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
        self.password = salt.hex() + '$' + key.hex()

    def check_password(self, password):
        salt_hex, key_hex = self.password.split('$')
        salt = bytes.fromhex(salt_hex)
        stored_key = bytes.fromhex(key_hex)
        new_key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
        return new_key == stored_key