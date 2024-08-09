#!/usr/bin/python3
""" holds class User"""

import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from hashlib import md5


class User(BaseModel, Base):
    """Representation of a user """
    if models.storage_t == 'db':
        __tablename__ = 'users'
        first_name = Column(String(100), nullable=False)
        last_name = Column(String(100), nullable=False)
        contact_number = Column(String(100), nullable=False)
        email = Column(String(100), nullable=False)
        password = Column(String(100), nullable=True)
        country = Column(String(100), nullable=False)
        company_name = Column(String(100), nullable=False)
        address = Column(String(100), nullable=False)
        state_or_country = Column(String(100), nullable=False)
        postal_or_zip = Column(String(100), nullable=False)
        order_notes = Column(String(255))
        Orders = relationship("Order",
                              backref="users",
                              cascade="all, delete, delete-orphan")
    else:
        first_name = ""
        last_name = ""
        contact_number = ""
        email = ""
        password = ""
        country = ""
        company_name = ""
        address = ""
        state_or_country = ""
        postal_or_zip = ""
        order_notes = ""

    def __init__(self, *args, **kwargs):
        """initializes user"""
        super().__init__(*args, **kwargs)

    '''def __setattr__(self, name, value):
        """to set an encryption password"""
        if name == "password":
            value = md5(value.encode()).hexdigest()
        super().__setattr__(name, value)'''
