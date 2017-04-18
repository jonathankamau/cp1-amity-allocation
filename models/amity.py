"""
This file contains all the methods in the amity application which are contained in class Amity

"""
import os.path
import random
import re
from termcolor import colored

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from models.person import Person, Fellow, Staff
from models.room import Room, Office, LivingSpace
from models.db.sqlalchemy_declarative import (Base, PersonStore, FellowStore, StaffStore, RoomStore,
                                              OfficeStore, LSpaceStore, AllocationsStore,
                                              UnallocatedStore)

class Amity:
    """ This class holds all the methods for amity """
    def __init__(self):
        self.office = []
        self.lspace = []
        self.fellows = []
        self.staff = []
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
                returnmsg = colored(' '.join(names_exist), "red")
            elif len(names_exist) > 1 and len(names_created) > 1:
                returnmsg = (colored(' '.join(names_exist), "red"),
                             colored(' '.join(names_created), "green"))
            else:
                returnmsg = colored(' '.join(names_created), "green")

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
                returnmsg = colored(' '.join(names_exist), "red")
            elif len(names_exist) > 1 and len(names_created) > 1:
                returnmsg = (colored(' '.join(names_exist), "red"),
                             colored(' '.join(names_created), "green"))
            else:
                returnmsg = colored(' '.join(names_created), "green")

            return returnmsg

        else:
            return colored("Room not created!! check your input format and try again"
                           "\n Usage: create_room <roomtype> <roomname>...", "red")

    def add_person(self, firstname, lastname, role, accomodation="N"):
        """ adds a person """
        name = firstname+" "+lastname
        person = self.fellows + self.staff
        returnmsg = ''
        allocateoffice = ''
        allocateliving = ''
        allocate = ''
        if role.upper() == "FELLOW":
            if any(fellow.name == name for fellow in person):
                returnmsg = colored(name + " already exists!!!", "red")
            else:
                newfellow = Fellow(firstname, lastname, role, accomodation)
                fname = newfellow.name
                newfellow.person_id = id(newfellow.name)
                self.fellows.append(newfellow)
                returnmsg = colored(("Fellow {} Added Successfully with ID {}"
                                     .format(newfellow.name, newfellow.person_id)), "green")
                allocateoffice = colored(self.allocate_fellow_office(newfellow, fname), "green")
                allocateliving = colored(self.allocate_fellow_livingspace
                                         (newfellow, fname, accomodation), "green")

            if (allocateoffice and allocateliving) == '':
                return "{}".format(returnmsg)
            else:
                return "{}\n{}\n{}".format(returnmsg, allocateoffice, allocateliving)

        elif role.upper() == "STAFF":
            if any(staff.name == name for staff in person):
                returnmsg = colored(name+ " already exists!!", "red")
            else:
                newstaff = Staff(firstname, lastname, role)
                fname = newstaff.name
                newstaff.person_id = id(newstaff.name)
                self.staff.append(newstaff)
                returnmsg = colored(("Staff {} Added Successfully with ID {}"
                                     .format(newstaff.name, newstaff.person_id)),
                                    "green", attrs=['blink'])
                allocate = colored(self.allocate_staff_office
                                   (newstaff, fname, accomodation), "green")
            if allocate == '':
                return "{}".format(returnmsg)
            else:
                return "{}\n{}".format(returnmsg, allocate)

    def allocate_fellow_office(self, newfellow, fname):
        if not self.office:
            returnmsg = colored('No offices available to select from!!', "red")
            self.unallocated_office.append(newfellow)
        else:
            selectoffice = random.choice(self.office)
            roomname = selectoffice.room_name
            people = selectoffice.allocations
            maxcapacity = selectoffice.max_capacity
            if any(office.room_name == roomname for office in self.office):
                if len(people) < maxcapacity:
                    newfellow.office = roomname
                    selectoffice.allocations.append(newfellow)
                    returnmsg = colored("Fellow "+fname+" assigned office "+roomname, "green")
                else:
                    self.unallocated_office.append(newfellow)
                    returnmsg = colored("Fellow not assigned office!!", "red")

        return returnmsg

    def allocate_staff_office(self, newstaff, fname, accomodation):
        if not self.office:
            returnmsg = colored('No offices available to select from!!', 'red')
            self.unallocated_office.append(newstaff)
        else:
            selectoffice = random.choice(self.office)
            roomname = selectoffice.room_name
            people = selectoffice.allocations
            maxcapacity = selectoffice.max_capacity
            if any(office.room_name == roomname for office in self.office):
                if len(people) < maxcapacity:
                    newstaff.office = roomname
                    selectoffice.allocations.append(newstaff)
                    returnmsg = colored("Staff "+fname+" assigned office "+roomname, "green")
                else:
                    self.unallocated_office.append(newstaff)
                    returnmsg = colored("Staff not assigned office!!","red")
        if accomodation == "Y":
            returnmsg = colored("staff cannot be assigned accomodation!!!", "red")

        return returnmsg

    def allocate_fellow_livingspace(self, newfellow, fname, accomodation):
        returnmsg = ''
        if accomodation == "Y":
            if not self.lspace:
                returnmsg = colored('no living spaces to select from!!', 'red')
                self.unallocated_lspace.append(newfellow)
            else:
                selectspace = random.choice(self.lspace)
                spacename = selectspace.room_name
                lspeople = selectspace.allocations
                lsmaxcapacity = selectspace.max_capacity
                if any(space.room_name == spacename for space in self.lspace):
                    if len(lspeople) < lsmaxcapacity:
                        newfellow.living = spacename
                        selectspace.allocations.append(newfellow)
                        returnmsg = colored("Fellow "+fname+" assigned living space "+spacename, "green")
                    else:
                        self.unallocated_lspace.append(newfellow)
                        returnmsg = colored("Fellow not assigned living space!!", "red")

        return returnmsg

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
            return_three.append(colored("Unable to open file! Please check if file exists"+
                                        " and if the file name is correct then try again", "red"))

        return "{}\n{}".format('\n'.join(return_three), '\n'.join(return_four))

    def print_room(self, roomname):
        """ method to print persons who have been allocated a room """
        # message = ''
        # returnmsg = ''
        printroom = []
        roomname = roomname.upper()
        rooms = self.office + self.lspace
        for room in rooms:
            if roomname == room.room_name.upper():
                printroom.append(" Room: {}\n".format(room.room_name.upper()))
                printroom.append("-" *50 + "\n")
                for allocate in room.allocations:
                    printroom.append(" Name: {}, ID: {}\n"
                                     .format(allocate.name.title(), allocate.person_id))

        return colored(' '.join(printroom), "green", "on_blue", attrs=['bold'])

    def print_allocations(self, args):
        """ method to print list of allocations """
        printout = ''
        printfile = ''
        printerror = ''
        printroom = []
        rooms = self.office + self.lspace
        people = self.office + self.lspace
        if len(rooms) == 0:
            print(colored("No rooms available!! please create rooms and add people!!", "red"))
        elif len(people) == 0:
            print(colored("No people added!! please add people!", "red"))
        else:
            for room in rooms:
                if len(room.allocations) > 0:
                    printroom.append("\n")
                    printroom.append(room.room_name.upper() + " - " + room.room_type + "\n")
                    printroom.append("-" *50 + "\n")
                    for allocate in room.allocations:
                        printroom.append("Name: {} ID: {}, "
                                         .format(allocate.name.title(), allocate.person_id))
                    printroom.append("\n")
                else:
                    printroom.append(colored("No room allocations available for {}!\n"
                                             .format(room.room_name), "red"))
                if len(room.allocations) > 0 and args["--o"]:
                    if not re.match("^[A-Za-z]*$", args['--o']):
                        printerror = ("Invalid input! Please enter"+
                                      "file name in string format")
                    else:
                        scriptpath = os.path.dirname(__file__)
                        filetitle = os.path.join(scriptpath, "../textfiles/"+args["--o"]+".txt")
                        printout = ' '.join(printroom)
                        fileopen = open(filetitle, "w+")
                        fileroom = printout+"\n"
                        fileopen.write(fileroom)
                        fileopen.close()
                        printfile = ("The list of allocations has been saved to the"+
                                     "following file: {}{}".format(args["--o"], ".txt"))
            if printfile != '':
                print(colored(printfile, "green"))
            elif printerror != '':
                print(colored(printerror, "red"))
            else:
                print(colored(' '.join(printroom), "green", "on_blue", attrs=['bold']))

    def print_unallocated(self, args):
        """ method to print list of unallocated people """
        printout = ''
        printfile = ''
        printerror = ''
        people = self.fellows + self.staff
        unallocated = self.unallocated_office + self.unallocated_lspace
        setoffice = set(self.unallocated_office)
        setlspace = set(self.unallocated_lspace)
        if len(people) == 0:
            print(colored("There are no people! please add people first using the " +
                          "add_person command!!"), "red")
        else:
            print_office = ["Here is the list of people not allocated an office space: \n"]
            print_office.append("-" *50 + "\n")
            print_living = ["Here is the list of people not allocated a living space: \n"]
            print_living.append("-" *50 + "\n")
            if self.unallocated_office == []:
                printout += colored("All persons were allocated offices!\n", "red")
            elif self.unallocated_office != []:
                printoffice = list(set(unallocated).intersection(setoffice))
                for unallocate in printoffice:
                    print_office.append("Name: {},  ID: {}\n"
                                        .format(unallocate.name.title(), unallocate.person_id))
            if self.unallocated_lspace == []:
                printout += colored("All persons were allocated living spaces!\n", "red")
            elif self.unallocated_lspace != []:
                printliving = list(set(unallocated).intersection(setlspace))
                for unallocate in printliving:
                    print_living.append("Name: {},  ID: {}\n"
                                        .format(unallocate.name.title(), unallocate.person_id))

            printout += ' '.join(print_office)
            printout += ' '.join(print_living)
            if args["--o"]:
                if not re.match("^[A-Za-z]*$", args['--o']):
                    printerror = ("Invalid input! Please enter"+
                                  " file name in string format")
                else:
                    scriptpath = os.path.dirname(__file__)
                    filetitle = os.path.join(scriptpath, "../textfiles/"+args["--o"]+".txt")
                    fileopen = open(filetitle, "w+")
                    fileroom = printout
                    fileopen.write(fileroom)
                    fileopen.close()
                    printfile = ("The list of unallocated persons has been saved to the"+
                                 "following file: {}{}".format(args["--o"], ".txt"))
            if printfile != '':
                print(colored(printfile, "green"))
            elif printerror != '':
                print(colored(printerror, "red"))
            elif len(print_office) == 2 and len(print_living) > 2:
                print(colored(''.join(print_living), "green", "on_blue", attrs=['bold']))
            elif len(print_living) == 2 and len(print_office) > 2:
                print(colored(''.join(print_office), "green", "on_blue", attrs=['bold']))
            else:
                print(colored(printout, "green", "on_blue", attrs=['bold']))

    def reallocate_person(self, person_identifier, new_room_name):
        """ method to reallocate person to a new room """
        persons = self.fellows + self.staff
        rooms = self.office + self.lspace
        returnmsg = ''
        personid = [person.person_id for person in persons]
        person_identifier = int(person_identifier)
        if person_identifier not in personid:
            returnmsg = "The ID does not exist!! Try again"
        else:
            for person in persons:
                if person.person_id == person_identifier:
                    person_object = person
            for room in rooms:
                allocatedroom = [allocate.person_id for allocate in room.allocations]
                if person_object.person_id in allocatedroom:
                    if new_room_name == room.room_name:
                        returnmsg = ("{} already is in room {}"
                                     .format(person_object.name, new_room_name))
                    else:
                        room.allocations.remove(person_object)
                if room.room_name.upper() == new_room_name.upper():
                    room_object = room
                    room_object.allocations.append(person_object)
                    returnmsg = ("{} has been reallocated successfully to room {}"
                                 .format(person_object.name, room_object.room_name))
        return returnmsg

    def print_all_people(self, args):
        """ prints a list of all persons """
        persons = self.fellows + self.staff
        if len(persons) == 0:
            print(colored("No persons added yet!!", "red"))
        else:
            print(colored("Persons List", "green", "on_blue", attrs=['bold']))
            print(colored("-" *50 + "\n", "green", "on_blue", attrs=['bold']))
            for person in persons:
                print(colored("Name: {}, ID: {}, Office: {}"
                              .format(person.name, person.person_id, person.office),
                              "green", "on_blue", attrs=['bold']))

    def delete_person(self, personid):
        """ Deletes a person from the system """
        people = self.fellows + self.staff
        rooms = self.office + self.lspace
        personal_id = [person.person_id for person in people]
        unallocated = self.unallocated_office + self.unallocated_lspace
        personid = int(personid)
        if personid not in personal_id:
            returnmsg = colored("ID does not exist!!", "red")
        else:
            for person in people:
                if person.person_id == personid and person.role.upper() == "FELLOW":
                    print(person.name)
                    print(person.person_id)
                    person_object = person
                    self.fellows.remove(person)
                    returnmsg = colored("{} deleted successfully"
                                        .format(person.name), "green")
                    for room in rooms:
                        if person.office == room.room_name:
                            print(person.office)
                            print(room.room_name)
                            room.allocations.remove(person)
                            returnmsg = colored("{} removed from office {}"
                                                .format(person.name, room.room_name), "green")
                        elif person.living == room.room_name:
                            print("person living"+person.living)
                            print("Living"+room.room_name)
                            room.allocations.remove(person)
                            returnmsg = colored("{} removed from living space {}"
                                                .format(person.name, room.room_name), "green")
                        for unallocate in self.unallocated_office:
                            if unallocate.person_id == personid and unallocate.office == '':
                                print(unallocate.name)
                                self.unallocated_office.remove(person)
                                returnmsg = colored("{} removed from office unallocated list"
                                                    .format(person.name), "green")
                        for unallocate in self.unallocated_lspace:
                            if unallocate.person_id == personid and unallocate.living == '':
                                print(unallocate.name)
                                self.unallocated_lspace.remove(person)
                                returnmsg = colored("{} removed from living space unallocated list"
                                                    .format(person.name), "green")
                elif person.person_id == personid and person.role.upper() == "STAFF":
                    self.staff.remove(person)
                    for room in rooms:
                        if person.office == room.room_name:
                            room.allocations.remove(person)
                    for unallocate in unallocated:
                        if unallocate.person_id == personid and unallocate.office == '':
                            self.unallocated_office.remove(person)
                            returnmsg = colored("{} deleted successfully"
                                                .format(person.name), "green")
                else:
                    returnmsg = colored("Could not delete person!!", "red")

            return returnmsg

    def print_all_rooms(self, args):
        """ prints a list of all rooms """
        rooms = self.office + self.lspace
        if len(rooms) == 0:
            print(colored("No rooms created yet!!", "red"))
        else:
            print(colored("Rooms List", "green", "on_blue", attrs=['bold']))
            print(colored("-" *50 + "\n", "green", "on_blue", attrs=['bold']))
            for room in rooms:
                print(colored("Name: {}, ID: {}".format(room.room_id, room.room_name),
                              "green", "on_blue", attrs=['bold']))

    def save_state(self, args):
        """ method to save data to the database """
        if args["--db"]:
            if not re.match("^[A-Za-z]*$", args["--db"]):
                print(colored("Invalid input! Please enter the"+
                              "database name in string format", "red"))
            else:
                engine = create_engine('sqlite:///models/db/'+args["--db"]+'.db')
                Base.metadata.create_all(engine)
                session = Session(bind=engine)
                rooms = self.office + self.lspace
                persons = self.fellows + self.staff


                for room in rooms:
                    session.add(RoomStore(room_id=room.room_id, room_name=room.room_name,
                                          room_type=room.room_type))
                for room in rooms:
                    roomname = room.room_name
                    roomtype = room.room_type
                    for allocate in room.allocations:
                        personid = allocate.person_id

                        session.add(AllocationsStore(person_id=personid,
                                                     first_name=allocate.firstname,
                                                     last_name=allocate.lastname,
                                                     person_role=allocate.role,
                                                     accomodation=allocate.accomodation,
                                                     room_name=roomname, room_type=roomtype))

                for person in persons:
                    session.add(PersonStore(person_id=person.person_id, first_name=person.firstname,
                                            last_name=person.lastname, role=person.role,
                                            accomodation=person.accomodation))
                    if person.role == "FELLOW":
                        session.add(FellowStore(person_id=person.person_id,
                                                office_name=person.office,
                                                accomodation=person.accomodation))
                    elif person.role == "STAFF":
                        session.add(StaffStore(person_id=person.person_id,
                                               office_name=person.office))

                for unallocate in self.unallocated_lspace:
                    roomtype = "LivingSpace"
                    session.add(UnallocatedStore(person_id=unallocate.person_id,
                                                 first_name=unallocate.firstname,
                                                 last_name=unallocate.lastname,
                                                 person_role=unallocate.role,
                                                 accomodation=unallocate.accomodation,
                                                 room_type=roomtype))

                for unallocate in self.unallocated_office:
                    roomtype = "Office"
                    session.add(UnallocatedStore(person_id=unallocate.person_id,
                                                 first_name=unallocate.firstname,
                                                 last_name=unallocate.lastname,
                                                 person_role=unallocate.role,
                                                 accomodation=unallocate.accomodation,
                                                 room_type=roomtype))


                session.commit()
                session.close()
                print(colored("Data stored successfully in database"+
                              " with the name: {}".format(args["--db"]), "green"))
        else:
            print(colored("Please give the DB name!", "red"))
            print("Usage: save_state --db=db_name")

    def load_state(self, database):
        """ method to load data from the database """

        persons = self.fellows + self.staff
        engine = create_engine('sqlite:///models/db/'+database+'.db')
        Base.metadata.bind = engine
        session = Session(bind=engine)

        roomstore = session.query(RoomStore.room_id, RoomStore.room_name, RoomStore.room_type).all()

        for rooms in roomstore:
            if rooms.room_type == "Office":
                office = Office(rooms.room_name)
                office.room_id = rooms.room_id
                self.office.append(office)

            elif rooms.room_type == "LivingSpace":
                lspace = LivingSpace(rooms.room_name)
                lspace.room_id = rooms.room_id
                self.lspace.append(lspace)

        roomslist = self.office + self.lspace


        personstore = session.query(PersonStore.first_name, PersonStore.last_name,
                                    PersonStore.person_id, PersonStore.role,
                                    PersonStore.accomodation).all()

        for persons in personstore:
            if persons.role == "FELLOW":
                fellow = Fellow(persons.first_name, persons.last_name,
                                persons.role, persons.accomodation)
                fellow.person_id = persons.person_id
                self.fellows.append(fellow)

            elif persons.role == "STAFF":
                staff = Staff(persons.first_name, persons.last_name, persons.role)
                staff.person_id = persons.person_id
                self.staff.append(staff)



        allocationsstore = session.query(AllocationsStore.person_id, AllocationsStore.first_name,
                                         AllocationsStore.last_name, AllocationsStore.person_role,
                                         AllocationsStore.accomodation, AllocationsStore.room_name,
                                         AllocationsStore.room_type).all()

        for allocate in allocationsstore:
            if allocate.person_role == "FELLOW":
                fellow_allocated = Fellow(allocate.first_name, allocate.last_name,
                                          allocate.person_role, allocate.accomodation)
                fellow_allocated.person_id = allocate.person_id
                for room in roomslist:
                    if room.room_name == allocate.room_name:
                        room.allocations.append(fellow_allocated)
            elif allocate.person_role == "STAFF":
                staff_allocated = Staff(allocate.first_name, allocate.last_name,
                                        allocate.person_role)
                staff_allocated.person_id = allocate.person_id
                for room in roomslist:
                    if room.room_name == allocate.room_name:
                        room.allocations.append(staff_allocated)

        unallocatedstore = session.query(UnallocatedStore.person_id, UnallocatedStore.first_name,
                                         UnallocatedStore.last_name, UnallocatedStore.person_role,
                                         UnallocatedStore.accomodation,
                                         UnallocatedStore.room_type).all()

        for unallocated in unallocatedstore:
            if unallocated.person_role == "FELLOW":
                fellow_unallocated = Fellow(unallocated.first_name, unallocated.last_name,
                                            unallocated.person_role, unallocated.accomodation)
                fellow_unallocated.person_id = unallocated.person_id
                if unallocated.room_type == "Office":
                    self.unallocated_office.append(fellow_unallocated)
                elif unallocated.room_type == "LivingSpace":
                    self.unallocated_lspace.append(fellow_unallocated)
            elif unallocated.person_role == "STAFF":
                staff_unallocated = Staff(unallocated.first_name, unallocated.last_name,
                                          unallocated.person_role)
                staff_unallocated.person_id = unallocated.person_id
                if unallocated.room_type == "Office":
                    self.unallocated_office.append(staff_unallocated)
        dbpath = os.path.dirname(__file__)
        dbname = os.path.join(dbpath, 'db/'+database+'.db')
        os.remove(dbname)
        session.close()
        print(colored("Data loaded successfully from database"+
                      " with the name: {}".format(database), "green"))


