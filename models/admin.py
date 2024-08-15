#!/usr/bin/python3
""" holds class Admin """
import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from hashlib import md5
from werkzeug.security import generate_password_hash, check_password_hash

class Admin(BaseModel, Base):
    """Representation of Admin"""
    if models.storage_t == 'db':
        __tablename__ = 'admins'
        admin_name = Column(String(100), nullable=False)
        email = Column(String(100), unique=True, nullable=False)
        password_hash = Column(String(1024), nullable=False)
        admin_role_id = Column(Integer, ForeignKey('admin_roles.id'), nullable=False)
        status = Column(Integer)  # This field is optional based on your schema
        products = relationship(
            "Product",
            backref="admins",  # Singular form since this is a many-to-one relationship
            cascade="all, delete, delete-orphan"
        )
        # Relationship to Category
        suppliers = relationship('Supplier', backref='admin_relationship')
        categories = relationship('Category', back_populates='admin')
        products = relationship('Product', back_populates='admin')
        admin_role = relationship('AdminRole', back_populates='admins')
    else:
        admin_name = ""
        email = ""
        password_hash = ""
        admin_role_id = None
        status = None

    '''def __init__(self, *args, **kwargs):
        """Initializes Admin"""
        super().__init__(*args, **kwargs)'''


    '''def __setattr__(self, name, value):
        """to set an encryption password"""
        if name == "password":
            value = md5(value.encode()).hexdigest()
        super().__setattr__(name, value)'''

    def __init__(self, *args, **kwargs):
        """Initializes Admin"""
        if "password" in kwargs:
            kwargs["password_hash"] = self.hash_password(kwargs.pop("password"))
        super().__init__(*args, **kwargs)

    @staticmethod
    def hash_password(password):
        """Generates a hashed password."""
        return generate_password_hash(password)

    def verify_password(self, password):
        """Verify the provided password against the stored hashed password."""
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def get_by_username(cls, username):
        """Retrieve an Admin instance by username."""
        return models.storage.session.query(cls).filter_by(username=username).first()

    def __setattr__(self, name, value):
        """Custom setter to handle password hashing."""
        if name == "password":
            value = self.hash_password(value)
        super().__setattr__(name, value)
