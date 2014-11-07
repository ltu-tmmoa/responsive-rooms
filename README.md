responsive-rooms
================

LTU Project: Responsive Rooms (Pervasive Computing)

By connecting sensors and actuators, physical rooms may be made to respond to human interaction or other events. Temperature may regulate lighting, radiation level effect hazard level, motion may trigger audio messages, etc.

The core of the Responsive Rooms project is to create a system defined in terms of communicating processes, all with one of the three roles Sensor, Actuator, or Master. Communication is made using a higher-level protocol which make the system agnostic to the actual types of sensors and actuators. Sensor and actuator processes are responsible for the communication with the concrete physical sensors and acturators, which omits the need for the master process to know of any particular hardware.
