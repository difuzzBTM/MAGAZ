from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from data.db_session import SqlAlchemyBase
from werkzeug.security import generate_password_hash, check_password_hash

class ProductType(SqlAlchemyBase):
    __tablename__ = 'product_types'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)

    products = relationship("Product", back_populates="type")



class Size(SqlAlchemyBase):
    __tablename__ = 'sizes'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(20), nullable=False)

    product_sizes = relationship("ProductSize", back_populates="size")



class PaymentType(SqlAlchemyBase):
    __tablename__ = 'payment_types'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)

    orders = relationship("Order", back_populates="payment_type_rel")



class OrderType(SqlAlchemyBase):
    __tablename__ = 'order_types'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)

    orders = relationship("Order", back_populates="order_type_rel")



class Shop(SqlAlchemyBase):
    __tablename__ = 'shops'

    id = Column(Integer, primary_key=True, autoincrement=True)
    address = Column(String(200), nullable=False)
    from_shop = Column(String(100))
    schedule = Column(String(200))

    persons = relationship("Person", back_populates="shop")
    storages = relationship("Storage", back_populates="shop")



class Person(SqlAlchemyBase):
    __tablename__ = 'persons'

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(100), unique=True, nullable=False)
    surname = Column(String(50), nullable=False)
    name = Column(String(50), nullable=False)
    password = Column(String(255), nullable=False)
    login = Column(String(50), unique=True, nullable=False)
    address = Column(String(200))

    id_shop = Column(Integer, ForeignKey('shops.id'), nullable=True)

    shop = relationship("Shop", back_populates="persons")
    carts = relationship("Cart", back_populates="person")
    orders = relationship("Order", back_populates="person")

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)



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


class Order(SqlAlchemyBase):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, autoincrement=True)
    person_id = Column(Integer, ForeignKey('persons.id'), nullable=False)
    payment_type_id = Column(Integer, ForeignKey('payment_types.id'), nullable=True)
    order_type_id = Column(Integer, ForeignKey('order_types.id'), nullable=True)

    person = relationship("Person", back_populates="orders")
    payment_type_rel = relationship("PaymentType", back_populates="orders")
    order_type_rel = relationship("OrderType", back_populates="orders")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")




class ProductSize(SqlAlchemyBase):
    __tablename__ = 'product_sizes'

    product_id = Column(Integer, ForeignKey('products.id'), primary_key=True)
    size_id = Column(Integer, ForeignKey('sizes.id'), primary_key=True)

    product = relationship("Product", back_populates="product_sizes")
    size = relationship("Size", back_populates="product_sizes")



class Storage(SqlAlchemyBase):
    __tablename__ = 'storages'

    shop_id = Column(Integer, ForeignKey('shops.id'), primary_key=True)
    product_id = Column(Integer, ForeignKey('products.id'), primary_key=True)
    amount = Column(Integer, nullable=False, default=0)

    shop = relationship("Shop", back_populates="storages")
    product = relationship("Product", back_populates="storages")


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

class UserAddress(SqlAlchemyBase):
    __tablename__ = 'user_addresses'

    id = Column(Integer, primary_key=True, autoincrement=True)
    person_id = Column(Integer, ForeignKey('persons.id'), nullable=False)
    address = Column(String(200), nullable=False)
    is_default = Column(Boolean, default=False)

    person = relationship("Person", backref="addresses")


class UserPaymentMethod(SqlAlchemyBase):
    __tablename__ = 'user_payment_methods'

    id = Column(Integer, primary_key=True, autoincrement=True)
    person_id = Column(Integer, ForeignKey('persons.id'), nullable=False)
    card_number = Column(String(19), nullable=False)
    card_type = Column(String(20))
    is_default = Column(Boolean, default=False)

    person = relationship("Person", backref="payment_methods")

