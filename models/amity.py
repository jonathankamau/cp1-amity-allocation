import os.path
class Amity:
    room_capacity = 6
    def __init__(self):
        self.office_list = []
        #office_list = office_list
        self.living_space_list = []
        self.all_rooms = []
        self.living_space_dict = {"Kenya":"O", "Uganda":"V"}
        self.office_dict = {"Hogwarts":"O", "Bootcamp":"V", "Vienna":"O", "Valhalla":"V"}
        self.all_people = []
        self.fellow_dict = {"F002":"Alex", "F003":"John", "F005":"Terry", "F006":"Fred"}
        self.office_occupied = {"F002": "Hogwarts", "ST002":"Vienna", "F006":"Valhalla",
                                "F018":"Hogwarts", "F023":"Hogwarts", "F024":"Hogwarts",
                                "F025":"Hogwarts", "F026":"Hogwarts", "F027":"Hogwarts"}
        self.living_space_occupied = {"F005":"Kenya", "F009":"Kenya",
                                      "F010":"Kenya", "F013":"Kenya", "F019":"Kenya"}
        self.staff_dict = {"ST001":"Musa", "ST002":"Hellen"}
        self.person_room_dict = {3:"Machakos", 5:"Kisumu"}
        self.loadpeople = "persons.txt"

    def add_person(self, name, status):
        """ adds a person """
        if status == "FELLOW":
            person_id = "FOO4"
            self.fellow_dict[person_id] = name
            self.all_people.append(name)
            #return "Fellow Added Successfully"
            return
        else:
            person_id = "ST003"
            self.staff_dict[person_id] = name
            self.all_people.append(name)

            #return "Staff Added Successfully"
            return
    def create_room(self, room_name, room_type):
        """ creates room"""
        if room_type == "Office":
            self.office_dict[room_name] = "V"
            self.all_rooms.append(room_name)
            #return "Office created successfully"
            return
        elif room_type == "Living Space":
            self.living_space_dict[room_name] = "V"
            self.all_rooms.append(room_name)
            #return "living space created successfully"
            return
    def allocate_fellow_office(self, name, person_id):
        for x, y in self.fellow_dict.items():
             if y == name and x == person_id:
                 if self.office_occupied.__contains__(x):
                     #return "already allocated office"
                     return
                 else:
                     for a, b in self.office_dict.items():
                         if b =="V":
                             self.office_occupied[x]=a
                             self.office_dict[a]="O"
                             #return "Office assigned successfully to %s", name
                             return
    def allocate_fellow_livingspace(self, name, person_id):
        for x, y in self.fellow_dict.items():
             if y == name and x == id:
                 if self.living_space_occupied.__contains__(x):
                     #return "already allocated living space"
                     return
                 else:
                     for a, b in self.living_space_dict.items():
                         if b =="V":
                             self.living_space_occupied[x]=a
                             self.living_space_dict[a]="O"
                             #return "Living Space assigned successfully to " +name
                             return

    def allocate_staff_office(self, name, person_id):
        for x, y in self.staff_dict.items():
             if y == name and x == id:
                 if self.office_occupied.__contains__(x):
                     #return "already allocated office"
                     return
                 else:
                     for a, b in self.office_dict.items():
                         if b =="V":
                             self.office_occupied[x]=a
                             self.office_dict[a]="O"
                             #return "Office assigned successfully to %s", name
                             return

    def load_people(self, filename):
        filename = self.loadpeople
        scriptpath = os.path.dirname(__file__)
        filetitle = os.path.join(scriptpath, filename)
        fileopen = open(filetitle)
        persons = fileopen.read()
        fileopen.close()
        return persons

    def print_room(self, roomname):
        return roomname.upper()+"\n"
        fellow_dict.update(staff_dict)
        for keyAmity, valueAmity in fellow_dict.items():
            for keyOffice, valueOffice in office_occupied.items():
                if str(keyOffice) == str(keyAmity) and valueOffice == roomname:
                    return valueAmity+"\n"
    
    def print_allocations(self, filename):
        if filename == " ":
            self.fellow_dict.update(self.staff_dict)
            for keyAmity, valueAmity in self.fellow_dict.items():
                for keyOffice, valueOffice in self.office_occupied.items():
                    if str(keyOffice) == str(keyAmity):
                        return valueOffice+"\n ----------\n"+valueAmity+"\n"

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
                        #return y+" reallocated successfully to "+a
                        return
                        break
                break
            else:
                #return "Could not reallocate fellow! Check ID and try again"
                return
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
                     #return y+" assigned successfully to "+a
                     return
                     break
                 break     
             else:
                 return
                 #return "Could not reallocate Staff! Check ID and try again"
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
                             return
                         #return y+" assigned successfully to "+a
                         break
                     break
             else:
                 return
                 #return "Could not reallocate Fellow! Check ID and try again"
                 break
