#!/usr/bin/python3
""" holds class OrderItem"""
import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, DECIMAL, Integer, ForeignKey, DateTime
from datetime import datetime
from sqlalchemy.orm import relationship


class OrderItem(BaseModel, Base):
    """Representation of OrderItem """
    if models.storage_t == "db":
        __tablename__ = 'order_items'
        product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
        amount = Column(DECIMAL(10, 2), nullable=False)
        price = Column(DECIMAL(10, 2), nullable=False)
        order_id = Column(Integer, ForeignKey('orders.id'), nullable=False)
        # Relationship to Category
        product = relationship('Product', back_populates='order_items')
        order = relationship('Order', back_populates='order_items')
    else:
        order_id = ""
        product_id = ""
        amount = ""
        price = ""

    def __init__(self, *args, **kwargs):
        """initializes OrderItem"""
        super().__init__(*args, **kwargs)
