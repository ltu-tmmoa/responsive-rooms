# Use Cases for Responsive Rooms System

This document outlines how a human operator could go about in installing sensors
and actuators, and having these inter-operate through the use of a programs kept
by a master node.

## Sensor Use Cases

### Installing a New Sensor
| # | Actor    | Action                                                        |
|:-:|:---------|:--------------------------------------------------------------|
| 1 | Human    | Turns on and connects sensor hardware to network router.      |
| 2 | Human    | Types `list sensor unassigned` in a Responsive Rooms terminal.|
| 3 | Terminal | Prints data about the connected sensor.                       |

### Assigning Sensor to Room
| # | Actor    | Action                                                        |
|:-:|:---------|:--------------------------------------------------------------|
| 1 | Human    | Types `list sensor unassigned` in a Responsive Rooms terminal.|
| 2 | Terminal | Prints data about unassigned connected sensors, including IDs.|
| 3 | Human    | Types `sensor assign <ID> <room>` in terminal.                |
| 4 | Terminal | Prints confirmation about sensor being assigned to given room.|

### Unassigning Sensor from Room
| # | Actor    | Action                                                        |
|:-:|:---------|:--------------------------------------------------------------|
| 1 | Human    | Types `sensor unassign <ID>` in a Responsive Rooms terminal.  |
| 2 | Terminal | Prints confirmation about sensor being unassigned from room.  |

### Discovering Unresponsive Sensors
| # | Actor    | Action                                                        |
|:-:|:---------|:--------------------------------------------------------------|
| 1 | Human    | Types `list sensor unresponsive` in a terminal.               |
| 2 | Terminal | Prints data about unresponsive sensors.                       |

### Listing All Sensors
| # | Actor    | Action                                                        |
|:-:|:---------|:--------------------------------------------------------------|
| 1 | Human    | Types `list sensor` in a terminal.                            |
| 2 | Terminal | Prints data about all sensors.                                |

### Listing Sensors by Room
| # | Actor    | Action                                                        |
|:-:|:---------|:--------------------------------------------------------------|
| 1 | Human    | Types `list sensor room <room>` in a terminal.                |
| 2 | Terminal | Prints data about sensors in given room.                      |

## Actuator Use Cases

The use cases for actuators are identical to those of sensors, with the
difference that the word `actuator` is used in place of `sensor` in all
relevant terminal commands.

## Programming Use Cases

### Adding a New Program
| # | Actor    | Action                                                        |
|:-:|:---------|:--------------------------------------------------------------|
| 1 | Human    | Types `program add <path-to-local-program>`* in a terminal.   |
| 2 | Terminal | Prints program add confirmation, including program name.      |

\* The program is expected to be a file on the computer using the terminal,
  relative to its current working directory.

### Listing Existing Programs
| # | Actor    | Action                                                        |
|:-:|:---------|:--------------------------------------------------------------|
| 1 | Human    | Types `list program` in a terminal.                           |
| 2 | Terminal | Prints a list of existing programs.                           |

### Removing Existing Program
| # | Actor    | Action                                                        |
|:-:|:---------|:--------------------------------------------------------------|
| 1 | Human    | Types `program remove <name>` in a terminal.                  |
| 2 | Terminal | Prints a confirmation about program being removed.            |

## Example Use Cases

### Making A Room Temperature of 200C Fire an Alarm
| # | Actor    | Action                                                        |
|:-:|:---------|:--------------------------------------------------------------|
| 1 | Human    | Turns on and connects temperature sensor and alarm to router. |
| 2 | Human    | Types `list sensor unassigned` in a terminal.                 |
| 3 | Terminal | Prints data about sensor, including type `temp` and ID `123`. |
| 4 | Human    | Types `sensor assign 123 room_a`.                             |
| 5 | Terminal | Confirms sensor `123` being added to room `room_a`.           |
| 6 | Human    | Types `list actuator unassigned` in terminal.                 |
| 7 | Terminal | Prints data about actuator, including type `alarm` and ID `4`.|
| 8 | Human    | Types `actuator assign 4 room_a`.                             |
| 9 | Terminal | Confirms actuator `4` being added to room `room_a`.           |
|10 | Human    | Types `program add temp_alarm.lua`* in terminal.              |
|11 | Terminal | Confirms `temp_alarm.lua` being added.                        |

\* The program `temp_alarm.lua` could have something like the following
   contents:

```lua
register("thermometer", function (facility, room, sensor)
  local isTriggered = sensor.get("celcius") > 200;
  for _, alarm in room.getActuatorsByType("alarm")
  do
    alarm.set("triggered", isTriggered)
  end
end)
```
