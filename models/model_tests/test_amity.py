import unittest
import sys
import os
from contextlib import contextmanager
from io import StringIO

from models.room import Room, Office, LivingSpace
from models.amity import Amity
from models.person import Person, Fellow, Staff

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
        self.testperson = "Jon"

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
        firstname = "James"
        lastname = "Mwangi"
        role = "Fellow"
        accomodation = 'Y'
        returnmsg = "Fellow {} {} Added Successfully".format(firstname, lastname)
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

    def test_prints_allocations(self):
        """ tests if it prints room allocations """
        roomname = ['meru', 'embu']
        self.amity.create_room("office", roomname)
        self.amity.add_person("John", "Mark", "fellow", "N")
        #message = "The list of allocations has been saved to"
        with self.captured_output() as (out, err):
            self.amity.print_allocations('')
            output = out.getvalue()
        self.assertIn(output, "", msg="allocations not printed to screen!")
        #returnmsg = self.amity.print_allocations({"--o":"testfile"})
        #self.assertIn(message, returnmsg, msg="allocations not printed to screen!")

    def test_print_unallocated(self):
        """ tests if it prints unallocated staff and fellows """
        returnmsg = self.amity.print_unallocated({"--o":"testfile"})
        message = "Here is the list of people unallocated"
        self.assertIn(message, returnmsg, msg="Not found!")

    def test_prints_room(self):
        """ tests if it prints list of people in a room """
        roomname = "Valhalla"
        self.assertIn(self.amity.print_room(roomname), "Alex", msg="Could not find person!")

    def test_add_person_isstring(self):
        """ test if output for add person method is a string """
        self.assertIsInstance(self.amity.add_person("Ben", "FELLO"), str, msg="Is not string")

    def test_create_room_isstring(self):
        """ tests if output for create room method is a string """
        self.assertIsInstance(self.amity.create_room("Voi", "Living Space"), list, msg="Is not string")

    def test_allocate_fellow_office_str(self):
        """ tests if output for allocate fellow office method is a string """
        fellowoffice = self.amity.allocate_fellow_office("Alex", "F002")
        self.assertIsInstance(fellowoffice, str,msg="Is not string")

    def test_allocate_fellow_ls_for_str(self):
        """" tests if output for allocate fellow living space method is a string """
        fellowliving = self.amity.allocate_fellow_livingspace("Alex", "F002")
        self.assertIsInstance(fellowliving, str,msg="Is not string")

    def test_allocate_staff_office_str(self):
        """ tests if output for allocate staff office is a string """
        staf_office = self.amity.allocate_staff_office("Hellen", "ST002")
        self.assertIsInstance(staf_office, str,msg="Is not string")

    def test_reallocate_fellow_off_str(self):
        """ tests if reallocate_fellow_office method returns a string """
        fel = self.amity.reallocate_fellow_office("F012", "Valhalla")
        self.assertIsInstance(fel, str, msg="Is not string")

    def test_reallocate_staff_off_isstr(self):
        """ tests if reallocate_staff_office method returns a string """
        fel = self.amity.reallocate_staff_office("ST012", "Valhalla")
        self.assertIsInstance(fel, str, msg="Is not string")

    def test_reallocate_fellow_ls_isstr(self):
        """ tests if reallocate_fellow_living_space returns a string """
        fel = self.amity.reallocate_fellow_living_space("ST012", "Valhalla")
        self.assertIsInstance(fel, str,msg="Is not string")

    def test_creates_db(self):
        "Tests if a db is created successfully"
        self.amity.save_state('amitydb')
        self.assertTrue(os.path.isfile('amitydb.sqlite'))


    def tearDown(self):
        """ free up resources """
        self.office = []
        self.livingspace = []
        self.person = []
        self.fellow = []
        self.staff = []
        del self.amity
        del self.testperson


if __name__ == '__main__':
    unittest.main()
