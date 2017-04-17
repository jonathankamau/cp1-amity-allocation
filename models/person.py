
class Person(object):
    def __init__(self, firstname, lastname, role):
        self.firstname = firstname
        self.lastname = lastname
        self.name = "{} {}".format(self.firstname, self.lastname)
        self.role = role
        self.accomodation = ''
        self.person_id = 0

class Fellow(Person):
    def __init__(self, firstname, lastname, role, accomodation):
        super(Fellow, self).__init__(firstname, lastname, role="FELLOW")
        name = "{} {}".format(firstname, lastname)
        self.name = name
        self.office = ''
        self.living = ''
        self.accomodation = accomodation
        self.person_id = 0

class Staff(Person):
    def __init__(self, firstname, lastname, role):
        super(Staff, self).__init__(firstname, lastname, role="STAFF")
        name = "{} {}".format(firstname, lastname)
        self.name = name
        self.office = ''
        self.person_id = 0
        self.accomodation = ''
