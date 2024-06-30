#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Integer, Column, String
from sqlalchemy import ForeignKey, Float, Table
from os import getenv
from sqlalchemy.orm import relationship

place_amenity = Table ('place_amenity', Base.metadata,
                       Column('place_id', String(60), ForeignKey('places.id'),
                              primary_key=True, nullable=False),
                       Column('amenity_id', String(60), ForeignKey('amenities.id'),
                              primary_key=True, nullable=False))
class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = 'places'
    city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    number_rooms = Column(Integer,nullable=False, default=0)
    number_bathrooms = Column(Integer,nullable=False, default=0)
    max_guest = Column(Integer,nullable=False, default=0)
    price_by_night = Column(Integer,nullable=False, default=0)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    amenity_ids = []

    if getenv('HBNB_TYPE_STORAGE') == 'db':
        reviews = relationship('Review', backref='place', cascade='all, delete-orphan')
        amenities = relationship('Amenity', secondary=place_amenity, back_populates='places')
    else:
        @property
        def reviews(self):
            """Getter for reviews when using file storage"""
            from models import storage
            review_list = []
            for review in storage.all('Review').values():
                if review.place_id == self.id:
                    review_list.append(review)
            return review_list

        @property
        def amenities(self):
            """Getter for amenities when using file storage"""
            from models import storage
            from models.amenity import Amenity
            amenity_list = []
            for amenity_id in self.amenity_ids:
                amenity = storage.get(Amenity, amenity_id)
                if amenity:
                    amenity_list.append(amenity)
            return amenity_list

        @amenities.setter
        def amenities(self, amenity):
            """Setter for amenities when using file storage"""
            from models.amenity import Amenity
            if isinstance(amenity, Amenity) and \
                    amenity.id not in self.amenity_ids:
                self.amenity_ids.append(amenity.id)
