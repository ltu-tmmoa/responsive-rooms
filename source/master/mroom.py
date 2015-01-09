
all_rooms = {}
all_facilities = {}

class Facility:
	def __init__(self, identifier):
		self._id = identifier
		self._rooms = {}
	def getRoom(self, identifier):
		if identifier in self._rooms:
			return self._rooms[identifier]
		else:
			return None
	def getRooms(self):
		return self._rooms.values()

class Room:
	def __init__(self, identifier):
		self._id = identifier
		self._actuators = set()
	def getActuators(self):
		return [actuator for actuator in self._actuators]
	def getActuatorsByType(self, actuator_type):
		return [actuator for actuator in self._actuators if actuator.getType() == actuator_type]

def get_room(room_id):
	if room_id not in all_rooms:
		all_rooms[room_id] = Room(room_id)
	return all_rooms[room_id]
	
def put_actuator_in_room(actuator, room_id):
	if room_id and room_id not in all_rooms:
		all_rooms[room_id] = Room(room_id)
	for facility in all_facilities.values():
		for room in facility._rooms.values():
			room._actuators.discard(actuator)
	if room_id:
		all_rooms[room_id]._actuators.add(actuator)

def put_room_in_facility(room_id, facility_id):
	if facility_id not in all_facilities:
		all_facilities[facility_id] = Facility(facility_id)
	if room_id not in all_rooms:
		all_rooms[room_id] = Room(room_id)
	for facility in all_facilities.values():
		if room_id in facility._rooms:
			facility._rooms.pop(room_id)
	all_facilities[facility_id]._rooms[room_id] = all_rooms[room_id]

def get_facility_of_room(room):
	if room:
		for facility in all_facilities.values():
			if room in facility._rooms.values():
				return facility
	return None

def get_facility_id_of_room_id(room_id):
	for facility in all_facilities.values():
		for room in facility._rooms.values():
			if room._id == room_id:
				return facility._id
	return None

put_room_in_facility('A117', 'ABuilding')
put_room_in_facility('A1513', 'ABuilding')
put_room_in_facility('A2526', 'ABuilding')
put_room_in_facility('C120', 'CBuilding')
put_room_in_facility('C200', 'CBuilding')
put_room_in_facility('C1515', 'CBuilding')
