#!/usr/bin/python3
""" holds class Supplier """
import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship

class Supplier(BaseModel, Base):
    """Representation of Supplier"""
    if models.storage_t == 'db':
        __tablename__ = 'suppliers'
        supplier_name = Column(String(255), nullable=False)
        contact_number = Column(String(50), nullable=False)
        address = Column(String(100), nullable=False)
        created_by_admin_id = Column(Integer, ForeignKey('admins.id'), nullable=False)
        company_name = Column(String(255), nullable=False)
        email = Column(String(100), unique=True, nullable=False)
        notes = Column(String(255))
        products = relationship(
            "Product",
            backref="suppliers",  # Singular form since this is a many-to-one relationship
            cascade="all, delete, delete-orphan"
        )
        
    else:
        supplier_name = ""
        contact_number = ""
        address = ""
        created_by_admin_id = None
        company_name = ""
        email = ""
        notes = ""


    def __init__(self, *args, **kwargs):
        """Initializes Supplier"""
        super().__init__(*args, **kwargs)
