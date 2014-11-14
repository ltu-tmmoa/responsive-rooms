# Responsive Rooms

LTU Project: Responsive Rooms (Pervasive Computing)

## Introduction

By connecting sensors and actuators, physical rooms may be made to respond to
human interaction or other events. Temperature may regulate lighting, radiation
level effect hazard level, motion may trigger audio messages, etc.

The core of the Responsive Rooms project is to create a system defined in terms
of communicating processes, all with one of the three roles __sensor__,
__actuator__, or __master__. Communication is made using a higher-level protocol
which make the system agnostic to the actual types of sensors and actuators
involved. A human operator may upload rules to the master which allows it to
govern the behavior of the actuators in response to sensor readings.

## Documentation

| Section                        | Description                                 |
|:-------------------------------|:--------------------------------------------|
| [Use Cases](docs/use_cases.md) | Outlines human system interaction.          |
| [Sensor](docs/sensor.md)       | Senses its environment.                     |
| [Actuator](docs/actuator.md)   | Interacts with its environment.             |
| [Master](docs/master.md)       | Governs actuators using sensors and rules.  |
| [Terminal](docs/terminal.md)   | Allows a human to organize a system.        |
