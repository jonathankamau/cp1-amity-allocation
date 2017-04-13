import os.path
import random

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from models.person import Person, Fellow, Staff
from models.room import Room, Office, LivingSpace
from models.db.sqlalchemy_declarative import (Base, PersonStore, FellowStore, StaffStore, RoomStore,
                                              OfficeStore, LSpaceStore, AllocationsStore,
                                              UnallocatedStore)

class Amity:
    def __init__(self):
        self.office = []
        self.lspace = []
        self.fellows = []
        self.staff = []
        self.loadpeople = "persons.txt"
        self.unallocated_office = []
        self.unallocated_lspace = []

    def create_room(self, roomtype, roomname):
        """ method that creates room"""
        if roomtype.upper() == "OFFICE":
            all_rooms = self.office + self.lspace
            names_exist = ["The following offices exist:"]
            names_created = ["The following offices were created successfully:"]
            for name in roomname:
                if  any(offices.room_name == name for offices in all_rooms):
                    names_exist.append(name)
                else:
                    self.office.append(Office(name))
                    names_created.append(name)
            if len(names_exist) > 1 and len(names_created) == 1:
                returnmsg = ' '.join(names_exist)
            elif len(names_exist) > 1 and len(names_created) > 1:
                returnmsg = ' '.join(names_exist), ' '.join(names_created)
            else:
                returnmsg = ' '.join(names_created)

            return returnmsg
        elif roomtype.upper() == "LIVING":
            all_rooms = self.office + self.lspace
            names_exist = ["The following living spaces exist:"]
            names_created = ["The following living spaces were created successfully:"]
            for name in roomname:
                if  any(spaces.room_name == name for spaces in self.lspace):
                    names_exist.append(name)
                else:
                    self.lspace.append(LivingSpace(name))
                    names_created.append(name)
            if len(names_exist) > 1 and len(names_created) == 1:
                returnmsg = ' '.join(names_exist)
            elif len(names_exist) > 1 and len(names_created) > 1:
                returnmsg = ' '.join(names_exist), ' '.join(names_created)
            else:
                returnmsg = ' '.join(names_created)

            return returnmsg

        else:
            return "Room not created!! check your input format and try again"

    def add_person(self, firstname, lastname, role, accomodation="N"):
        """ adds a person """
        name = firstname+" "+lastname
        person = self.fellows + self.staff
        returnmsg = ''
        if role.upper() == "FELLOW":
            if any(fellow.name == name for fellow in person):
                returnmsg = name + " already exists!!!"
            else:
                newfellow = Fellow(firstname, lastname, role, accomodation)
                fname = newfellow.name
                self.fellows.append(newfellow)
                returnmsg = "Fellow "+fname+" Added Successfully"
                #return result
                allocateoffice = self.allocate_fellow_office(newfellow, fname)

                allocateliving = self.allocate_fellow_livingspace(newfellow, fname, accomodation)

            return "{}\n{}\n{}".format(returnmsg, allocateoffice, allocateliving)

        elif role.upper() == "STAFF":
            if any(staff.name == name for staff in person):
                returnmsg = name+ " already exists!!"
            else:
                newstaff = Staff(firstname, lastname, role)
                fname = newstaff.name
                self.fellows.append(newstaff)
                returnmsg = "Staff "+fname+" Added Successfully"
                allocate = self.allocate_staff_office(newstaff, fname, accomodation)

            return "{}\n{}".format(returnmsg, allocate)

    def allocate_fellow_office(self, newfellow, fname):
        if not self.office:
            returnmsg = 'No offices available to select from!!'
        else:
            selectoffice = random.choice(self.office)
            roomname = selectoffice.room_name
            people = selectoffice.allocations
            maxcapacity = selectoffice.max_capacity
            if any(office.room_name == roomname for office in self.office):
                if len(people) < maxcapacity:
                    selectoffice.allocations.append(newfellow)
                    returnmsg = "Fellow "+fname+" assigned office "+roomname
                else:
                    self.unallocated_office.append(newfellow)
                    returnmsg = "Fellow not assigned office!!"

            return returnmsg

    def allocate_staff_office(self, newstaff, fname, accomodation):
        if not self.office:
            returnmsg = 'No offices available to select from!!'
        else:
            selectoffice = random.choice(self.office)
            roomname = selectoffice.room_name
            people = selectoffice.allocations
            maxcapacity = selectoffice.max_capacity
            if any(office.room_name == roomname for office in self.office):
                if len(people) < maxcapacity:
                    selectoffice.allocations.append(newstaff)
                    returnmsg = "Staff "+fname+" assigned office "+roomname
                else:
                    self.unallocated_office.append(newstaff)
                    returnmsg = "Staff not assigned office!!"
        if accomodation == "Y":
            returnmsg = "staff cannot be assigned accomodation!!!"

        return returnmsg

    def allocate_fellow_livingspace(self, newfellow, fname, accomodation):
        if accomodation == "Y":
            if not self.lspace:
                return 'no living spaces to select from!!'
            else:
                selectspace = random.choice(self.lspace)
                spacename = selectspace.room_name
                lspeople = selectspace.allocations
                lsmaxcapacity = selectspace.max_capacity
                if any(space.room_name == spacename for space in self.lspace):
                    if len(lspeople) < lsmaxcapacity:
                        selectspace.allocations.append(newfellow)
                        return "Fellow "+fname+" assigned living space "+spacename
                    else:
                        self.unallocated_lspace.append(newfellow)
                        return "Fellow not assigned living space!!"

    def load_people(self, filename):
        """ method to load people from a file """
        return_three = []
        return_four = []
        scriptpath = os.path.dirname(__file__)
        filetitle = os.path.join(scriptpath, "../textfiles/"+filename+".txt")
        try:
            with open(filetitle, 'r') as fileopen:
                for line in fileopen:
                    splitwords = line.split()
                    if len(splitwords) < 4:
                        accomodate = ' '
                        return_three.append(self.add_person(splitwords[0], splitwords[1],
                                                            splitwords[2], accomodate))
                    elif len(splitwords) == 4:
                        accomodate = splitwords[3]
                        return_four.append(self.add_person(splitwords[0], splitwords[1],
                                                           splitwords[2], accomodate))
                        if 'str' in line:
                            break
        except FileNotFoundError:
            return_three.append("Unable to open file! Please check if file exists"+
                                " and if the file name is correct then try again")

        return "{}\n{}".format('\n'.join(return_three), '\n'.join(return_four))

    def print_room(self, roomname):
        """ method to print persons who have been allocated a room """
        rooms = self.office + self.lspace
        for room in rooms:
            if roomname == room.room_name:
                returnmsg = room.room_name
                for allocate in room.allocations:
                    message = allocate.name

        return "{}\n{}".format(returnmsg, message)

    def print_allocations(self, printfile):
        """ method to print list of allocations """
        rooms = self.office + self.lspace
        for room in rooms:
            if len(room.allocations) > 1 and printfile is None:
                print(room.room_name)
                for allocate in room.allocations:
                    print(allocate.name)
            elif len(room.allocations) > 1 and printfile != None:
                scriptpath = os.path.dirname(__file__)
                filetitle = os.path.join(scriptpath, printfile+".txt")
                fileopen = open(filetitle, "w+")
                fileroom = room.room_name+"\n"
                fileopen.write(fileroom)
                for allocate in room.allocations:
                    filepeople = allocate.name
                    fileopen.write(filepeople)
                    fileopen.close()

    def print_unallocated(self, filename):
        """ method to print list of unallocated people """
        for unallocated in self.unallocated_office:
            scriptpath = os.path.dirname(__file__)
            filetitle = os.path.join(scriptpath, filename+".txt")
            fileopen = open(filetitle, "w+")
            fileroom = "People Unallocated Office Space\n"+unallocated.room_name+"\n"
            fileopen.write(fileroom)
            for unallocate in self.unallocated_office:
                fileoffice = unallocate.name
                fileopen.write(fileoffice)
            fileopen.close()

    def search_for_id(self, name):
        pass
    def search_for_room(self, name):
        pass

    def reallocate_person(self, person_identifier, new_room_name):
        """ method to reallocate person to a new room """
        people = self.fellows + self.staff
        rooms = self.office + self.lspace
        #if any(person.name == person_identifier for person in people):
        if person_identifier not in [person.name for person in people]:
            returnmsg = "The name or ID does not exist!! Try again"
        else:
            for person, room, allocate in zip(people, rooms, room.allocations):
                if person.name == person_identifier and allocate == person:
                    room.allocations.remove(person)
                if (room.room_name == new_room_name and
                        len(room.allocations) < room.max_capacity):
                    room.allocations.append(person)
                    returnmsg = "{} has been reallocated successfully".format(person.name)

                else:
                    returnmsg = "Could not reallocate {} to room {}!".format(person.name, new_room_name)

        return returnmsg

    def reallocated_person(self, person_identifier, new_room_name):
        """ method to reallocate person to a new room """
        people = self.fellows + self.staff
        rooms = self.office + self.lspace
        for person in people:
            if person.name == person_identifier:
                for room in rooms:
                    for allocate in room.allocations:
                        if allocate == person:
                            room.allocations.remove(person)
                    if (room.room_name == new_room_name and
                            len(room.allocations) < room.max_capacity):
                        room.allocations.append(person)
                        returnmsg = "{} has been reallocated successfully".format(person.name)
                    else:
                        returnmsg = "Could not reallocate {} to room {}!".format(person.name, new_room_name)
            else:
                returnmsg = "The name or ID does not exist!! Try again"


        return returnmsg

    def save_state(self, database):
        """ method to save data to the database """
        engine = create_engine('sqlite:///models/db/'+database+'.db')
        Base.metadata.create_all(engine)
        session = Session(bind=engine)
        rooms = self.office + self.lspace
        persons = self.fellows + self.staff

        for room in rooms:
            session.add(RoomStore(room_id=room.room_id, room_name=room.room_name,
                                  room_type=room.room_type))

        for person in persons:
            session.add(PersonStore(person_id=person.person_id, first_name=person.firstname,
                                    last_name=person.lastname, role=person.role,
                                    accomodation=person.accomodation))

        session.commit()

    def load_state(self, database):
        """ method to load data from the database """
        engine = create_engine('sqlite:///models/db/'+database+'.db')
        Base.metadata.bind = engine
        session = Session(bind=engine)

        roomstore = session.query(RoomStore.room_id, RoomStore.room_name, RoomStore.room_type).all()

        for rooms in roomstore:
            if rooms.room_type == "Office":
                office = Office(rooms.room_name)
                self.office.append(office)

            elif rooms.room_type == "LivingSpace":
                lspace = LivingSpace(rooms.room_name)
                self.lspace.append(lspace)

        personstore = session.query(PersonStore.first_name, PersonStore.last_name,
                                    PersonStore.person_id, PersonStore.role,
                                    PersonStore.accomodation).all()

        for persons in personstore:
            if persons.role == "FELLOW":
                fellow = Fellow(persons.first_name, persons.last_name,
                                persons.role, persons.accomodation)
                self.fellows.append(fellow)

            elif persons.role == "STAFF":
                staff = Staff(persons.first_name, persons.last_name, persons.role)
                self.staff.append(staff)

