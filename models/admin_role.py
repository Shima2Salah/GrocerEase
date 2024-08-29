#!/usr/bin/python3
""" holds class AdminRole """
import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship


class AdminRole(BaseModel, Base):
    """Representation of AdminRole"""
    if models.storage_t == 'db':
        __tablename__ = 'admin_roles'
        admin_role_name = Column(String(100), nullable=False)
        admin_role_description = Column(String(255))
        admins = relationship(
            "Admin",
            backref="admin_roles",  # Singular form since this is a many-to-one relationship
            cascade="all, delete, delete-orphan"
        )
        # Relationship to Product
        admins = relationship('Admin', back_populates='admin_role')
        # Override BaseModel columns to remove them
        created_at = None
        updated_at = None
        is_deleted = None
        deleted_at = None
    else:
        admin_role_name = ""
        admin_role_description = ""

    def __init__(self, *args, **kwargs):
        """Initializes AdminRole"""
        super().__init__(*args, **kwargs)
