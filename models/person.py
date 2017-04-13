
class Person(object):
    def __init__(self, firstname, lastname, role):
        self.firstname = firstname
        self.lastname = lastname
        self.role = role
        self.accomodation = ''

class Fellow(Person):
    def __init__(self, firstname, lastname, role, accomodation):
        super(Fellow, self).__init__(firstname, lastname, role="FELLOW")
        name = "{} {}".format(firstname, lastname)
        self.name = name
        self.office = ''
        self.accomodation = accomodation
        self.person_id = id(name)

class Staff(Person):
    def __init__(self, firstname, lastname, role):
        super(Staff, self).__init__(firstname, lastname, role="STAFF")
        name = "{} {}".format(firstname, lastname)
        self.name = name
        self.office = ''
        self.person_id = id(name)
        self.accomodation = ''
