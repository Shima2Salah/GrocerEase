#!/usr/bin/python3
""" holds class Category """
import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship


class Category(BaseModel, Base):
    """Representation of Category"""
    if models.storage_t == 'db':
        __tablename__ = 'categories'
        category_name = Column(String(255), unique=True, nullable=False)
        products = relationship(
            "Product",
            backref="categories",  # Singular form since this is a many-to-one relationship
            cascade="all, delete, delete-orphan"
        )
        created_by_admin_id = Column(Integer, ForeignKey('admins.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
        # Relationship to Product
        products = relationship('Product', back_populates='category')
        admin = relationship('Admin', back_populates='categories')
    else:
        category_name = ""
        created_by_admin_id = None

    def __init__(self, *args, **kwargs):
        """Initializes Category"""
        super().__init__(*args, **kwargs)
