from sqlalchemy import ForeignKey, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from datetime import datetime

Base = declarative_base()

class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    quantity = Column(Integer, default=0)
    price = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.now)

    def __repr__(self):
        return f"<Product(name='{self.name}', quantity={self.quantity}, price={self.price})>"

class Transaction(Base):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, nullable=False)
    quantity = Column(Integer, nullable=False)
    transaction_type = Column(String, nullable=False)
    date = Column(DateTime, default=datetime.now)

    def __repr__(self):
        return f"<Transaction(product_id={self.product_id}, quantity={self.quantity}, type='{self.transaction_type}')>"
    
class StockMovement(Base):
    __tablename__ = 'stock_movements'

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    movement_type = Column(String, nullable=False)
    date = Column(DateTime, default=datetime.now, nullable=False)

    product = relationship('Product', back_populates='movements')

Product.movements = relationship('StockMovement', order_by=StockMovement.id, back_populates='product')
