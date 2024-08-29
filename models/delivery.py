#!/usr/bin/python3
""" holds class Delivery """
import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship

class Delivery(BaseModel, Base):
    """Representation of Delivery"""
    if models.storage_t == 'db':
        __tablename__ = 'deliveries'
        delivery_name = Column(String(100), nullable=False)
        contact_number = Column(String(50), nullable=False)
        address = Column(String(100), nullable=False)
        is_active = Column(Integer, nullable=False)

        orders = relationship('Order', back_populates='delivery')
    else:
        delivery_name = ""
        contact_number = ""
        address = ""
        is_active = 1  # Default to active (1)

    def __init__(self, *args, **kwargs):
        """Initializes Delivery"""
        super().__init__(*args, **kwargs)
