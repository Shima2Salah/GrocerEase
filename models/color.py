#!/usr/bin/python3
""" holds class Color"""
import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, Integer, ForeignKey, Table
from sqlalchemy.orm import relationship

if models.storage_t == 'db':
    products_colors = Table('products_colors', Base.metadata,
				Column('product_id', Integer,
                                 ForeignKey('products.id', onupdate='CASCADE',
                                            ondelete='CASCADE'),
                                 primary_key=True),
                   	       Column('color_id', Integer,
                                 ForeignKey('colors.id', onupdate='CASCADE',
                                            ondelete='CASCADE'),
                                 primary_key=True))


class Color(BaseModel, Base):
    """Representation of color """
    if models.storage_t == 'db':
        __tablename__ = 'colors'
        color_name = Column(String(255), unique=True, nullable=False)
        products = relationship("Product",
		secondary=products_colors)
    else:
        color_name = ""

    def __init__(self, *args, **kwargs):
        """initializes color"""
        super().__init__(*args, **kwargs)
