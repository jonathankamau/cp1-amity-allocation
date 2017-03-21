import unittest
from ..room import Room, Office, LivingSpace

class RoomTest(unittest.TestCase):
    """ initializes the test class """
    def setUp(self):
        

     def test_for_livingspace_inheritance(self):
        self.assertTrue( issubclass(LivingSpace, Room) )

    def test_for_office_inheritance(self):
        self.assertTrue( issubclass(Office, Room ) )

    def test_if_room_exists(self):
        self.assertIn(Room.load_rooms, Room.create_room('tsavo'))

    def test_for_create_room_return(self):
        self.assertEqual(Room.create_room, "Room created successfully")
        
    def check_if_load_room_has_returned(self):
        self.assertNotEqual(Room.load_rooms, " ")

    def check_if_print_room_has_returned(self):
        self.assertNotEqual(Room.print_room, " ")

    def test_capacity_office_space(self):
        tsavo = Office("TSAVO")
        self.assertEqual(tsavo.room_capacity, 6)
        self.assertEqual(tsavo.room_type, "OFFICE")

    def test_capacity_living_space(self):
        mara = LivingSpace("MARA")
        self.assertEqual(mara.room_capacity, 4)
        self.assertEqual(mara.room_type, "LIVING SPACE")

    

    def tearDown(self):
        """ """


if __name__ == '__main__':
    unittest.main()
