#!/usr/bin/python3
""" holds class Discount """
import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, Integer, Numeric, DateTime
from sqlalchemy.orm import relationship

class Discount(BaseModel, Base):
    """Representation of Discount"""
    if models.storage_t == 'db':
        __tablename__ = 'discounts'
        discount_percentage = Column(Numeric(10, 2), nullable=False)
        start_date = Column(DateTime, nullable=False)
        end_date = Column(DateTime, nullable=False)
        products = relationship(
            "Product",
            backref="discounts",  # Singular form since this is a many-to-one relationship
            cascade="all, delete, delete-orphan")
        products = relationship('Product', back_populates='discount')
        # Override BaseModel columns to remove them
        created_at = None
        updated_at = None
    else:
        discount_percentage = 0.00
        start_date = None
        end_date = None

    def __init__(self, *args, **kwargs):
        """Initializes Discount"""
        super().__init__(*args, **kwargs)
