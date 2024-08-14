#!/usr/bin/python3
""" holds class Admin """
import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

class Admin(BaseModel, Base):
    """Representation of Admin"""
    if models.storage_t == 'db':
        __tablename__ = 'admins'
        admin_name = Column(String(100), nullable=False)
        email = Column(String(100), unique=True, nullable=False)
        password_hash = Column(String(100), nullable=False)
        admin_role_id = Column(Integer, ForeignKey('admin_roles.id'), nullable=False)
        status = Column(Integer)  # This field is optional based on your schema
        products = relationship(
            "Product",
            backref="admins",  # Singular form since this is a many-to-one relationship
            cascade="all, delete, delete-orphan"
        )

    else:
        admin_name = ""
        email = ""
        password_hash = ""
        admin_role_id = None
        status = None

    def __init__(self, *args, **kwargs):
        """Initializes Admin"""
        super().__init__(*args, **kwargs)
