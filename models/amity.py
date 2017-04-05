import os.path
import uuid
class Amity:
    room_capacity = 6
    def __init__(self):
        self.office_list = []
        #office_list = office_list
        self.living_space_list = []
        self.all_rooms = []
        self.living_space_dict = {}
        self.office_dict = {}
        self.all_people = []
        self.fellow_dict = {}
        self.office_occupied = {}
        self.living_space_occupied = {}
        self.staff_dict = {}
        self.person_room_dict = {}
        self.loadpeople = "persons.txt"

    def add_person(self, name, status):
        """ adds a person """
        if status == "FELLOW":
            person_id = "F" + str(hash(str(uuid.uuid1())) % 10000)
            self.fellow_dict[person_id] = name
            self.all_people.append(name)
            return "Fellow Added Successfully"
        elif status == "STAFF":
            person_id = "ST" + str(hash(str(uuid.uuid1())) % 10000)
            self.staff_dict[person_id] = name
            self.all_people.append(name)

            return "Staff Added Successfully"
        else:
            return "Staff Not Added"
    def create_room(self, **room_name):
        """ method that creates room"""
        for roomkeys, roomvalues in room_name.items():
            if roomvalues == "Office":
                self.office_dict[roomkeys] = "V"
                self.all_rooms.append(roomkeys)
                return "Office created successfully"
            elif roomvalues == "Living Space":
                self.living_space_dict[roomkeys] = "V"
                self.all_rooms.append(roomkeys)
                return "living space created successfully"

    def allocate_fellow_office(self, name, person_id):
        """ method to allocate fellow office """
        for fellowkeys, fellowvalues in self.fellow_dict.items():
            if fellowvalues == name and fellowkeys == person_id:
                if self.office_occupied.__contains__(fellowkeys):
                    return "already allocated office"
                else:
                    for officekeys, officevalues in self.office_dict.items():
                        if officevalues == "V":
                            self.office_occupied[fellowkeys] = officekeys
                            self.office_dict[officekeys] = "O"
                            return "Office assigned successfully to %s", name

    def allocate_fellow_livingspace(self, name, person_id):
        """ method to allocate fellow living space """
        for fellow_keys, fellow_values in self.fellow_dict.items():
            if fellow_values == name and fellow_keys == person_id:
                if self.living_space_occupied.__contains__(fellow_keys):
                    return "already allocated living space"
                else:
                    for living_keys, living_values in self.living_space_dict.items():
                        if living_values == "V":
                            self.living_space_occupied[fellow_keys] = living_keys
                            self.living_space_dict[living_keys] = "O"
                            return "Living Space assigned successfully to " +name

    def allocate_staff_office(self, name, person_id):
        """ method to allocate staff an office """
        for staffkeys, staffvalues in self.staff_dict.items():
            if staffvalues == name and staffkeys == person_id:
                if self.office_occupied.__contains__(staffkeys):
                    return "already allocated office"
                else:
                    for officekeys, officevalues in self.office_dict.items():
                        if officevalues == "V":
                            self.office_occupied[staffkeys] = officekeys
                            self.office_dict[officekeys] = "O"
                            return "Office assigned successfully to %s", name

    def load_people(self, filename):
        """ method to load people from a file """
        filename = self.loadpeople
        scriptpath = os.path.dirname(__file__)
        filetitle = os.path.join(scriptpath, filename)
        fileopen = open(filetitle)
        persons = fileopen.read()
        fileopen.close()
        return persons

    def print_room(self, roomname):
        """ method to print persons who have been allocated a room """
        print(roomname.upper()+"\n")
        self.fellow_dict.update(self.staff_dict)
        for keyamity, valueamity in self.fellow_dict.items():
            for keyoffice, valueoffice in self.office_occupied.items():
                if str(keyoffice) == str(keyamity) and valueoffice == roomname:
                    return valueamity+"\n"

    def print_allocations(self, filename):
        """ method to print allocations """
        self.fellow_dict.update(self.staff_dict)
        for keyamity, valueamity in self.fellow_dict.items():
            for keyoffice, valueoffice in self.office_occupied.items():
                if str(keyoffice) == str(keyamity) and filename == " ":
                    return valueoffice+"\n ----------\n"+valueamity+"\n"
                elif str(keyoffice) == str(keyamity) and filename != " ":
                    scriptpath = os.path.dirname(__file__)
                    filetitle = os.path.join(scriptpath, filename)
                    filecontent = valueoffice+"\n ----------\n"+valueamity+"\n"
                    fileopen = open(filetitle, "w+")
                    persons = fileopen.write(filecontent)
                    fileopen.close()

    def print_unallocated(self, filename):
        if filename == " ":
            self.fellow_dict.update(self.staff_dict)
            for keyAmity, valueAmity in self.fellow_dict.items():
                for keyOffice, valueOffice in self.office_occupied.items():
                    if str(keyOffice) != str(keyAmity):
                        return keyAmity+" : "+valueAmity+"\n"

    def reallocate_fellow_office(self, person_id, room_name):
        """ reallocates fellow office """
        for x, y in self.fellow_dict.items():
            if x == person_id and person_id[:1] == "F":
                for a, b in self.office_dict.items():
                    if a == room_name:
                        self.office_occupied[x] = a
                        if b == "V":
                            self.office_dict[a] = "O"
                        return y+" reallocated successfully to "+a
                        break
                break
            else:
                return "Could not reallocate fellow! Check ID and try again"
                break

    def reallocate_staff_office(self, person_id, room_name):
         """ reallocates staff office """
         for x, y in self.staff_dict.items():
             if x == person_id and person_id[:1] == "S":
                 for a, b in self.office_dict.items():
                     if a == room_name:
                         self.office_occupied[x]=a
                         if b == "V":
                             self.office_dict[a] = "O"
                     return y+" assigned successfully to "+a
                     break
                 break     
             else:
                 return "Could not reallocate Staff! Check ID and try again"
                 break
    
    def reallocate_fellow_living_space(self, person_id, room_name):
     """ reallocates fellow living space """
     for x, y in self.fellow_dict.items():
             if x == person_id and person_id[:1] == "F":
                 for a, b in self.living_space_dict.items():
                     if a == room_name:
                         self.living_space_occupied[x]=a
                         if b == "V":
                             self.living_space_dict[a] = "O"
                             
                         return y+" assigned successfully to "+a
                         break
                     break
             else:
                 
                 return "Could not reallocate Fellow! Check ID and try again"
                 break

    def save_state(self, dbname):
        pass
