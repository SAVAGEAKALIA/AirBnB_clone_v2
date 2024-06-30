#!/usr/bin/python3
"""
This module defines a base class
for all models in our hbnb clone
"""
import uuid
from os import getenv
from datetime import datetime
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
#import logging
#logging.basicConfig()
#logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)


Base = declarative_base()


class BaseModel:
    """A base class for all hbnb models"""
    #if getenv('HBNB_TYPE_STORAGE') == 'db':
    id = Column(String(60), primary_key=True, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow())

    def __init__(self, *args, **kwargs):
        """Instantiates a new model"""
        self.id = str(uuid.uuid4())
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

        if kwargs:
            for key, value in kwargs.items():
                if key == 'created_at' or key == 'updated_at':
                    value = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f")
                if key != '__class__' and hasattr(self.__class__, key):
                    setattr(self, key, value)

    def __str__(self):
        """Returns a string representation of the instance"""
        dict = self.__dict__.copy()
        dict.pop('_sa_instance_state', None)
        cls = (str(type(self)).split('.')[-1]).split('\'')[0]
        return '[{}] ({}) {}'.format(cls, self.id, dict)

    def save(self):
        """
        Updates updated_at with
        current time when instance is changed
        """
        import models
        self.updated_at = datetime.now()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        """Convert instance into dict format"""
        dictionary = self.__dict__.copy()
        #print(f"Before popping _sa_instance_state: {dictionary}")
        dictionary.pop('_sa_instance_state', None)
        #print(f"After popping _sa_instance_state: {dictionary}")
        dictionary['__class__'] = (str(type(self)).\
            split('.')[-1]).split('\'')[0]
        dictionary['created_at'] = self.created_at.isoformat()
        dictionary['updated_at'] = self.updated_at.isoformat()
        return dictionary

    def delete(self):
        """Method to delete current instance from storage"""
        import models
        models.storage.delete(self)
