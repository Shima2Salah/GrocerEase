#!/usr/bin/python3
""" holds class Order"""
import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, Integer, DECIMAL, ForeignKey
from sqlalchemy.orm import relationship


class Order(BaseModel, Base):
    """Representation of Order """
    if models.storage_t == "db":
        __tablename__ = 'orders'
        user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
        total_price = Column(DECIMAL(10, 2), nullable=False)
        order_items = relationship("OrderItem",
                              backref="orders",
                              cascade="all, delete, delete-orphan")
    else:
        user_id = ""
        total_price = ""

    def __init__(self, *args, **kwargs):
        """initializes Order"""
        super().__init__(*args, **kwargs)
