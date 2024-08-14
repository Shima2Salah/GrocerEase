#!/usr/bin/python3
""" holds class Product"""
import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, Integer, Float, ForeignKey, DECIMAL, DateTime
from sqlalchemy.orm import relationship


class Product(BaseModel, Base):
    """Representation of Product """
    if models.storage_t == "db":
        __tablename__ = 'products'
        product_name = Column(String(255), nullable=False)
        unit_price = Column(DECIMAL(10, 2))
        image_url = Column(String(255))
        description = Column(String(255))
        supplier_id = Column(Integer, ForeignKey('suppliers.id'), nullable=False)
        created_by_admin_id = Column(Integer, ForeignKey('admins.id'), nullable=False)
        discount_id = Column(Integer, ForeignKey('discounts.id'))
        stock_weight = Column(DECIMAL(10, 2))
        weight = Column(DECIMAL(10, 2))
        category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)
        order_items = relationship("OrderItem",
                              backref="products",
                              cascade="all, delete, delete-orphan")
    else:
        product_name = ""
        unit_price = None
        image_url = ""
        description = ""
        supplier_id = None
        created_by_admin_id = None
        discount_id = None
        created_at = None
        updated_at = None
        stock_weight = None
        weight = None
        category_id = None

    def __init__(self, *args, **kwargs):
        """initializes Product"""
        super().__init__(*args, **kwargs)
