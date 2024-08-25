#!/usr/bin/python3
"""
Contains the class DBStorage
"""

import models
from models.admin import Admin
from models.admin_role import AdminRole
from models.base_model import BaseModel, Base
from models.category import Category
from models.coupon import Coupon
from models.delivery import Delivery
from models.discount import Discount
from models.order import Order
from models.order_item import OrderItem
from models.order_status import OrderStatus
from models.payment import Payment
from models.product import Product
from models.user import User
from models.supplier import Supplier
from os import getenv
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

classes = {
    "BaseModel": BaseModel,
    "Product": Product,
    "User": User,
    "Order": Order,
    "OrderItem": OrderItem,
    "Category": Category,
    "Coupon": Coupon,
    "Supplier": Supplier,
    "Admin": Admin,
    "AdminRole": AdminRole,
    "Discount": Discount,
    "Delivery": Delivery,
    "OrderStatus": OrderStatus,
    "Payment": Payment
}

class DBStorage:
    """interacts with the MySQL database"""
    __engine = None
    __session = None

    def __init__(self):
        """Instantiate a DBStorage object"""
        GROCER_MYSQL_USER = getenv('GROCER_MYSQL_USER')
        GROCER_MYSQL_PWD = getenv('GROCER_MYSQL_PWD')
        GROCER_MYSQL_HOST = getenv('GROCER_MYSQL_HOST')
        GROCER_MYSQL_DB = getenv('GROCER_MYSQL_DB')
        GROCER_ENV = getenv('GROCER_ENV')
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(GROCER_MYSQL_USER,
                                             GROCER_MYSQL_PWD,
                                             GROCER_MYSQL_HOST,
                                             GROCER_MYSQL_DB))
        if GROCER_ENV == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """query on the current database session"""
        new_dict = {}
        for clss in classes:
            if cls is None or cls is classes[clss] or cls is clss:
                objs = self.__session.query(classes[clss]).all()
                for obj in objs:
                    key = obj.__class__.__name__ + '.' + str(obj.id)
                    new_dict[key] = obj
        return new_dict

    def new(self, obj):
        """add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete from the current database session obj if not None"""
        if obj is not None:
            # Call the model's delete method instead of directly deleting
            if isinstance(obj, BaseModel):
                obj.delete()
            else:
                self.__session.delete(obj)

    '''def delete(self, obj=None):
        """delete from the current database session obj if not None"""
        if obj is not None:
            self.__session.delete(obj)'''

    def reload(self):
        """reloads data from the databases"""
        Base.metadata.create_all(self.__engine)
        sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sess_factory)
        self.__session = Session

    def close(self):
        """call remove() method on the private session attribute"""
        self.__session.remove()

    def get(self, cls, id):
        """
        Returns the object based on the class name and its ID, or
        None if not found
        """
        if cls not in classes.values():
            return None

        all_cls = models.storage.all(cls)
        for value in all_cls.values():
            if (value.id == id):
                return value

        return None

    def count(self, cls=None):
        """
        count the number of objects in storage
        """
        all_class = classes.values()

        if not cls:
            count = 0
            for clas in all_class:
                count += len(models.storage.all(clas).values())
        else:
            count = len(models.storage.all(cls).values())

        return count

    def query(self, cls):
        """Returns a query object for the given class"""
        if cls not in classes.values():
            return None
        return self.__session.query(cls)

    def get_by_username(self, cls, username):
        """Retrieve an object by username."""
        if cls == Admin:
            return self.session.query(cls).filter_by(admin_name=username).first()
        return None

    @property
    def session(self):
        """Provide direct access to the SQLAlchemy session."""
        return self._DBStorage__session  # Assuming __session is the actual session object

    def filter_by_category(self, model_class, category_id):
        """Return all instances of a class filtered by category_id"""
        if self.__session is None:
            self.reload()  # Ensure the session is loaded
        return self.__session.query(model_class).filter_by(category_id=category_id).all()

    def filter_by_discount(self, cls, discount_id):
        """Return a list of objects of class `cls` filtered by `discount_id`."""
        return self.__session.query(cls).filter(cls.discount_id == discount_id).all()
