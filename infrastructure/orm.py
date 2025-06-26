from sqlalchemy import Column, Integer, String, Float, Table, ForeignKey, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql.functions import func

Base = declarative_base()

class ProductORM(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name=Column(String)
    quantity=Column(Integer)
    price=Column(Float)
    is_active = Column(Boolean, default=True)
    update_datetime = Column(DateTime,  server_default=func.now(), onupdate=func.now())

class OrderORM(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, autoincrement=True)
    create_datetime = Column(DateTime, server_default=func.now())
    update_datetime = Column(DateTime,  server_default=func.now(), onupdate=func.now())
    id_product = Column(Integer, ForeignKey('products.id'))
    is_deleted = Column(Boolean)
    address = Column(String)


order_product_associations = Table(
    'order_product_associations', Base.metadata,
    Column('order_id', ForeignKey('orders.id')),
    Column('product_id', ForeignKey('products.id'))
)

OrderORM.products = relationship("ProductORM", secondary=order_product_associations)
