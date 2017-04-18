from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
 
Base = declarative_base()

class RoomStore(Base):
    """ class to create rooms table """
    __tablename__ = 'rooms'
    room_id = Column(Integer, primary_key=True)
    room_name = Column(String(50), nullable=False)
    room_type = Column(String(50), nullable=False)

class OfficeStore(Base):
    """ class to create office table """
    __tablename__ = 'office'
    room_id = Column(Integer, ForeignKey('rooms.room_id'), primary_key=True)
    occupants = Column(Integer)
    rooms = relationship(RoomStore)

class LSpaceStore(Base):
    """ class to create living space table """
    __tablename__ = 'livingspace'
    room_id = Column(Integer, ForeignKey('rooms.room_id'), primary_key=True)
    occupants = Column(Integer)
    rooms = relationship(RoomStore)
 
class PersonStore(Base):
    """ class to create person table """
    __tablename__ = 'person'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    person_id = Column(Integer, primary_key=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    role = Column(String(50), nullable=False)
    accomodation = Column(String)
 
class FellowStore(Base):
    """ class to create fellows table """
    __tablename__ = 'fellows'
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    person_id = Column(Integer, ForeignKey('person.person_id'), primary_key=True)
    office_name = Column(String)
    accomodation = Column(String)
    person = relationship(PersonStore)

class StaffStore(Base):
    """ class to create staff table """
    __tablename__ = 'staff'
    person_id = Column(Integer, ForeignKey('person.person_id'), primary_key=True)
    office_name = Column(String)
    person = relationship(PersonStore)

class AllocationsStore(Base):
    """ class to create allocations table """
    __tablename__ = 'allocations'
    status_id = Column(Integer, primary_key=True)
    person_id = Column(Integer, ForeignKey('person.person_id'))
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    person_role = Column(String(50), nullable=False)
    accomodation = Column(String)
    room_name = Column(String)
    room_type = Column(String)

class UnallocatedStore(Base):
    """ class to create unallocated table """
    __tablename__ = 'unallocated'
    status_id = Column(Integer, primary_key=True)
    person_id = Column(Integer, ForeignKey('person.person_id'))
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    person_role = Column(String(50), nullable=False)
    accomodation = Column(String)
    room_type = Column(String(50), nullable=False)
