"""
Tests for amity
"""
import unittest
import sys
from contextlib import contextmanager
from io import StringIO


from models.room import Room, Office, LivingSpace
from models.amity import Amity
from models.person import Person, Fellow, Staff
import models.db.sqlalchemy_declarative


class AmityTest(unittest.TestCase):
    """ initializes the test class """

    def setUp(self):
        self.room = Room
        self.office = Office
        self.livingspace = LivingSpace
        self.person = Person
        self.fellow = Fellow
        self.staff = Staff
        self.amity = Amity()

    @contextmanager
    def captured_output(self):
        """
        method is used to capture the output of print() statements from other methods
        for purposes of testing with assert statements it does this by temporarily substituting
        in built stdout and stderr with instances of StringIO class
        """

        new_out, new_err = StringIO(), StringIO()
        old_out, old_err = sys.stdout, sys.stderr
        try:
            sys.stdout, sys.stderr = new_out, new_err
            yield sys.stdout, sys.stderr
        finally:
            sys.stdout, sys.stderr = old_out, old_err

    def test_living_space_inheritance(self):
        """ Tests if living space class inherits from room class """
        self.assertTrue(issubclass(LivingSpace, Room))

    def test_for_office_inheritance(self):
        """ Tests if office class inherits from room class """
        self.assertTrue(issubclass(Office, Room))

    def test_office_name_length(self):
        # sets up the required parameters
        roomname = [
            'fsdjfisjidfjsdjcksdnflksdjlfjrfeuhfdsjoksjfodsfjosdgfjdhgjfdhgkjdfkjfdfnkvjdf']
        roomtype = "Office"
        # expected return message
        returnmsg = "The following rooms could not be created due to length"
        # saves return from method to a variable
        room_create = self.amity.create_room(roomtype, roomname)
        # checks if the expected return what is actually returned by method
        self.assertIn(returnmsg, room_create,
                      msg="Office not successfully created!!")

    def test_living_space_name_length(self):
        # sets up the required parameters
        roomname = [
            'fsdjfisjidfjsdjcksdnflksdjlfjrfeuhfdsjoksjfodsfjosdgfjdhgjfdhgkjdfkjfdfnkvjdf']
        roomtype = "Living"
        # expected return message
        returnmsg = "The following rooms could not be created due to length"
        # saves return from method to a variable
        room_create = self.amity.create_room(roomtype, roomname)
        # checks if the expected return what is actually returned by method
        self.assertIn(returnmsg, room_create,
                      msg="Office not successfully created!!")

    def test_for_create_office(self):
        """ Tests if office has been created """
        # sets up the required parameters
        roomname = "Forest"
        roomtype = "Office"
        # expected return message
        returnmsg = "The following offices were created successfully"
        # saves return from method to a variable
        room_create = self.amity.create_room(roomtype, roomname)
        # checks if the expected return what is actually returned by method
        self.assertIn(returnmsg, room_create,
                      msg="Office not successfully created!!")

    def test_for_create_livingspace(self):
        """ Tests if living space has been created """
        # sets up the required parameters
        roomname = "Coast"
        roomtype = "living"
        # expected return message
        returnmsg = "The following living spaces were created successfully"
        # saves return from method to a variable
        room_create = self.amity.create_room(roomtype, roomname)
        # checks if the expected return what is actually returned by method
        self.assertIn(returnmsg, room_create,
                      msg="Living Space not successfully created!!")

    def test_add_fellow(self):
        """ Tests if fellow has been added """
        # sets up the required parameters
        firstname = "James"
        lastname = "Mwangi"
        role = "Fellow"
        accomodation = 'Y'
        # expected return message
        returnmsg = "Fellow {} {} Added Successfully".format(
            firstname, lastname)
        # saves return from method to a variable
        add_fellow = self.amity.add_person(
            firstname, lastname, role, accomodation)
        # checks if the expected return what is actually returned by method
        self.assertIn(returnmsg, add_fellow, msg="Fellow not added!!")

    def test_add_staff(self):
        """ tests if staff has been added """
        # sets up the required parameters
        firstname = "John"
        lastname = "Mweri"
        role = "Staff"
        # expected return message
        returnmsg = "Staff {} {} Added Successfully".format(
            firstname, lastname)
        # saves return from method to a variable
        add_staff = self.amity.add_person(firstname, lastname, role)
        # checks if the expected return what is actually returned by method
        self.assertIn(returnmsg, add_staff, msg="Staff not added!!")

    def test_fellow_allocated_office(self):
        """ tests if fellow has been allocated office """
        # sets up the required parameters
        roomname = ['meru', 'embu']
        # creates the rooms
        self.amity.create_room("office", roomname)
        firstname = "James"
        lastname = "Mwangi"
        role = "Fellow"
        accomodation = 'Y'
        # expected return message
        returnmsg = "Fellow {} {} assigned office".format(firstname, lastname)
        # saves return from method to a variable
        add_fellow = self.amity.add_person(
            firstname, lastname, role, accomodation)
        # checks if the expected return what is actually returned by method
        self.assertIn(returnmsg, add_fellow, msg="Fellow not added!!")

    def test_fellow_allocated_living_space(self):
        """ tests if fellow has been allocated office """
        # sets up the required parameters
        roomname = ['meru', 'embu']
        # creates the rooms
        self.amity.create_room("living", roomname)
        firstname = "James"
        lastname = "Mwangi"
        role = "Fellow"
        accomodation = 'Y'
        # expected return message
        returnmsg = "Fellow {} {} assigned living space".format(
            firstname, lastname)
        # saves return from method to a variable
        add_fellow = self.amity.add_person(
            firstname, lastname, role, accomodation)
        # checks if the expected return what is actually returned by method
        self.assertIn(returnmsg, add_fellow,
                      msg="Fellow not assigned living space!!")

    def test_staff_allocated_office(self):
        """ tests if staff has been allocated office """
        # sets up the required parameters
        firstname = "John"
        lastname = "Mwangi"
        role = "Staff"
        # expected return message
        other_rooms = ['mombasa', 'malindi']
        self.amity.create_room("office", other_rooms)
        returnmsg = "Staff {} {} assigned office".format(
            firstname, lastname)
        # saves return from method to a variable
        add_staff = self.amity.add_person(firstname, lastname, role)
        # checks if the expected return what is actually returned by method
        self.assertIn(returnmsg, add_staff, msg="Staff not added!!")

    def test_staff_cannot_get_lspace(self):
        firstname = "John"
        lastname = "Mwangi"
        role = "Staff"
        # expected return message
        other_rooms = ['mombasa', 'malindi']
        self.amity.create_room("office", other_rooms)
        rooms = ['kenya', 'nanyuki']
        self.amity.create_room("living", rooms)
        returnmsg = "Staff cannot be assigned accomodation!!!"
        # saves return from method to a variable
        add_staff = self.amity.add_person(firstname, lastname, role, "Y")
        # checks if the expected return what is actually returned by method
        self.assertIn(returnmsg, add_staff, msg="Staff got accomodation!!")

    def test_print_allocations_without_people(self):
        with self.captured_output() as (out, err):
            self.amity.print_allocations({"--o": "testfile"})
            output = out.getvalue()
        self.assertIn("No rooms available!! please create rooms and add people!!",
                      output, msg="Allocations list printed")

    def test_fellow_not_given_office(self):
        other_rooms = ['mombasa']
        self.amity.create_room("office", other_rooms)
        load_people = self.amity.load_people("persons")
        firstname = "John"
        lastname = "Mwangi"
        role = "Fellow"
        message = "Fellow not assigned office!!"
        returnmsg = self.amity.add_person(firstname, lastname, role, "Y")
        self.assertIn(message, returnmsg, msg="Staff allocated office")

    def test_load_people(self):
        """ tests if people were loaded to the application from file """
        # sets up the required parameters
        testfile = "persons"
        # expected return message
        returnmsg = "Added Successfully"
        # saves return from method to a variable
        load_people = self.amity.load_people(testfile)
        # checks if the expected return what is actually returned by method
        self.assertIn(returnmsg, load_people,
                      msg="People not loaded from file!")

    def test_for_fellow_inheritance(self):
        """ tests if fellow class inherits from person class """
        self.assertTrue(issubclass(Fellow, Person))

    def test_for_staff_inheritance(self):
        """ tests if staff class inherits from person class """
        self.assertTrue(issubclass(Staff, Person))

    def test_reallocate_person(self):
        """ tests if person was reallocated """
        # sets up the required parameters
        roomname = ['meru', 'embu']
        other_rooms = ['mombasa', 'malindi']
        name = "John Mark"
        # creates rooms
        self.amity.create_room("office", roomname)
        # creates person
        self.amity.add_person("John", "Mark", "fellow", "N")
        # creates more rooms after adding person
        self.amity.create_room("office", other_rooms)
        # checks if fellow is in fellow list
        for fellow in self.amity.fellows:
            if fellow.name == name:
                fellowid = fellow.person_id
        # expected return message
        message = "has been reallocated successfully"
        # saves return from method to a variable
        returnmsg = self.amity.reallocate_person(fellowid, "mombasa")
        # checks if the expected return what is actually returned by method
        self.assertIn(message, returnmsg, msg="Not reallocated")

    def test_prints_allocations_tofile(self):
        """ tests if it prints room allocations to file """
        # sets up the required parameters
        roomname = ['meru', 'embu']
        # creates rooms
        self.amity.create_room("office", roomname)
        # creates person
        self.amity.add_person("John", "Mark", "fellow", "N")
        # gets print output from running method print_allocations with file
        # option
        with self.captured_output() as (out, err):
            self.amity.print_allocations({"--o": "testfile"})
            output = out.getvalue()
            # checks if the expected output what is actually returned by method
        self.assertIn("list of allocations has been saved",
                      output, msg="allocations not printed to file!")

    def test_prints_allocations_screen(self):
        """ tests if it prints room allocations to screen """
        # sets up the required parameters
        roomname = ['meru', 'embu']
        # creates rooms
        self.amity.create_room("office", roomname)
        # adds person
        self.amity.add_person("John", "Mark", "fellow", "N")
        # gets print output from running method print_allocations
        with self.captured_output() as (out, err):
            self.amity.print_allocations({'--o': ''})
            output = out.getvalue()
        # checks if the expected output what is actually returned by method
        self.assertIn("Name:",
                      output, msg="allocations not printed to screen!")

    def test_no_unallocated(self):
        office_name = ['meru', 'embu', 'valhalla']
        ls_name = ['nairobi', 'meru']
        self.amity.create_room("office", office_name)
        self.amity.create_room("living", ls_name)
        self.amity.add_person("John", "Mark", "fellow", "Y")
        with self.captured_output() as (out, err):
            self.amity.print_unallocated({"--o": ""})
            output = out.getvalue()

        message = "All persons were allocated offices"
        self.assertIn(message, output, msg="Printed unallocated persons!")

    def test_print_unallocated_toscreen(self):
        """ tests if it prints unallocated staff and fellows """
        # adds person
        self.amity.add_person("John", "Mark", "fellow", "Y")
        # gets print output from running method print_unallocated
        with self.captured_output() as (out, err):
            self.amity.print_unallocated({"--o": ""})
            output = out.getvalue()
            # expected output
        message = "Here is the list of people not allocated"
        # checks if the expected output what is actually returned by method
        self.assertIn(message, output,
                      msg="unallocated people not printed to screen!")

    def test_print_unallocated_tofile(self):
        """ tests if it prints unallocated staff and fellows """
        # adds person
        self.amity.add_person("John", "Mark", "fellow", "Y")
        # gets print output from running method print_unallocated
        with self.captured_output() as (out, err):
            self.amity.print_unallocated({"--o": "unallocated"})
            output = out.getvalue()
        message = "list of unallocated persons has been saved to"
        self.assertIn(message, output,
                      msg="unallocated people not printed to file!")

    def test_prints_room(self):
        """ tests if it prints list of people in a room """
        # sets up parameters
        room_name = ['meru', 'embu', 'valhalla']
        # creates room
        self.amity.create_room("office", room_name)
        # adds people
        self.amity.add_person("John", "Mark", "fellow", "Y")
        roomname = "valhalla"
        # checks if expected output is in method return
        self.assertIn("Room: VALHALLA", self.amity.print_room(roomname),
                      msg="Could not print room!")

    def test_print_all_people(self):
        """ tests if a person list was printed """
        # sets up parameters
        room_name = ['meru', 'embu', 'valhalla']
        # creates room
        self.amity.create_room("office", room_name)
        # adds person
        self.amity.add_person("John", "Mark", "fellow", "Y")
        # captures print output from method
        with self.captured_output() as (out, err):
            self.amity.print_all_people({'': ''})
            output = out.getvalue()
            # checks if expected output is in method return
        self.assertIn("Persons List", output,
                      msg="people not printed to file!")

    def test_print_all_rooms(self):
        """ tests if a room list was printed """
        # sets up parameters
        room_name = ['meru', 'embu', 'valhalla']
        # creates room
        self.amity.create_room("office", room_name)
        # adds person
        self.amity.add_person("John", "Mark", "fellow", "Y")
        # captures print output from method
        with self.captured_output() as (out, err):
            self.amity.print_all_rooms({'': ''})
            output = out.getvalue()
            # checks if expected output is in method return
        self.assertIn("Rooms List", output, msg="people not printed to file!")

    def test_delete_fellow(self):
        """test if person was successfully deleted """
        # sets up parameters
        room_name = ['meru', 'embu', 'valhalla']
        # creates room
        self.amity.create_room("office", room_name)
        firstname = "John"
        lastname = "Mark"
        name = "{} {}".format(firstname, lastname)
        self.amity.add_person(firstname, lastname, "fellow", "Y")
        # searches for person and retrieves id
        for fellow in self.amity.fellows:
            if fellow.name == name:
                fellow_id = fellow.person_id
        returnmsg = self.amity.delete_person(fellow_id)
        # checks if expected output is in method return
        self.assertIn("{} deleted successfully".format(name),
                      returnmsg, msg="Person was not deleted!")

    def test_delete_staff(self):
        """test if person was successfully deleted """
        # sets up parameters
        room_name = ['meru', 'embu', 'valhalla']
        # creates room
        self.amity.create_room("office", room_name)
        firstname = "John"
        lastname = "Mark"
        name = "{} {}".format(firstname, lastname)
        self.amity.add_person(firstname, lastname, "staff")
        # searches for person and retrieves id
        for staff in self.amity.staff:
            if staff.name == name:
                staff_id = staff.person_id
        returnmsg = self.amity.delete_person(staff_id)
        # checks if expected output is in method return
        self.assertIn("{} deleted successfully".format(name),
                      returnmsg, msg="Person was not deleted!")

    def test_delete_person_from_lspace(self):
         # sets up parameters
        room_name = ['meru', 'embu', 'valhalla']
        # creates room
        self.amity.create_room("office", room_name)
        ls_name = ['nairobi', 'meru']
        self.amity.create_room("living", ls_name)
        firstname = "John"
        lastname = "Mark"
        name = "{} {}".format(firstname, lastname)
        self.amity.add_person(firstname, lastname, "fellow", "Y")
        # searches for person and retrieves id
        for fellow in self.amity.fellows:
            if fellow.name == name:
                fellow_id = fellow.person_id
        returnmsg = self.amity.delete_person(fellow_id)
        self.assertIn("{} removed from living space".format(name),
                      returnmsg, msg="Person was not deleted from living space!")

    def test_delete_office(self):
        # sets up parameters
        room_name = ['meru', 'embu', 'valhalla']
        # creates room
        self.amity.create_room("office", room_name)
        name = 'Embu'
        for room in self.amity.office:
            if room.room_name.upper() == name.upper():
                roomid = room.room_id
        returnmsg = self.amity.delete_room(roomid)
        self.assertIn("removed {} from list of offices".format(name),
                      returnmsg, msg="Room was not deleted!")

    def test_save_state(self):
        """Tests if data has been stored in db"""
        # sets up parameters
        room_name = ['meru', 'embu', 'valhalla']
        # create room
        self.amity.create_room("office", room_name)
        # add person
        self.amity.add_person("John", "Mark", "fellow", "Y")
        returnmsg = self.amity.save_state({'--db': 'monthly'})
        self.assertIn("Please give the DB name!",
                      returnmsg, msg="Could not store to database!")

    def test_db_exists_for_save_state(self):
        """Tests if data has been stored in db"""
        # sets up parameters
        room_name = ['meru', 'embu', 'valhalla']
        # create room
        self.amity.create_room("office", room_name)
        # add person
        self.amity.add_person("John", "Mark", "fellow", "Y")
        returnmsg = self.amity.save_state({'--db': ''})
        self.assertIn("Data stored successfully in database",
                      returnmsg, msg="Could not store to database!")

    def save_state_invalid_input(self):
        room_name = ['meru', 'embu', 'valhalla']
        # create room
        self.amity.create_room("office", room_name)
        # add person
        self.amity.add_person("John", "Mark", "fellow", "Y")
        returnmsg = self.amity.save_state({'--db': '65654454'})
        self.assertIn("Invalid input! Please enter the database name in string format",
                      returnmsg, msg="Could not store to database!")

    def test_load_state(self):
        """ tests if data has been loaded from db """
        # sets up parameters
        database = "monthly"
        returnmsg = self.amity.load_state(database)
        self.assertIn("Data loaded successfully from database",
                      returnmsg, msg="Could not load from database!")

    def tearDown(self):
        """ free up resources """
        self.office = []
        self.livingspace = []
        self.person = []
        self.fellow = []
        self.staff = []
        del self.amity


if __name__ == '__main__':
    unittest.main()
