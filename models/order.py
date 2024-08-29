#!/usr/bin/python3
""" holds class Order"""
import models
from models.base_model import BaseModel, Base
from models.coupon import Coupon
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, Integer,
	DECIMAL, ForeignKey, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime


class Order(BaseModel, Base):
    """Representation of Order """
    if models.storage_t == "db":
        __tablename__ = 'orders'
        user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
        total_price = Column(DECIMAL(10, 2), nullable=False)
        delivery_id = Column(Integer, ForeignKey('deliveries.id'))
        order_date = Column(DateTime, default=datetime.utcnow, nullable=False)
        status_id = Column(Integer, ForeignKey('orders_statuses.id'), nullable=False, default=1)
        payment_id = Column(Integer, ForeignKey('payments.id'), nullable=False)
        coupon_id = Column(Integer, ForeignKey('coupons.id'))
        delivery_date = Column(DateTime)
        payment_date = Column(DateTime)
        payment_status = Column(Integer)
        final_price = Column(DECIMAL(10, 2), nullable=False)
        order_items = relationship("OrderItem",
                              backref="orders",
                              cascade="all, delete, delete-orphan")
        # Define the relationship
        payment = relationship('Payment', back_populates='orders')
        user = relationship('User', back_populates='orders')
        delivery = relationship('Delivery', back_populates='orders')
        order_status = relationship('OrderStatus', back_populates='orders')
        order_items = relationship('OrderItem', back_populates='order')
        coupon = relationship('Coupon', back_populates='orders')
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

    @property
    def categories(self):
        return list({item.product.category for item in self.order_items})

    '''@property
    def calculate_final_price(self):
        """Calculate the final price after applying a coupon."""
        if self.coupon_id:
            coupon = models.storage.get(Coupon, self.coupon_id)
            if coupon and coupon.start_date <= datetime.utcnow() <= coupon.end_date:
                return max(self.total_price - float(coupon.coupon_amount), 0)
        return self.total_price

    @property
    def final_price(self):
        """Get or calculate final price."""
        return self.calculate_final_price

    @final_price.setter
    def final_price(self, value):
        """Set final price."""
        self._final_price = value

    def __init__(self, *args, **kwargs):
        """initializes Order"""
        super().__init__(*args, **kwargs)
        if not self.final_price:
            self.final_price = self.calculate_final_price'''
