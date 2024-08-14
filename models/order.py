#!/usr/bin/python3
""" holds class Order"""
import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, Integer, DECIMAL, ForeignKey, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime


class Order(BaseModel, Base):
    """Representation of Order """
    if models.storage_t == "db":
        __tablename__ = 'orders'
        user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
        total_price = Column(DECIMAL(10, 2), nullable=False)
        delivery_id = Column(Integer, ForeignKey('deliveries.id'), nullable=False)
        order_date = Column(DateTime, nullable=False)
        status_id = Column(Integer, ForeignKey('orders_statuses.id'))
        payment_id = Column(Integer, ForeignKey('payments.id'), nullable=False)
        coupon_id = Column(Integer, ForeignKey('coupons.id'))
        delivery_date = Column(DateTime)
        payment_date = Column(DateTime)
        payment_status = Column(Integer)
        order_items = relationship("OrderItem",
                              backref="orders",
                              cascade="all, delete, delete-orphan")
    else:
        user_id = None
        total_price = None
        delivery_id = None
        order_date = None
        status_id = None
        payment_id = None
        coupon_id = None
        delivery_date = None
        payment_date = None
        payment_status = None

    def __init__(self, *args, **kwargs):
        """initializes Order"""
        super().__init__(*args, **kwargs)
