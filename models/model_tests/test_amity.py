import unittest
import os
from ..room import Room, Office, LivingSpace
from ..amity import Amity
from ..person import Person, Fellow, Staff

class AmityTest(unittest.TestCase):
    """ initializes the test class """
    def setUp(self):
        self.room = Room()
        self.office = Office()
        self.livingspace = LivingSpace
        self.room_capacity = 5
        self.person = Person()
        self.fellow = Fellow()
        self.staff = Staff()
        self.amity = Amity()
        self.testperson = "Jon"

    def test_living_space_inheritance(self):
        """ Tests if living space class inherits from room class """
        self.assertTrue(issubclass(LivingSpace, Room))

    def test_for_office_inheritance(self):
        """ Tests if office class inherits from room class """
        self.assertTrue(issubclass(Office, Room))

    def test_for_room_added(self):
        # a test must have just one reason to fail.
        """ Tests if room has been added """
        room1 = "Forest"
        roomtype = "Office"
        list1 = len(self.amity.all_rooms)
        self.assertEqual(list1, 0)
        returnmsg = "Created Room Successfully"
        room_create = self.amity.create_room(room1, roomtype)
        self.assertEqual(room_create, returnmsg, msg="Room not successfully created")
        list2 = len(self.amity.all_rooms)
        self.assertNotEqual(list1, list2, msg="Lists are equal")

    def test_office_capacity(self):
        """ checks if capacity of office has exceeded max limit """
        officespace = "Hogwarts"
        officelist = list(self.amity.office_occupied.values())
        officecounter = officelist.count(officespace)
        self.assertLessEqual(officecounter, self.office.max_capacity, msg="Exceeded maximum limit!")

    def test_living_space_capacity(self):
        """ tests if living space capacity has exceeded max limit """
        livingspace = "Kenya"
        lslist = list(self.amity.living_space_occupied.values())
        lscount = lslist.count(livingspace)
        self.assertLessEqual(lscount, self.livingspace.max_capacity, msg="Exceeded maximum limit!")


    def test_for_fellow_inheritance(self):
        """ tests if fellow class inherits from person class """
        self.assertTrue(issubclass(Fellow, Person))

    def test_for_staff_inheritance(self):
        """ tests if staff class inherits from person class """
        self.assertTrue(issubclass(Staff, Person))

    def test_if_person_exists(self):
        """ tests if person exists in person list """
        self.assertIn(self.testperson, self.amity.all_people, msg="Person not found")

    def test_add_person(self):
        """ tests if person was added """
        person1 = "Ben"
        status1 = "FELLO"
        list3 = len(self.amity.all_people)
        self.assertEqual(list3, 0)
        list4 = len(self.amity.all_people)
        self.assertEqual(list3, list4)
        amity_add = self.amity.add_person(person1, status1)
        self.assertEqual(amity_add, "Fellow Added Successfully", msg="Not added successfully")

    def test_if_added_fellow_is_stored(self):
        """ tests if fellow added was stored """
        person1 = "Bee"
        status1 = "FELLO"
        self.amity.add_person(person1, status1)
        amity_added = self.amity.add_person(person1, status1)
        self.assertEqual(amity_added, "Fellow Added Successfully", msg="Not stored successfully")
        for test_person in self.amity.fellow_dict.items():
            if test_person == person1:
                self.assertEqual(person1, test_person, msg="Not Found")

    def test_create_living_space(self):
        """ tests if living space was created successfully """
        room1 = "ChillZone"
        roomtype = "Living Spac"
        list1 = len(self.amity.all_rooms)
        self.assertEqual(list1, 0)
        returnmsg = "living space created successfully"
        test_ls = self.amity.create_room(room1, roomtype)
        self.assertEqual(test_ls, returnmsg, msg="Living space not successfully created")
        list2 = len(self.amity.all_rooms)
        self.assertNotEqual(list1, list2, msg="Lists are equal")

    def test_assign_fellow_office(self):
        """ tests if fellow was assigned office """
        fellow_name = "Alex"
        fellow_id = "F002"
        fel_office = self.amity.allocate_fellow_office(fellow_name, fellow_id)
        fel_msg = "Office assigned successfully to "+fellow_name
        self.assertEqual(fel_office, fel_msg, msg="Not Assigned")

    def test_assign_staff_office(self):
        """ tests if staff was assigned office """
        staff_name = "Hellen"
        staff_id = "ST002"
        staf_office = self.amity.allocate_staff_office(staff_name, staff_id)
        staf_msg = "Office assigned successfully to "+staff_name
        self.assertEqual(staf_office, staf_msg, msg="Not Assigned")

    def test_assign_fellow_living_space(self):
        """ checks if fellow was assigned living space """
        fellow_name = "Alex"
        fellow_id = "F002"
        fel_ls = self.amity.allocate_fellow_livingspace(fellow_name, fellow_id)
        fel_msg = "Living Space assigned successfully to "+fellow_name
        self.assertEqual(fel_ls, fel_msg, msg="Not Assigned")

    def test_if_person_file_exists(self):
        """ tests if file exists """
        filetitle = "personnel.txt"
        self.assertEqual(filetitle, self.amity.loadpeople, msg="file not found!")

    def test_if_file_is_open(self):
        """ tests if file was opened successfully """
        filetitle = "personnel.txt"
        sample_person = "Francis"
        file_open = self.amity.load_people(filetitle)
        self.assertIn(sample_person, file_open, msg="Cannot find name")

    def test_reallocate_fellow_office(self):
        """ tests if fellow was reallocated office """
        sample_id = "ST012"
        sample_room = "Valhalla"
        fname = str(self.amity.fellow_dict.get(sample_id))
        fel = self.amity.reallocate_fellow_office(sample_id, sample_room)
        fel_msg = "reallocated successfully to "+sample_room
        self.assertEqual(fel, fname+fel_msg, msg="Not reallocated")

    def test_reallocate_staff_office(self):
        """ tests if staff was reallocated to an office """
        sample_id = "F012"
        sample_room = "Valhalla"
        fname = str(self.amity.staff_dict.get(sample_id))
        staf = self.amity.reallocate_staff_office(sample_id, sample_room)
        staf_msg = fname+" reallocated successfully to "+sample_room
        self.assertEqual(staf, staf_msg, msg="Not reallocated")

    def test_reallocates_fellow_ls(self):
        """ tests if fellow was reallocated to a living space """
        sample_id = "ST012"
        sample_room = "Valhalla"
        fname = str(self.amity.fellow_dict.get(sample_id))
        fel = self.amity.reallocate_fellow_living_space(sample_id, sample_room)
        fel_msg = fname+" assigned successfully to "+sample_room
        self.assertEqual(fel, fel_msg, msg="Not reallocated")

    def test_print_allocations(self):
        """ tests if it prints room allocations """
        fname = "allocate.txt"
        self.amity.print_allocations(fname)
        scriptpath = os.path.dirname(__file__)
        filetitle = os.path.join(scriptpath, fname)
        fileopen = open(filetitle)
        persons = fileopen.read()
        self.assertIn('Hogwarts', persons, msg="Not found!")

    def test_print_unallocated(self):
        """ tests if it prints unallocated staff and fellows """
        fname = "unallocated.txt"
        self.amity.print_allocations(fname)
        scriptpath = os.path.dirname(__file__)
        filetitle = os.path.join(scriptpath, fname)
        fileopen = open(filetitle)
        persons = fileopen.read()
        self.assertIn('Alex', persons, msg="Not found!")

    def test_prints_room(self):
        """ tests if it prints list of people in a room """
        roomname = "Valhalla"
        self.assertIn(self.amity.print_room(roomname), "Alex", msg="Could not find person!")

    def test_add_person_isstring(self):
        """ test if output for add person method is a string """
        self.assertIsInstance(self.amity.add_person("Ben", "FELLOW"), str)

    def test_create_room_isstring(self):
        """ tests if output for create room method is a string """
        self.assertIsInstance(self.amity.create_room("Voi", "Living Space"), list)

    def test_allocate_fell_office_str(self):
        """ tests if output for allocate fellow office method is a string """
        fellowoffice = self.amity.allocate_fellow_office("Alex", "F002")
        self.assertIsInstance(fellowoffice, str)

    def test_allocate_fellow_ls_for_str(self):
        """" checks if output for allocate fellow living space method is a string """
        fellowliving = self.amity.allocate_fellow_livingspace("Alex", "F002")
        self.assertIsInstance(fellowliving, str)

    def test_allocate_staff_office_str(self):
        """ tests if output for allocate staff office is a string """
        staf_office = self.amity.allocate_staff_office("Hellen", "ST002")
        self.assertIsInstance(staf_office, str)

    def test_reallocate_fellow_off_str(self):
        """ tests if reallocate_fellow_office method returns a string """
        fel = self.amity.reallocate_fellow_office("F012", "Valhalla")
        self.assertIsInstance(fel, str)

    def test_reallocate_staff_off_isstr(self):
        """ tests if reallocate_staff_office method returns a string """
        fel = self.amity.reallocate_staff_office("ST012", "Valhalla")
        self.assertIsInstance(fel, str)

    def test_reallocate_fellow_ls_isstr(self):
        """ tests if reallocate_fellow_living_space returns a string """
        fel = self.amity.reallocate_fellow_living_space("ST012", "Valhalla")
        self.assertIsInstance(fel, str)

    def test_creates_db(self):
        "Tests if a db is created successfully"
        self.amity.save_state('amitydb')
        self.assertTrue(os.path.isfile('amitydb.sqlite'))


    def tearDown(self):
        """ free up resources """
        pass


if __name__ == '__main__':
    unittest.main()
