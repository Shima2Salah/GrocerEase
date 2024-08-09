#!/usr/bin/python3
""" holds class OrderItem"""
import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, DECIMAL, Integer, ForeignKey
from sqlalchemy.orm import relationship


class OrderItem(BaseModel, Base):
    """Representation of OrderItem """
    if models.storage_t == "db":
        __tablename__ = 'order_items'
        order_id = Column(Integer, ForeignKey('orders.id'), nullable=False)
        product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
        quantity = Column(Integer, nullable=False)
        price = Column(DECIMAL(10, 2), nullable=False)
    else:
        order_id = ""
        product_id = ""
        quantity = ""
        price = ""

    def __init__(self, *args, **kwargs):
        """initializes OrderItem"""
        super().__init__(*args, **kwargs)
