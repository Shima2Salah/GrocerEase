#!/usr/bin/python3
""" holds class OrderStatus """
import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship


class OrderStatus(BaseModel, Base):
    """Representation of OrderStatus"""
    if models.storage_t == 'db':
        __tablename__ = 'orders_statuses'
        status_name = Column(String(100), nullable=False)
        orders = relationship('Order', back_populates='order_status')
        # Override BaseModel columns to remove them
        created_at = None
        updated_at = None
    else:
        status_name = ""

    def __init__(self, *args, **kwargs):
        """Initializes OrderStatus"""
        super().__init__(*args, **kwargs)
