#!/usr/bin/python3
""" holds class Size"""
import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, Integer, ForeignKey, Table
from sqlalchemy.orm import relationship

if models.storage_t == 'db':
    products_sizes = Table('products_sizes', Base.metadata,
                          Column('product_id', Integer,
                                 ForeignKey('products.id', onupdate='CASCADE',
                                            ondelete='CASCADE'),
                                 primary_key=True),
                          Column('size_id', Integer,
                                 ForeignKey('sizes.id', onupdate='CASCADE',
                                            ondelete='CASCADE'),
                                 primary_key=True))


class Size(BaseModel, Base):
    """Representation of size """
    if models.storage_t == 'db':
        __tablename__ = 'sizes'
        size_name = Column(String(255), unique=True, nullable=False)
        products = relationship("Product",
		secondary=products_sizes)
    else:
        size_name = ""

    def __init__(self, *args, **kwargs):
        """initializes size"""
        super().__init__(*args, **kwargs)
