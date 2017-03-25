#from .person import Person, Fellow, Staff
#from .room import LivingSpace, Office
import os.path
class Amity:
    room_capacity = 6
    def __init__(self):
        self.office_list = []
        #office_list = office_list
        self.living_space_list = []
        #self.living_space_list = living_space_list
        
        #self.room_capacity = room_capacity
        self.all_rooms = []
        self.living_space_dict = {"Kenya":"O","Uganda":"V"}
        self.office_dict = {"Hogwarts":"O", "Bootcamp":"V","Vienna":"O"}
        self.all_people = []
        self.fellow_dict = {"F002":"Alex","F003":"John","F005":"Terry"}
        self.office_occupied = {"F002": "Hogwarts", "ST002":"Vienna"}
        self.living_space_occupied = {"F005":"Kenya"}
        self.staff_dict = {"ST001":"Musa","ST002":"Hellen"}
        self.person_room_dict = {3:"Machakos",5:"Kisumu"}
    
    
    """def reallocate_room_staff(self, id, room_name):
            for id in self.person_room_dict.keys:
                if self.person_room_dict.values == room_name:
                    self.staff_dict.keys = id
"""
    def add_person(self, name, status):
        if status == "FELLOW":
            id = "FOO4"
            self.fellow_dict[id] = name
            self.all_people.append(name)
            return "Fellow Added Successfully"
        else:
            id = "ST003"
            self.staff_dict[id] = name
            self.all_people.append(name)

            return "Staff Added Successfully"
    
    def create_room(self, room_name, room_type):
        if room_type == "Office":
            self.office_dict[room_name] = "V"
            self.all_rooms.append(room_name)
            return "Office created successfully"
        elif room_type == "Living Space":
            self.living_space_dict[room_name] = "V"
            self.all_rooms.append(room_name)
            return "living space created successfully"
    
    def allocate_fellow_office(self, name, person_id):
        for x, y in self.fellow_dict.items():
             if y == name and x == person_id:
                 if self.office_occupied.__contains__(x):
                     return "already allocated office"
                 else:
                     for a, b in self.office_dict.items():
                         if b =="V":
                             self.office_occupied[x]=a
                             self.office_dict[a]="O"
                             return "Office assigned successfully to %s", name
    def allocate_fellow_livingspace(self, name, person_id):
        for x, y in self.fellow_dict.items():
             if y == name and x == id:
                 if self.living_space_occupied.__contains__(x):
                     return "already allocated living space"
                 else:
                     for a, b in self.living_space_dict.items():
                         if b =="V":
                             self.living_space_occupied[x]=a
                             self.living_space_dict[a]="O"
                             return "Living Space assigned successfully to " +name

    def allocate_staff_office(self, name, person_id):
        for x, y in self.staff_dict.items():
             if y == name and x == id:
                 if self.office_occupied.__contains__(x):
                     return "already allocated office"
                 else:
                     for a, b in self.office_dict.items():
                         if b =="V":
                             self.office_occupied[x]=a
                             self.office_dict[a]="O"
                             return "Office assigned successfully to %s", name

    def load_people(self):
        scriptpath = os.path.dirname(__file__)
        filename = os.path.join(scriptpath, 'persons.txt')
        f = open(filename)
        persons = f.read()
        return persons

    def reallocate_room(self, person_id, room_name):
        pass
    def load_rooms(self):
        pass
    def print_room(self):
        pass

    #def assigns_room
    
