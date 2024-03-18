#!/usr/bin/python3
""" New class for SQLAlchemy """
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
from sqlalchemy.ext.declarative import declarative_base
from models.base_model import Base
from models.state import State
from models.city import City
from models.user import User
from models.place import Place
from models.review import Review
from models.amenity import Amenity


class DBStorage:
    """Class for managing the SQLAlchemy database"""
    __engine = None
    __session = None

    def __init__(self):
        """Create the engine and session"""
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'
                                      .format(os.getenv('HBNB_MYSQL_USER'),
                                              os.getenv('HBNB_MYSQL_PWD'),
                                              os.getenv('HBNB_MYSQL_HOST'),
                                              os.getenv('HBNB_MYSQL_DB')),
                                      pool_pre_ping=True)
        if os.getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Query all objects of a class"""
        objects = {}
        if cls is not None:
            for obj in self.__session.query(cls).all():
                key = '{}.{}'.format(obj.__class__.__name__, obj.id)
                objects[key] = obj
        else:
            for c in [state.State, city.City]:
                for obj in self.__session.query(c).all():
                    key = '{}.{}'.format(obj.__class__.__name__, obj.id)
                    objects[key] = obj
        return objects

    def new(self, obj):
        """Add an object to the session"""
        self.__session.add(obj)

    def save(self):
        """Commit all changes to the session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete an object from the session"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """Create all tables and session"""
        Base.metadata.create_all(self.__engine)
        self.__session = scoped_session(sessionmaker(
            bind=self.__engine, expire_on_commit=False))
