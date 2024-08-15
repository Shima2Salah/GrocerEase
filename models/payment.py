#!/usr/bin/python3
""" holds class Payment """
import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship


class Payment(BaseModel, Base):
    """Representation of Payment"""
    if models.storage_t == 'db':
        __tablename__ = 'payments'
        payment_method = Column(String(100), nullable=False)
        order = relationship('Order', back_populates='payments')
    else:
        payment_method = ""

    def __init__(self, *args, **kwargs):
        """Initializes Payment"""
        super().__init__(*args, **kwargs)
