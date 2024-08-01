#!/usr/bin/python3
"""
This module defines a class to manage
database storage for hbnb clone
"""
from os import getenv
from models.base_model import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


# import logging
# logging.basicConfig()
# logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)


class DBStorage:
    """
    This class manages storage of
    hbnb models in Database
    """
    __engine = None
    __session = None

    def __init__(self):
        """ Instance int function for class """
        USER = getenv('HBNB_MYSQL_USER')
        PWD = getenv('HBNB_MYSQL_PWD')
        HOST = getenv('HBNB_MYSQL_HOST')
        DB = getenv('HBNB_MYSQL_DB')
        data_set = 'mysql+mysqldb://{}:{}@{}/{}'.format(USER, PWD, HOST, DB)
        self.__engine = create_engine(data_set, pool_pre_ping=True)

        # Base.metadata.create_all(self.__engine)

        if getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """ query on the current database session (self.__session) all objects
            depending of the class name (argument cls) """
        if cls:
            obj = self.__session.query(cls).all()
        else:
            obj = []
            for i in [State, City, User, Place, Review, Amenity]:
                obj += self.__session.query(i).all()
        new_dict = {}
        for i in obj:
            # key = type(i).__name__ + '.' + i.id
            key = i.to_dict()['__class__'] + '.' + i.id
            new_dict[key] = i

        return new_dict

    def new(self, obj):
        """ add the object to the current database session (self.__session)"""
        # print(f"Adding object to session: {obj}")
        if obj:
            self.__session.add(obj)

    def save(self):
        """ commit all changes of the current database session"""
        # print("Committing changes to the database...")
        self.__session.commit()

    def delete(self, obj=None):
        """ delete from the current database session obj if not None """
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """ create all tables in the database """
        # print("Creating all tables in the database...")
        Base.metadata.create_all(self.__engine)
        sess = scoped_session(sessionmaker(bind=self.__engine,
                                           expire_on_commit=False))
        self.__session = sess()

        # print("Database reloaded successfully.")

    def close(self):
        """call remove() method on the private session attribute"""
        self.__session.remove()
