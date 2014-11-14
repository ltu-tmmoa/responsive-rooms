# Terminal Specification

The Terminal isn't strictly part of the Responsive Rooms specification, but is
required in order for a human to operate such a system. Even though the terminal
defined in this documentation is a command line application, the only strict
conformance requirement of an actual terminal is to be able to communicate with
a master process using HTTP/REST.

## Prototype Project Terminal Implementation

A terminal has to be able to participate in the human interactions outlined in
the [use cases](use_cases.md). Also, it has to be able to interace with the web
service provided by the [master processes](master.md) in order to be able to
fullfill the requirements of the use cases.
