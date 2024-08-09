#!/usr/bin/python3
""" holds class Product"""
import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship


class Product(BaseModel, Base):
    """Representation of Product """
    if models.storage_t == "db":
        __tablename__ = 'products'
        product_name = Column(String(255), nullable=False)
        price = Column(Float, nullable=False)
        description = Column(String(255))
        image_url = Column(String(255))
        category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)
        order_items = relationship("OrderItem",
                              backref="products",
                              cascade="all, delete, delete-orphan")
    else:
        product_name = ""
        price = ""
        description = ""
        image_url = ""
        category_id = ""

    def __init__(self, *args, **kwargs):
        """initializes Product"""
        super().__init__(*args, **kwargs)
