class Room(object):
    def __init__(self, room_name, room_type, max_capacity):
        self.room_name = room_name
        self.room_type = room_type
        self.max_capacity = max_capacity
        self.allocations = []

class Office(Room):
    def __init__(self, room_name):
        super(Office, self).__init__(room_name, room_type="Office", max_capacity=6)
        self.room_id = id(room_name)
        self.occupancy = 0
        self.allocations = []

class LivingSpace(Room):
    def __init__(self, room_name):
        super(LivingSpace, self).__init__(room_name, room_type="LivingSpace", max_capacity=4)
        self.room_id = id(room_name)
        self.occupancy = 0
        self.allocations = []








