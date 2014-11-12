# Master Specification

The master process keeps track of an arbitrary amount of sensor and actuator
processes. It receives readings from the sensors, and makes the actuators
perform actions in relation to rules known by the master process.

## Pre-conditions

A master process is expected to be able to participate in the communications
outlined in the [actuator](actuator.md) and [sensor](sensor.md) sections.

## Rule Expression

Rules are written in the [Lua](http://www.lua.org) language, which gives room
for arbitrary complexity in defining sensor-actuator interoperability, and are
defined as responses to sensor input.

Do note that the current API does not aim to be feature complete. The
specification is currently aimed at providing the functionality required to
create a working system prototype.

Example:

TODO

Below are the components part of the interface available when writing rules:

### The Register Function

Registers a new rule, which is a reaction to input of some category of sensor.

__register( sensorType, sensorRule )__
- `sensorType` _(string)_
  - Identifies a category of sensors, eg. "thermometer".
- `sensorRule` _(function (facility, room, sensor))_
  - A reference to a function called whenever a reading is received from a
    sensor of the registered type. The arguments given to the function
    referenced are described below.

### The Facility Object

An object passed to a sensor rule function representing all sensors and
actuators managed by the master process executing the rule.

__room = facility.getRoom( identifier )__
- `room` _Room | nil_
  - The identified room, or nil.
- `identifier` _string_
  - Room identifier.

__rooms = facility.getRooms()__
- `rooms` _Room[]_
  - All facility rooms.

### The Room Object

An object passed to a sensor rule function, representing all sensors and
actuators in a room.

__actuators = facility.getActuators()__
- `actuators` _Actuator[]_
  - All actuators in room.

__actuators = facility.getActuatorsByType( type )__
- `actuators` _Actuator[]_
  - All actuators in room having given type.
- `type` _string_
  - Actuator type identifier.

### The Actuator Object

TODO

### The Sensor Object

TODO

## Rule Management

TODO
