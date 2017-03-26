import unittest
from ..room import Room, Office, LivingSpace
from ..amity import Amity
from ..person import Person, Fellow, Staff

class AmityTest(unittest.TestCase):
    """ initializes the test class """
    def setUp(self):
        self.room = Room()
        self.office = Office()
        self.livingspace = LivingSpace
        self.room_name = 'Hyena'
        self.room_type = 'Living Space'
        self.room_capacity = 5
        self.person = Person()
        self.fellow = Fellow()
        self.staff = Staff()
        self.amity = Amity()

    def test_for_livingspace_inheritance(self):
        self.assertTrue( issubclass(LivingSpace, Room) )

    def test_for_office_inheritance(self):
        self.assertTrue( issubclass(Office, Room ) )  
    def test_for_room_added(self):
        room1 = "Forest"
        roomtype = "Office"
        list1 = len(self.amity.all_rooms)
        self.assertEqual(list1, 0)
        returnmsg = "Created Room Successfully"
        self.assertEqual(self.amity.create_room(room1,roomtype), returnmsg, msg="Room not successfully created")
        list2 = len(self.amity.all_rooms)
        self.assertNotEqual(list1,list2,"Lists are equal")
        #self.assertEqual(len(living_space_list), 0)
    def test_office_capacity(self):
        self.assertEqual(self.office.max_capacity, 8)
    def test_living_space_capacity(self):
        self.assertEqual(self.livingspace.max_capacity, 20)

    def test_for_fellow_inheritance(self):
        self.assertTrue( issubclass(Fellow, Person) )

    def test_for_staff_inheritance(self):
        self.assertTrue( issubclass(Staff, Person) )

    def test_for_personexists(self):
        self.assertEqual(self.amity.all_people,"jonatha")
    
    def test_add_person(self):
        person1 = "Ben"
        status1 = "FELLO"
        list3 = len(self.amity.all_people)
        self.assertEqual(list3,0)
        list4 = len(self.amity.all_people)
        self.assertEqual(self.amity.add_person(person1, status1),"Fellow Added Successfully",msg="Fellow was not added successfully")

    def test_if_added_fellow_is_stored(self):
        person1 = "Bee"
        status1 = "FELLO"
        self.amity.add_person(person1, status1)
        self.assertEqual(self.amity.add_person(person1, status1),"Fellow Added Successfully",msg="Fellow was not added successfully")
        for x, y in self.amity.fellow_dict.items():
            if y==person1:
                self.assertEqual(person1, y, "Not Found")
            

    def test_for_created_living_space(self):
        room1 = "ChillZone"
        roomtype = "Living Spac"
        list1 = len(self.amity.all_rooms)
        self.assertEqual(list1, 0)
        returnmsg = "living space created successfully"
        self.assertEqual(self.amity.create_room(room1,roomtype), returnmsg, msg="Living space not successfully created")
        list2 = len(self.amity.all_rooms)
        self.assertNotEqual(list1,list2,"Lists are equal")
       
    def test_assign_fellow_office(self):
         fellow_name = "Alex"
         fellow_id = "F002"
         fel_office = self.amity.allocate_fellow_office(fellow_name, fellow_id)
         self.assertEqual(fel_office, "Office assigned successfully to "+fellow_name, msg="Not Assigned")

    def test_assign_staff_office(self):
        staff_name = "Hellen"
        staff_id = "ST002"
        staf_office = self.amity.allocate_staff_office(staff_name, staff_id)
        self.assertEqual(staf_office, "Office assigned successfully to "+staff_name, msg="Not Assigned")

    def test_assign_fellow_living_space(self):
        fellow_name = "Alex"
        fellow_id = "F002"
        fel_ls = self.amity.allocate_fellow_livingspace(fellow_name, fellow_id)
        self.assertEqual(fel_ls, "Living Space assigned successfully to "+fellow_name, msg="Not Assigned")
    def test_for_file_open(self):
       sample_person = "Francis"
       file_open = self.amity.load_people()
       self.assertIn(sample_person, file_open, msg="Cannot find name")
    def test_reallocate_fellow_office(self):
        sample_id = "ST012"
        sample_room = "Valhalla"
        fname = str(self.amity.fellow_dict.get(sample_id))  
        fel = self.amity.reallocate_fellow_office(sample_id, sample_room)
        self.assertEqual(fel, fname+" reallocated successfully to "+sample_room, msg="Not reallocated")

    def test_reallocate_staff_office(self):
        sample_id = "F012"
        sample_room = "Valhalla"
        fname = str(self.amity.staff_dict.get(sample_id))  
        fel = self.amity.reallocate_staff_office(sample_id, sample_room)
        self.assertEqual(fel, fname+" reallocated successfully to "+sample_room, msg="Not reallocated")

    def test_reallocate_fellow_living_space(self):
        sample_id = "ST012"
        sample_room = "Valhalla"
        fname = str(self.amity.fellow_dict.get(sample_id))  
        fel = self.amity.reallocate_fellow_living_space(sample_id, sample_room)
        self.assertEqual(fel, fname+" reallocated successfully to "+sample_room, msg="Not reallocated")

    def test_add_person_isint(self):
        self.assertNotIsInstance(self.amity.add_person("Ben", "FELLOW"), int)
    def test_add_person_isdict(self):
        self.assertNotIsInstance(self.amity.add_person("Ben", "FELLOW"), dict)
    def test_add_person_isstring(self):
        self.assertIsInstance(self.amity.add_person("Ben", "FELLOW"), str)
    def test_add_person_islist(self):
        self.assertNotIsInstance(self.amity.add_person("Ben", "FELLOW"), list)
    def test_create_room_isint(self):
        self.assertNotIsInstance(self.amity.create_room("Voi", "Living Space"), int)
    def test_create_room_isdict(self):
        self.assertNotIsInstance(self.amity.create_room("Voi", "Living Space"), dict)
    def test_create_room_islist(self):
        self.assertNotIsInstance(self.amity.create_room("Voi", "Living Space"), list)
    def test_create_room_isstring(self):
        self.assertIsInstance(self.amity.create_room("Voi", "Living Space"), list)
    def test_allocate_fellow_office_isstring(self):
        fel_office = self.amity.allocate_fellow_office("Alex", "F002")
        self.assertIsInstance(fel_office, str)
    def test_allocate_fellow_living_space_isstring(self):
        fel_ls = self.amity.allocate_fellow_livingspace("Alex", "F002")
        self.assertIsInstance(fel_ls, str)
    def test_allocate_staff_office_isstring(self):
        staf_office = self.amity.allocate_staff_office("Hellen", "ST002")
        self.assertIsInstance(staf_office, str)
    def test_load_people_isistring(self):
        self.assertIsInstance(self.amity.load_people(), str)
    def test_reallocate_fellow_office_isstring(self): 
        fel = self.amity.reallocate_fellow_office("ST012", "Valhalla")
        self.assertIsInstance(fel, str)
    def test_reallocate_staff_office_isstring(self):
        fel = self.amity.reallocate_staff_office("F012", "Valhalla")
        self.assertIsInstance(fel, str)
    def test_reallocate_fellow_living_space_isstring(self):
        fel = self.amity.reallocate_fellow_living_space("ST012", "Valhalla")
        self.assertIsInstance(fel, str)







    def tearDown(self):
        """ """


if __name__ == '__main__':
    unittest.main()
