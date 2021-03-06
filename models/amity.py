"""
This file contains all the methods in the amity application which are contained in class Amity


"""
import os.path
import random
import re
from termcolor import colored

# imports DB
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from models.person import Fellow, Staff
from models.room import Office, LivingSpace
from models.db.sqlalchemy_declarative import (Base, PersonStore, FellowStore, StaffStore, RoomStore,
                                              OfficeStore, LSpaceStore, AllocationsStore,
                                              UnallocatedStore)


class Amity:
    """ This class holds all the methods for amity """

    def __init__(self):
        # lists of objects
        self.office = []
        self.lspace = []
        self.fellows = []
        self.staff = []
        self.unallocated_office = []
        self.unallocated_lspace = []

    def create_room(self, roomtype, roomname):
        """ method that creates room"""
        # combines office and living space lists
        all_rooms = self.office + self.lspace
        returnmsg = ''
        # lists to append output
        names_exist = ["The following rooms exist:"]
        names_created = ["The following offices were created successfully:"]
        error = ["The following rooms could not be created due to length:"]

        # checks if roomtype is office
        if roomtype.upper() == "OFFICE":
            for name in roomname:

                # checks if the roomnames given already exist
                if any(offices.room_name.title() == name.title() for offices in all_rooms):
                    names_exist.append(name.title())

                # checks for length of name if it's too long
                if len(name) > 35:
                    error.append(name)
                    returnmsg += colored(' '.join(error), "red")

                # checks if name is normal length
                if len(name) < 35:
                    self.office.append(Office(name.title()))
                    names_created.append(name.title())

                # if all names given exist, an error message is given
                if len(names_exist) > 1 and len(names_created) == 1:
                    returnmsg = colored(' '.join(names_exist), "yellow")

                # if some of the names given exist, an error is given.
                # the other names are added
                elif len(names_exist) > 1 and len(names_created) > 1:
                    returnmsg = (colored(' '.join(names_exist), "yellow"),
                                 colored(' '.join(names_created), "green"))
                elif len(names_exist) == 1 and len(names_created) > 1:
                    # if all names do not exist, they are added
                    returnmsg = colored(' '.join(names_created), "green")

         # checks if roomtype is office
        elif roomtype.upper() == "LIVING":

            # list to append output of created rooms
            names_created = [
                "The following living spaces were created successfully:"]

            # iterates through rooms given
            for name in roomname:

                 # checks if the roomnames given already exist
                if any(spaces.room_name.title() == name.title() for spaces in all_rooms):
                    names_exist.append(name.title())

                # checks for length of name if it's too long
                if len(name) > 35:
                    error.append(name)
                    returnmsg += colored(' '.join(error), "red")
                 # checks if name is normal length
                if len(name) < 35:
                    self.lspace.append(LivingSpace(name.title()))
                    names_created.append(name.title())

                # if all names given exist, an error message is given
                if len(names_exist) > 1 and len(names_created) == 1:
                    returnmsg = colored(' '.join(names_exist), "yellow")

                # if some of the names given exist, an error is given.
                # the other names are added
                elif len(names_exist) > 1 and len(names_created) > 1:
                    returnmsg = (colored(' '.join(names_exist), "yellow"),
                                 colored(' '.join(names_created), "green"))
                elif len(names_exist) == 1 and len(names_created) > 1:
                    # if all names do not exist, they are added
                    returnmsg = colored(' '.join(names_created), "green")

        else:
            # if input format is wrong, an error is given
            returnmsg += colored("Room not created!! check your input format and try again"
                                 "\n Usage: create_room <roomtype> <roomname>...", "red")

        return returnmsg

    def add_person(self, firstname, lastname, role, accomodation="N"):
        """ adds a person """
        # combines firstname and last name in name variable
        name = firstname.title() + " " + lastname.title()

        # combines fellow and staff lists
        person = self.fellows + self.staff
        returnmsg = ''
        allocateoffice = ''
        allocateliving = ''
        allocate = ''

        # checks if role is fellow
        if role.upper() == "FELLOW":

            # checks if fellow already exists
            if any(fellow.name == name for fellow in person):
                returnmsg = colored(name + " already exists!!!", "yellow")
            else:
                # if fellow doesn't exist, create the fellow object
                newfellow = Fellow(firstname.title(),
                                   lastname.title(), role, accomodation)
                fname = newfellow.name

                # autogenerate an id for the fellow
                newfellow.person_id = id(newfellow.name)
                # append fellow to the list of fellows
                self.fellows.append(newfellow)
                # returns successful message if fellow is added
                returnmsg = colored(("Fellow {} Added Successfully with ID {}"
                                     .format(newfellow.name, newfellow.person_id)), "green")
                # function called that allocates fellow office
                allocateoffice = colored(
                    self.allocate_fellow_office(newfellow, fname), "green")
                # function called that allocates fellow living space
                allocateliving = colored(self.allocate_fellow_livingspace
                                         (newfellow, fname, accomodation), "green")
            # if fellow could not be allocated room, return only the
            # status that he/she has been added
            if (allocateoffice and allocateliving) == '':
                return "{}".format(returnmsg)
            else:
                # if fellow was able to be allocated room, return both statuses
                return "{}\n{}\n{}\n".format(returnmsg, allocateoffice, allocateliving)

        elif role.upper() == "STAFF":
            # check if staff exists
            if any(staff.name == name for staff in person):
                returnmsg = colored(name + " already exists!!", "yellow")
            else:
                # create a staff object
                newstaff = Staff(firstname.title(), lastname.title(), role)
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
        """ method to allocate a fellow an office """
        # check if offices exist
        if not self.office:
            # gives error message if there are no offices
            returnmsg = colored(
                'No offices available to select from!!', "yellow")
            # appends person to list of unallocated people
            self.unallocated_office.append(newfellow)
        else:
            # randomly selects an office
            selectoffice = random.choice(self.office)
            roomname = selectoffice.room_name
            people = selectoffice.allocations
            # gets the maximum capacity property of room
            maxcapacity = selectoffice.max_capacity
            # checks if room is in office list
            if any(office.room_name == roomname for office in self.office):
                # check if office is less than maximum capacity
                if len(people) < maxcapacity:
                    newfellow.office = roomname
                    # allocates fellow to allocations
                    selectoffice.allocations.append(newfellow)
                    returnmsg = colored(
                        "Fellow " + fname + " assigned office " + roomname, "green")
                else:
                    # allocates fellow to list of persons not allocated an
                    # office
                    self.unallocated_office.append(newfellow)
                    returnmsg = colored(
                        "Fellow not assigned office!!", "yellow")

        return returnmsg

    def allocate_staff_office(self, newstaff, fname, accomodation):
        """ method to allocate staff an office """
        returnmsg = []
        # checks if offices exist
        if not self.office:
             # gives error message if there are no offices
            returnmsg.append(
                colored('No offices available to select from!!\n', 'yellow'))
            # appends person to list of unallocated people
            self.unallocated_office.append(newstaff)

        elif self.office:
            # randomly selects an office
            selectoffice = random.choice(self.office)
            roomname = selectoffice.room_name
            people = selectoffice.allocations
            # gets the maximum capacity property of room
            maxcapacity = selectoffice.max_capacity
            # checks if room is in office list
            if any(office.room_name == roomname for office in self.office):
                # check if office is less than maximum capacity
                if len(people) < maxcapacity:
                    newstaff.office = roomname
                    # appends staff to room allocations list
                    selectoffice.allocations.append(newstaff)
                    returnmsg.append(colored("Staff " + fname +
                                             " assigned office " + roomname + "\n", "green"))
                else:
                    # allocates staff to list of persons not allocated an
                    # office
                    self.unallocated_office.append(newstaff)
                    returnmsg.append(
                        colored("Staff not assigned office!!\n", "yellow"))
        # if attempt is made to give staff accomodation, returns an error
        if accomodation.upper() == "Y":
            returnmsg.append(
                colored("Staff cannot be assigned accomodation!!!", "yellow"))

        return ''.join(returnmsg)

    def allocate_fellow_livingspace(self, newfellow, fname, accomodation):
        """ method to allocate fellow a living space """
        returnmsg = ''
        # checks if fellow wants accomodation
        if accomodation.upper() == "Y":
            # checks if living spaces exist
            if not self.lspace:
                # gives error message if there are no living spaces
                returnmsg = colored(
                    'no living spaces to select from!!', 'yellow')
                # appends person to list of unallocated people
                self.unallocated_lspace.append(newfellow)
            else:
                # randomly selects an living space
                selectspace = random.choice(self.lspace)
                spacename = selectspace.room_name
                lspeople = selectspace.allocations
                # gets the maximum capacity property of room
                lsmaxcapacity = selectspace.max_capacity
                # checks if room is in living space list
                if any(space.room_name == spacename for space in self.lspace):
                    if len(lspeople) < lsmaxcapacity:
                        # check if living space is less than maximum capacity
                        newfellow.living = spacename
                        # allocates fellow to room occupants list
                        selectspace.allocations.append(newfellow)
                        returnmsg = colored("Fellow " + fname +
                                            " assigned living space " + spacename, "green")
                    else:
                        self.unallocated_lspace.append(newfellow)
                        returnmsg = colored(
                            "Fellow not assigned living space!!", "yellow")

        return returnmsg

    def load_people(self, filename):
        """ method to load people from a file """
        return_three = []
        return_four = []
        # path to script folder
        scriptpath = os.path.dirname(__file__)
        # path to the file
        filetitle = os.path.join(
            scriptpath, "../textfiles/" + filename + ".txt")
        try:
            # opens file
            with open(filetitle, 'r') as fileopen:
                # retrieves each line from file
                for line in fileopen:
                    # splits the line into individual words
                    splitwords = line.split()
                    if len(splitwords) < 4:
                        # if accomodation option was not given
                        accomodate = ' '
                        return_three.append(self.add_person(splitwords[0], splitwords[1],
                                                            splitwords[2], accomodate))
                    # if accomodation option has been given
                    elif len(splitwords) == 4:
                        accomodate = splitwords[3]
                        return_four.append(self.add_person(splitwords[0], splitwords[1],
                                                           splitwords[2], accomodate))
                        if 'str' in line:
                            break
        # if file is not found
        except FileNotFoundError:
            return_three.append(colored("Unable to open file! Please check if file exists" +
                                        " and if the file name is correct then try again", "red"))

        return "{}\n{}".format('\n'.join(return_three), '\n'.join(return_four))

    def print_room(self, roomname):
        """ method to print persons who have been allocated a room """
        printroom = []
        roomname = roomname.upper()
        rooms = self.office + self.lspace
        # check if room given is in rooms list
        for room in rooms:
            if roomname == room.room_name.upper():
                # appends room and its occupants to a list that will output as
                # a string
                printroom.append(" Room: {}\n".format(room.room_name.upper()))
                printroom.append("-" * 50 + "\n")
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
        # checks if no rooms are available
        if len(rooms) == 0:
            print(
                colored("No rooms available!! please create rooms and add people!!", "yellow"))
        # checks if no people are available
        elif len(people) == 0:
            print(colored("No people added!! please add people!", "yellow"))
        else:
            for room in rooms:
                # checks if there are allocations
                if len(room.allocations) > 0:
                    printroom.append("\n")
                    printroom.append(room.room_name.upper() +
                                     " - " + room.room_type + "\n")
                    printroom.append("-" * 50 + "\n")
                    # appends people allocated to that room
                    for allocate in room.allocations:
                        printroom.append("Name: {} ID: {}, "
                                         .format(allocate.name.title(), allocate.person_id))
                    printroom.append("\n")
                else:
                    printroom.append(colored("No room allocations available for {}!\n"
                                             .format(room.room_name),
                                             "red", "on_blue", attrs=['bold']))
                if len(room.allocations) > 0 and args["--o"]:
                    # checks file name given if its a string
                    if not re.match("^[A-Za-z]*$", args['--o']):
                        printerror = ("Invalid input! Please enter" +
                                      "file name in string format")
                    else:
                        # gives path to current file and appends the desired
                        # path to the text file
                        scriptpath = os.path.dirname(__file__)
                        filetitle = os.path.join(
                            scriptpath, "../textfiles/" + args["--o"] + ".txt")
                        printout = ' '.join(printroom)
                        fileopen = open(filetitle, "w+")
                        fileroom = printout + "\n"
                        fileopen.write(fileroom)
                        fileopen.close()
                        printfile = ("The list of allocations has been saved to the" +
                                     "following file: {}{}".format(args["--o"], ".txt"))
            if printfile != '':
                print(colored(printfile, "green"))
            elif printerror != '':
                print(colored(printerror, "red", "on_blue"))
            else:
                print(colored(' '.join(printroom),
                              "green", "on_blue", attrs=['bold']))

    def print_unallocated(self, args):
        """ method to print list of unallocated people """
        printout = ''
        printfile = ''
        printerror = ''
        # combines fellows and staff list
        people = self.fellows + self.staff
        # combines unallocated office and lspaces lists
        unallocated = self.unallocated_office + self.unallocated_lspace
        setoffice = set(self.unallocated_office)
        setlspace = set(self.unallocated_lspace)
        # checks if no people are available
        if len(people) == 0:
            print(colored("There are no people! please add people first using the " +
                          "add_person command!!"), "yellow")
        else:
            # lists to append those not allocated a room for output
            print_office = [
                "Here is the list of people not allocated an office space: \n"]
            print_office.append("-" * 50 + "\n")
            print_living = [
                "\nHere is the list of people not allocated a living space: \n"]
            print_living.append("-" * 50 + "\n")
            if self.unallocated_office == []:
                # checks if unallocated office list is empty, returns all were
                # allocated
                printout += colored("All persons were allocated offices!\n", "yellow")
            elif self.unallocated_office != []:
                # if unallocated list is not empty, append people to list for
                # output
                printoffice = list(set(unallocated).intersection(setoffice))
                for unallocate in printoffice:
                    print_office.append("Name: {},  ID: {}\n"
                                        .format(unallocate.name.title(), unallocate.person_id))
                printout += ' '.join(print_office)
            if self.unallocated_lspace == []:
                 # checks if unallocated lspace list is empty, returns all were
                 # allocated
                printout += colored("All persons were allocated living spaces!\n", "yellow")
            elif self.unallocated_lspace != []:
                # if unallocated list is not empty, append people to list for
                # output
                printliving = list(set(unallocated).intersection(setlspace))
                for unallocate in printliving:
                    print_living.append("Name: {},  ID: {}\n"
                                        .format(unallocate.name.title(), unallocate.person_id))
                printout += ' '.join(print_living)

            # if user gives a filename, create file and write list to it
            if args["--o"]:
                if not re.match("^[A-Za-z]*$", args['--o']):
                    printerror = ("Invalid input! Please enter" +
                                  " file name in string format")
                else:
                    # gets path to current file
                    scriptpath = os.path.dirname(__file__)
                    # joins path to current file with that of text file
                    filetitle = os.path.join(
                        scriptpath, "../textfiles/" + args["--o"] + ".txt")
                    fileopen = open(filetitle, "w+")
                    fileroom = printout
                    fileopen.write(fileroom)
                    fileopen.close()
                    printfile = ("The list of unallocated persons has been saved to the" +
                                 "following file: {}{}".format(args["--o"], ".txt"))
            # prints the output
            if printfile != '':
                print(colored(printfile, "green"))
            elif printerror != '':
                print(colored(printerror, "red"))
            elif len(print_office) == 2 and len(print_living) > 2:
                print(colored(''.join(print_living),
                              "green", "on_blue", attrs=['bold']))
            elif len(print_living) == 2 and len(print_office) > 2:
                print(colored(''.join(print_office),
                              "green", "on_blue", attrs=['bold']))
            else:
                print(colored(printout, "green", "on_blue", attrs=['bold']))

    def reallocate_person(self, person_identifier, new_room_name):
        """ method to reallocate person to a new room """
        # combines fellows and staff list
        persons = self.fellows + self.staff
        rooms = self.office + self.lspace
        returnmsg = ''
        new_room_name = new_room_name.title()

        # creates a list of person IDs
        personid = [person.person_id for person in persons]
        person_identifier = int(person_identifier)
        # check if the person exists
        if person_identifier not in personid:
            returnmsg = "The ID does not exist!! Try again"
        else:
            for person in persons:
                # where a person ID is the same as what user has given
                if person.person_id == person_identifier:
                    # stores the person object in a variable
                    person_object = person
            for room in rooms:
                # if the room name does exist
                if room.room_name.upper() == new_room_name.upper():
                    # stores the room object
                    room_object = room
                    # checks if person is already in that room
                    if person_object in room.allocations:
                        returnmsg = (colored("{} already exists in room {}"
                                             .format(person_object.name, room.room_name), "yellow"))
                    elif len(room.allocations) == room.max_capacity:
                        # if room has reached max capacity, it should not
                        # reallocate person
                        returnmsg = (colored("Cannot reallocate {} to {}!"
                                             " Room is at full capacity."
                                             "Please try another room"
                                             .format(person_object.name,
                                                     new_room_name), "yellow"))
                    # reallocate person if he is not already in that room
                    elif person_object.role == "STAFF" and room.room_type == "LivingSpace":
                        returnmsg = (colored("Staff {} cannot be assigned "
                                             "{} since it is a livingspace!"
                                             .format(person_object.name, new_room_name), "yellow"))
                    elif person_object not in room.allocations:
                        # capture the living space or office that was
                        # previously allocated
                        given_room = []
                        given_office = person_object.office
                        given_lspace = person_object.living
                        given_room.append(given_office)
                        given_room.append(given_lspace)
                        for room in rooms:
                            # check where room is the same as what was given
                            if room.room_name.title() in given_room:
                                # deletes previous allocation
                                room.allocations.remove(person_object)
                            # checks if person is in unallocated office list
                            elif given_room[0] == '' and person_object in self.unallocated_office:
                                # removes person from unallocated list
                                self.unallocated_office.remove(person_object)
                             # checks if person is in unallocated living space
                             # list
                            elif given_room[1] == '' and person_object in self.unallocated_lspace:
                                # removes person from unallocated list
                                self.unallocated_lspace.remove(person_object)

                        # appends person object to room
                        room_object.allocations.append(person_object)
                        returnmsg = (colored("{} has been reallocated"
                                             " successfully to room {}"
                                             .format(person_object.name,
                                                     room_object.room_name), "green"))

        return returnmsg

    def print_all_people(self, args):
        """ prints a list of all persons """
        # combines fellows and staff list
        persons = self.fellows + self.staff
        # checks if there are no people
        if len(persons) == 0:
            print(colored("No persons added yet!!", "yellow"))
        else:
            # if people exist, prints list of persons
            print(colored("Persons List", "green", "on_blue", attrs=['bold']))
            print(colored("-" * 50 + "\n", "green", "on_blue", attrs=['bold']))
            for person in persons:
                # prints persons ID and name
                print(colored("Name: {}, ID: {}, Office: {}"
                              .format(person.name, person.person_id, person.office),
                              "green", "on_blue", attrs=['bold']))

    def delete_person(self, personid):
        """ Deletes a person from the system """
        # combine lists
        people = self.fellows + self.staff
        rooms = self.office + self.lspace
        returnmsg = []
        # saves people IDs in a list
        personal_id = [person.person_id for person in people]
        personid = int(personid)
        # if person Id does not exist, return an error msg
        if personid not in personal_id:
            returnmsg.append(colored("Person ID does not exist!!", "yellow"))
        else:
            for person in people:
                # check where person ID matches that given and person role is
                # fellow
                if person.person_id == personid and person.role.upper() == "FELLOW":
                    person_object = person
                    # removes person from fellow list
                    self.fellows.remove(person_object)
                    returnmsg.append(colored("{} deleted successfully"
                                             .format(person_object.name), "green"))
                    for room in rooms:
                        # checks where the office name matches that given to
                        # fellow
                        if person_object.office.title() == room.room_name.title():
                            # removes fellow from room allocations
                            room.allocations.remove(person_object)
                            returnmsg.append(colored("{} removed from office {}"
                                                     .format(person_object.name,
                                                             room.room_name), "green"))
                        # checks where living space name matches that given to
                        # fellow
                        elif person_object.living.title() == room.room_name.title():
                            # removes the fellow from that room's list of
                            # occupants
                            room.allocations.remove(person_object)
                            returnmsg.append(colored("{} removed from living space {}"
                                                     .format(person_object.name,
                                                             room.room_name), "green"))
                        # if fellow is in list of those unallocated offices
                        # they are removed
                        for unallocate in self.unallocated_office:
                            if unallocate.person_id == personid and unallocate.office == '':
                                self.unallocated_office.remove(person)
                                returnmsg.append(colored("{} removed from office"
                                                         "unallocated list"
                                                         .format(person_object.name), "green"))

                        # if fellow is in list of those unallocated living spaces
                        # they are removed
                        for unallocate in self.unallocated_lspace:
                            if unallocate.person_id == personid and unallocate.living == '':
                                self.unallocated_lspace.remove(person_object)
                                returnmsg.append(colored("{} removed from living"
                                                         "space unallocated list"
                                                         .format(person_object.name), "green"))
                # checks if ID matches what is given and if role is staff
                elif person.person_id == personid and person.role.upper() == "STAFF":
                    person_object = person
                    # removes person from staff list
                    self.staff.remove(person_object)
                    returnmsg.append(colored("{} deleted successfully"
                                             .format(person.name), "green"))
                    for room in rooms:
                        # removes person from room allocations
                        if person_object.office.title() == room.room_name.title():
                            room.allocations.remove(person_object)
                        for unallocate in self.unallocated_office:
                            # removes person from list of those unallocated
                            # office
                            if unallocate.person_id == personid and unallocate.office == '':
                                self.unallocated_office.remove(person_object)
                                returnmsg.append(colored("{} deleted successfully"
                                                         .format(person_object.name), "green"))

        return '\n'.join(returnmsg)

    def print_all_rooms(self, args):
        """ prints a list of all rooms """
        # combines office and living space list
        rooms = self.office + self.lspace
        # check if there are no rooms, return error msg if true
        if len(rooms) == 0:
            print(colored("No rooms created yet!!", "yellow"))
        else:
            # if rooms are available, print rooms list
            print(colored("Rooms List", "green", "on_blue", attrs=['bold']))
            print(colored("-" * 50 + "\n", "green", "on_blue", attrs=['bold']))
            for room in rooms:
                print(colored("Name: {}, ID: {}".format(room.room_name, room.room_id),
                              "green", "on_blue", attrs=['bold']))

    def delete_room(self, roomid):
        """ deletes a room from the system """
        rooms = self.office + self.lspace
        returnmsg = []
        rooms_id = [room.room_id for room in rooms]
        roomid = int(roomid)
        if roomid not in rooms_id:
            returnmsg.append(colored("Room ID does not exist!!", "yellow"))
        else:
            for room in rooms:
                if room.room_id == roomid and room.room_type.upper() == "OFFICE":
                    self.unallocated_office.extend(room.allocations)
                    self.office.remove(room)
                    returnmsg.append(colored("removed {} from list of offices"
                                             .format(room.room_name), "green"))
                elif room.room_id == roomid and room.room_type.upper() == "LIVINGSPACE":
                    self.unallocated_lspace.extend(room.allocations)
                    self.lspace.remove(room)
                    returnmsg.append(colored("removed {} from list of living spaces"
                                             .format(room.room_name), "green"))
        return ''.join(returnmsg)

    def save_state(self, args):
        """ method to save data to the database """
        # checks for database given
        if args["--db"]:
            # checks if database name is a valid string
            if not re.match("^[A-Za-z]*$", args["--db"]):
                print(colored("Invalid input! Please enter the" +
                              "database name in string format", "red"))
            else:
                # creates the db engine
                engine = create_engine(
                    'sqlite:///models/db/' + args["--db"] + '.db')
                Base.metadata.create_all(engine)
                session = Session(bind=engine)
                rooms = self.office + self.lspace
                persons = self.fellows + self.staff

                # populates data for rooms in the  db
                for room in rooms:
                    session.add(RoomStore(room_id=room.room_id, room_name=room.room_name,
                                          room_type=room.room_type))
                # populates data for room allocations in the db
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

                # populates data for persons in the db
                for person in persons:
                    session.add(PersonStore(person_id=person.person_id, first_name=person.firstname,
                                            last_name=person.lastname, role=person.role,
                                            accomodation=person.accomodation))

                    if person.role == "FELLOW":
                        # populates data for fellows in the db
                        session.add(FellowStore(person_id=person.person_id,
                                                office_name=person.office,
                                                accomodation=person.accomodation))

                    elif person.role == "STAFF":
                        # populates data for staff in the db
                        session.add(StaffStore(person_id=person.person_id,
                                               office_name=person.office))

                for unallocate in self.unallocated_lspace:
                    # populates data for those unallocated living space to db
                    roomtype = "LivingSpace"
                    session.add(UnallocatedStore(person_id=unallocate.person_id,
                                                 first_name=unallocate.firstname,
                                                 last_name=unallocate.lastname,
                                                 person_role=unallocate.role,
                                                 accomodation=unallocate.accomodation,
                                                 room_type=roomtype))

                for unallocate in self.unallocated_office:
                    # populates data for those unallocated offices to db
                    roomtype = "Office"
                    session.add(UnallocatedStore(person_id=unallocate.person_id,
                                                 first_name=unallocate.firstname,
                                                 last_name=unallocate.lastname,
                                                 person_role=unallocate.role,
                                                 accomodation=unallocate.accomodation,
                                                 room_type=roomtype))

                # commits data to db
                session.commit()
                # ends db session
                session.close()
                returnmsg = (colored("Data stored successfully in database"
                                     " with the name: {}".format(args["--db"]), "green"))
        else:
            returnmsg = (colored("Please give the DB name!"
                                 "\n Usage: save_state --db=db_name", "red"))

        return returnmsg

    def load_state(self, database):
        """ method to load data from the database """
        # checks path to database
        roomlist = self.office + self.lspace
        unallocations = self.unallocated_lspace + self.unallocated_office
        file_exists = os.path.isfile('models/db/' + database + '.db')
        if file_exists is False:
            # gives error if file does not exist
            returnmsg = colored(
                "Could not find {}, it does not exist! ".format(database), "red")
        else:
            # combines fellows and staff list
            persons = self.fellows + self.staff
            # creates db engine
            engine = create_engine('sqlite:///models/db/' + database + '.db')
            Base.metadata.bind = engine
            session = Session(bind=engine)

            # retrieves room data from room table
            roomstore = session.query(RoomStore.room_id,
                                      RoomStore.room_name, RoomStore.room_type).all()

            # creates office object and appends to office list
            for rooms in roomstore:
                if rooms.room_type == "Office":
                    roomid = [room.room_id for room in self.office]
                    if rooms.room_id not in roomid:
                        office = Office(rooms.room_name)
                        office.room_id = rooms.room_id
                        self.office.append(office)

                # creates living space object and appends to living space list
                elif rooms.room_type == "LivingSpace":
                    roomid = [room.room_id for room in self.lspace]
                    if rooms.room_id not in roomid:
                        lspace = LivingSpace(rooms.room_name)
                        lspace.room_id = rooms.room_id
                        self.lspace.append(lspace)

            roomslist = self.office + self.lspace

            # retrieves person data from person table
            personstore = session.query(PersonStore.first_name, PersonStore.last_name,
                                        PersonStore.person_id, PersonStore.role,
                                        PersonStore.accomodation).all()

            # creates fellow object and appends to fellow list
            for persons in personstore:
                if persons.role == "FELLOW":
                    personid = [person.person_id for person in self.fellows]
                    if persons.person_id not in personid:
                        fellow = Fellow(persons.first_name, persons.last_name,
                                        persons.role, persons.accomodation)
                        fellow.person_id = persons.person_id
                        self.fellows.append(fellow)

                # creates person object and appends to person list
                elif persons.role == "STAFF":
                    personid = [person.person_id for person in self.fellows]
                    if persons.person_id not in personid:
                        staff = Staff(persons.first_name,
                                      persons.last_name, persons.role)
                        staff.person_id = persons.person_id
                        self.staff.append(staff)

            # retrieves allocations data from allocations table
            allocationsstore = session.query(AllocationsStore.person_id,
                                             AllocationsStore.first_name,
                                             AllocationsStore.last_name,
                                             AllocationsStore.person_role,
                                             AllocationsStore.accomodation,
                                             AllocationsStore.room_name,
                                             AllocationsStore.room_type).all()

            for allocate in allocationsstore:
                # appends fellow object to room allocations list
                if allocate.person_role == "FELLOW":
                    people_id = [people.person_id for people in self.fellows]
                    if allocate.person_id not in people_id:
                        fellow_allocated = Fellow(allocate.first_name, allocate.last_name,
                                                  allocate.person_role, allocate.accomodation)
                        fellow_allocated.person_id = allocate.person_id
                        for room in roomslist:
                            if room.room_name == allocate.room_name:
                                room.allocations.append(fellow_allocated)

                # appends staff object to room allocations list
                elif allocate.person_role == "STAFF":
                    people_id = [people.person_id for people in self.staff]
                    if allocate.person_id not in people_id:
                        staff_allocated = Staff(allocate.first_name, allocate.last_name,
                                                allocate.person_role)
                        staff_allocated.person_id = allocate.person_id
                        for room in roomslist:
                            if room.room_name == allocate.room_name:
                                room.allocations.append(staff_allocated)

            # retrieves unallocated persons data from unallocated table
            unallocatedstore = session.query(UnallocatedStore.person_id,
                                             UnallocatedStore.first_name,
                                             UnallocatedStore.last_name,
                                             UnallocatedStore.person_role,
                                             UnallocatedStore.accomodation,
                                             UnallocatedStore.room_type).all()

            for unallocated in unallocatedstore:
                if unallocated.person_role == "FELLOW":
                    people_id = [people.person_id for people in unallocations]
                    if unallocated.person_id not in people_id:
                        fellow_unallocated = Fellow(unallocated.first_name, unallocated.last_name,
                                                    unallocated.person_role,
                                                    unallocated.accomodation)
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
            dbname = os.path.join(dbpath, 'db/' + database + '.db')
            os.remove(dbname)
            session.close()
            returnmsg = (colored("Data loaded successfully from database" +
                                 " with the name: {}".format(database), "green"))

        return returnmsg
