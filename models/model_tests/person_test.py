""" Test file for Person class"""

import unittest 
from ..person import Person, Fellow, Staff


class PersonTest(unittest.TestCase):
    """test class for Person"""
    def setUp(self):
       people = "jonathan"
       self.people=people
       

    def test_for_fellow_inheritance(self):
        self.assertTrue( issubclass(Fellow, Person) )

    def test_for_staff_inheritance(self):
        self.assertTrue( issubclass(Staff, Person) )

    def test_for_personexists(self):
        self.assertEqual(self.people,"jonatha")

    





"""if __name__ == '__main__':
    unittest.main()"""







