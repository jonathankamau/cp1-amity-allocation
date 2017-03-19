""" Test file for Person class"""

from unittest import TestCase
from models.person import Person


class PersonTest(TestCase):
    """test class for Person"""
    def setUp(self):
        """ sets up the tests """
        self.person = Person
        self.add_person = Person.add_person

    def test_for_instance_of_class(self):
        """ checks if add_person is an instance of class Person"""
        self.assertIsInstance(self.add_person, self.person)

    def test_for_addperson_add(self):
        """ checks for successful add """
        self.assertEqual(self.add_person, "Person created successfully")

    def test_for_addperson_fail(self):
        """ checks for unsuccessful add"""
        self.assertEqual(self.add_person, "Failed to add person")


if __name__ == '__main__':
    unittest.main()







