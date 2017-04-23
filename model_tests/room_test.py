from unittest import TestCase
from models.room import Room

class RoomTest(TestCase):
    """ initializes the test class """
    def setUp(self):
        self.create_room = create_room

    def test_creates_office(self):
        self.create_room('o', 'Oculus')
        self.assertNotEqual(len(self.all_rooms), 0)
        self.assertIn('OCULUS', self.office_spaces.keys())
        self.all_rooms = []

    def test_creates_living_space(self):
        amity = Amity()
        amity.create_room('l', 'tsavo')
        self.assertNotEqual(len(amity.all_rooms), 0)
        self.assertIn('tsavo', Amity.living_spaces.keys())
        amity.all_rooms = []


if __name__ == '__main__':
    unittest.main()
