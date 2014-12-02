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

__Example:__

The below example causes readings from a sensor of type "thermometer" to update
some monitor with the property "temperature".

```lua
register("thermometer", function (facility, room, sensor)
    local celcius = sensor.get("celcius")
    for _, actuator in room.getActuatorsByType("monitor")
    do
        actuator.set("temperature", celcius)
    end
end)
```

Below are the components part of the interface available when writing rules:

### The Register Function

Registers a new rule, which is a reaction to input of some category of sensor.

```lua
register( sensorType, sensorRule )
```
- `sensorType` _(string)_
  - Identifies a category of sensors, eg. "thermometer".
- `sensorRule` _(function (facility, room, sensor))_
  - A reference to a function called whenever a reading is received from a
    sensor of the registered type. The arguments given to the function
    referenced are described below.

### The Facility Object

An object passed to a sensor rule function representing all sensors and
actuators managed by the master process executing the rule.

```lua
room = facility.getRoom( identifier )
```
- `room` _Room | nil_
  - The identified room, or nil.
- `identifier` _string_
  - Room identifier.

```lua
rooms = facility.getRooms()
```
- `rooms` _Room[]_
  - All facility rooms.

### The Room Object

An object passed to a sensor rule function, representing all sensors and
actuators in a room.

```lua
actuators = facility.getActuators()
```
- `actuators` _Actuator[]_
  - All actuators in room.

```lua
actuators = facility.getActuatorsByType( type )
```
- `actuators` _Actuator[]_
  - All actuators in room having given type.
- `type` _string_
  - Actuator type identifier.

### The Actuator Object

Represents an actuator.

```lua
type = actuator.getType()
```
- `type` _string_
  - Actuator type identifier, eg. "door".

```lua
value = actuator.get( property )
```
- `value` _any_
  - The value associated with the actuator property named.
- `property` _string_
  - Property name.

```lua
actuator.set( property, value )
```
- `property` _string_
  - Name of property to set.
- `value` _any_
  - Property value.

```lua
room = actuator.getRoom()
```
- `room` _Room_
  - The room in which the actuator is located.

### The Sensor Object

Represents a sensor.

```lua
type = sensor.getType()
```
- `type` _string_
  - Sensor type identifier, eg. "proximity_sensor".

```lua
value = sensor.get( property )
```
- `value` _any_

  - The value associated with the sensor property named.
- `property` _string_
  - Property name.

```lua
room = sensor.getRoom()
```
- `room` _Room_
  - The room in which the sensor is located.

## Rule Management

A master allows management of its rules, each rule being part of a program, by
exposing them as a [REST](http://www.ics.uci.edu/~fielding/pubs/dissertation/rest_arch_style.htmweb)ful
service on __port 14003__.

The API provided by the specification is currently not aimed at completeness,
but rather to allow for the construction of a working prototype.

### The Sensor Collection

#### GET /sensors

Acquires data about all resources, or a filtered subset of them.

__Request:__

    GET /sensors<query>
    Accept: application/json

`<query>` is optionally the a query parameter on the form `?room=<room>`, where
`<room>` is a room identifier or `null`.

__Response:__

    HTTP/1.1 200 OK
    Content-Type: application/json
    Collection-Items: <names>

    <body>

`<names>` is a comma separated list of all sensor identifiers.

`<body>` is the JSON payload containing information about all sensors.

### The Sensor Resource

#### PUT /sensors/:id/room

Assigns identified sensor to some given room.

__Request:__

    PUT /sensors/<id>/room
    Content-Type: text/plain
    Content-Length: <length>

    <room>

`<id>` is a sensor identifier.

`<length>` is the size of `<room>` in bytes.

`<room>` is the room in which to put the sensor. If `<room>` is empty, the
sensor is removed from its current room.

__Response:__

    HTTP/1.1 204 NO CONTENT

__Response if the identified sensor doesn't exist:__

    HTTP/1.1 404 NOT FOUND

### The Actuator Collection

This corresponds exactly to the Sensor Collection, but with the difference that
the word `sensor` is substituted for `actuator` in all cases.

### The Actuator Resource

This corresponds to the Sensor Resource, but with the difference that the word
`sensor` is substituted for `actuator` in all cases.

### The Program Collection

#### HEAD /programs

Acquires names all programs owned by master.

__Request:__

    HEAD /programs
    Accept: application/lua

__Response:__

    HTTP/1.1 200 OK
    Content-Type: application/lua
    Collection-Items: <names>

`<names>` is a comma separated list of program names.

#### POST /programs

Adds a new program to master.

__Request:__

    POST /programs
    Accept: text/plain
    Content-Type: application/lua
    Collection-Item: <name>

    <program>

`<name>` is the name of the program being added. `<program>` is the program
source code.

__Response:__

    HTTP/1.1 201 CREATED
    Content-Type: text/plain
    Location: <location>

    <name>

`<location>` is the URL at which the new program now is available. `<name>`is
the name of the added program.

__Response if program name is missing in header:__

    HTTP/1.1 400 BAD REQUEST
    Content-Type: text/plain

    No program name given in message header.

__Response if a program with given name already exists:__

    HTTP/1.1 403 FORBIDDEN
    Content-Type: text/plain

    A program with that name already exists.

### The Program Resource

#### GET /programs/:name

Acquires program with given name, eg. `thermometer_alarm.lua`.

__Request:__

    GET /programs/<name>
    Accept: application/lua

`<name>`is the name of the requested program.

__Response:__

    HTTP/1.1 200 OK
    Content-Type: application/lua
    Collection-Item: <name>

    <program>

`<name>` is the name of the requested program. `<program>` is the program
source code.

__Response if program does not exist:__

    HTTP/1.1 404 NOT FOUND

#### DELETE /programs/:name

Removes identified program from master.

__Request:__

    DELETE /programs/<name>

`<name>`is the name of the program  to be deleted.

__Response:__

    HTTP/1.1 204 NO CONTENT
    Collection-Item: <name>

`<name>` is the name of the deleted program.

__Response if attempting to delete non-existing program:__

    HTTP/1.1 204 NO CONTENT
    Collection-Item: <name>

`<name>` is the name of the program requested to be deleted, even if it didn't
exist.
