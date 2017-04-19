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

    def test_for_create_office(self):
        """ Tests if office has been created """
        roomname = "Forest"
        roomtype = "Office"
        returnmsg = "The following offices were created successfully"
        room_create = self.amity.create_room(roomtype, roomname)
        self.assertIn(returnmsg, room_create, msg="Office not successfully created!!")

    def test_for_create_livingspace(self):
        """ Tests if living space has been created """
        roomname = "Coast"
        roomtype = "living"
        returnmsg = "The following living spaces were created successfully"
        room_create = self.amity.create_room(roomtype, roomname)
        self.assertIn(returnmsg, room_create, msg="Living Space not successfully created!!")

    def test_add_fellow(self):
        """ Tests if fellow has been added """
        firstname = "James"
        lastname = "Mwangi"
        role = "Fellow"
        accomodation = 'Y'
        returnmsg = "Fellow {} {} Added Successfully".format(firstname, lastname)
        add_fellow = self.amity.add_person(firstname, lastname, role, accomodation)
        self.assertIn(returnmsg, add_fellow, msg="Fellow not added!!")

    def test_add_staff(self):
        """ tests if staff has been added """
        firstname = "John"
        lastname = "Mweri"
        role = "Staff"
        returnmsg = "Staff {} {} Added Successfully".format(firstname, lastname)
        add_staff = self.amity.add_person(firstname, lastname, role)
        self.assertIn(returnmsg, add_staff, msg="Staff not added!!")

    def test_fellow_allocated_office(self):
        """ tests if fellow has been allocated office """
        roomname = ['meru', 'embu']
        self.amity.create_room("office", roomname)
        firstname = "James"
        lastname = "Mwangi"
        role = "Fellow"
        accomodation = 'Y'
        returnmsg = "Fellow {} {} assigned office".format(firstname, lastname)
        add_fellow = self.amity.add_person(firstname, lastname, role, accomodation)
        self.assertIn(returnmsg, add_fellow, msg="Fellow not added!!")

    def test_staff_allocated_office(self):
        """ tests if staff has been allocated office """
        firstname = "John"
        lastname = "Mwangi"
        role = "Staff"
        returnmsg = "Staff {} {} Added Successfully".format(firstname, lastname)
        add_staff = self.amity.add_person(firstname, lastname, role)
        self.assertIn(returnmsg, add_staff, msg="Staff not added!!")

    def test_load_people(self):
        """ tests if people were loaded to the application from file """
        testfile = "persons"
        returnmsg = "Added Successfully"
        load_people = self.amity.load_people(testfile)
        self.assertIn(returnmsg, load_people, msg="People not loaded from file!")

    def test_for_fellow_inheritance(self):
        """ tests if fellow class inherits from person class """
        self.assertTrue(issubclass(Fellow, Person))

    def test_for_staff_inheritance(self):
        """ tests if staff class inherits from person class """
        self.assertTrue(issubclass(Staff, Person))

    def test_reallocate_person(self):
        """ tests if person was reallocated """
        roomname = ['meru', 'embu']
        name = "John Mark"
        self.amity.create_room("office", roomname)
        self.amity.add_person("John", "Mark", "fellow", "N")
        for fellow in self.amity.fellows:
            if fellow.name == name:
                fellowid = fellow.person_id
        message = "has been reallocated successfully"
        returnmsg = self.amity.reallocate_person(fellowid, "embu")
        self.assertIn(message, returnmsg, msg="Not reallocated")

    def test_prints_allocations_tofile(self):
        """ tests if it prints room allocations to file """
        roomname = ['meru', 'embu']
        self.amity.create_room("office", roomname)
        self.amity.add_person("John", "Mark", "fellow", "N")
        with self.captured_output() as (out, err):
            self.amity.print_allocations({"--o":"testfile"})
            output = out.getvalue()
        self.assertIn("list of allocations has been saved",
                      output, msg="allocations not printed to file!")

    def test_prints_allocations_screen(self):
        """ tests if it prints room allocations to screen """
        roomname = ['meru', 'embu']
        self.amity.create_room("office", roomname)
        self.amity.add_person("John", "Mark", "fellow", "N")
        with self.captured_output() as (out, err):
            self.amity.print_allocations({'--o':''})
            output = out.getvalue()
        self.assertIn("Name:",
                      output, msg="allocations not printed to screen!")

    def test_print_unallocated_toscreen(self):
        """ tests if it prints unallocated staff and fellows """
        self.amity.add_person("John", "Mark", "fellow", "Y")
        with self.captured_output() as (out, err):
            self.amity.print_unallocated({"--o":""})
            output = out.getvalue()
        message = "Here is the list of people not allocated"
        self.assertIn(message, output, msg="unallocated people not printed to screen!")

    def test_print_unallocated_tofile(self):
        """ tests if it prints unallocated staff and fellows """
        self.amity.add_person("John", "Mark", "fellow", "Y")
        with self.captured_output() as (out, err):
            self.amity.print_unallocated({"--o":"unallocated"})
            output = out.getvalue()
        message = "list of unallocated persons has been saved to"
        self.assertIn(message, output, msg="unallocated people not printed to file!")

    def test_prints_room(self):
        """ tests if it prints list of people in a room """
        room_name = ['meru', 'embu', 'valhalla']
        self.amity.create_room("office", room_name)
        self.amity.add_person("John", "Mark", "fellow", "Y")
        roomname = "valhalla"
        self.assertIn("Room: VALHALLA", self.amity.print_room(roomname),
                      msg="Could not print room!")

    def test_print_all_people(self):
        """ tests if a person list was printed """
        room_name = ['meru', 'embu', 'valhalla']
        self.amity.create_room("office", room_name)
        self.amity.add_person("John", "Mark", "fellow", "Y")
        with self.captured_output() as (out, err):
            self.amity.print_all_people({'':''})
            output = out.getvalue()
        self.assertIn("Persons List", output, msg="people not printed to file!")

    def test_print_all_rooms(self):
        """ tests if a room list was printed """
        room_name = ['meru', 'embu', 'valhalla']
        self.amity.create_room("office", room_name)
        self.amity.add_person("John", "Mark", "fellow", "Y")
        with self.captured_output() as (out, err):
            self.amity.print_all_rooms({'':''})
            output = out.getvalue()
        self.assertIn("Rooms List", output, msg="people not printed to file!")

    def test_delete_person(self):
        """test if person was successfully deleted """
        room_name = ['meru', 'embu', 'valhalla']
        self.amity.create_room("office", room_name)
        firstname = "John"
        lastname = "Mark"
        name = "{} {}".format(firstname, lastname)
        self.amity.add_person(firstname, lastname, "fellow", "Y")
        for fellow in self.amity.fellows:
            if fellow.name == name:
                fellow_id = fellow.person_id

        returnmsg = self.amity.delete_person(fellow_id)
        self.assertIn("deleted successfully", returnmsg, msg="Person was not deleted!")

    def test_save_state(self):
        """Tests if data has been stored in db"""
        room_name = ['meru', 'embu', 'valhalla']
        self.amity.create_room("office", room_name)
        self.amity.add_person("John", "Mark", "fellow", "Y")
        returnmsg = self.amity.save_state({'--db':'monthly'})
        self.assertIn("Data stored successfully in database",
                      returnmsg, msg="Could not store to database!")

    def test_load_state(self):
        """ tests if data has been loaded from db """
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
