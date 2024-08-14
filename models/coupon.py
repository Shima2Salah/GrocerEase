#!/usr/bin/python3
""" holds class Coupon """
import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, Integer, String, Numeric, DateTime

class Coupon(BaseModel, Base):
    """Representation of Coupon"""
    if models.storage_t == 'db':
        __tablename__ = 'coupons'
        coupon_code = Column(String(100), unique=True, nullable=False)
        amount = Column(Numeric(10, 2), nullable=False)
        start_date = Column(DateTime, nullable=False)
        end_date = Column(DateTime, nullable=False)
    else:
        coupon_code = ""
        amount = 0.00
        start_date = None
        end_date = None

    def __init__(self, *args, **kwargs):
        """Initializes Coupon"""
        super().__init__(*args, **kwargs)
