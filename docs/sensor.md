# Sensor Specification

A sensor is a process able to query its environment for data. This document
outlines the states, communications and messages a sensor is expected to conform
to in order to be part of a responsive rooms system.

## Sensor State Diagram

![Diagram](pics/sensor_state_diagram.png)

### Registration States (Yellow)

| State    | Description                                                       |
|:---------|:------------------------------------------------------------------|
| Bind     | Binds UDP port to use when listening for master broadcasts.       |
| Listen   | Listens for master discovery broadcasts (message M).              |
| Unbind   | Removes UDP port binding.                                         |
| Connect  | Connects to discovered master using TCP.                          |
| Register | Sends registration message to master (message SMR).               |

### Runtime States (Blue)

| State    | Description                                                       |
|:---------|:------------------------------------------------------------------|
| Schedule | Determines when to receive message and report state.              |
| Receive  | Attempts to receive (non-blocking) message from master.           |
| Update   | Updates local context data (using message CU).                    |
| Report   | Sends curent state to master (message SR).                        |

### Error States (Red)

| State    | Description                                                       |
|:---------|:------------------------------------------------------------------|
| Unbind   | Removes UDP port binding.                                         |
| Wait     | Waits for some suitable time.                                     |
| Invalid  | Received message that is invalid or of unknown type.              |
| Rep. Er. | Reports to master about received message error (message ER).      |

## Sensor/Master Communication

A sensor may be connected to one, and only one, master process, which may query
its state.

### Registration

```
+------------+    +------------+
|   Sensor   |    |   Master   |
+------------+    +------------+
      |                 |
    +-+-+             +-+-+
    |   |<-----MD-----|   | Master Process Discovery (UDP Broadcast)
    |   |             |   |
    |   |-----SYN---->|   |
    |   |<--SYN/ACK---|   | TCP Handshake
    |   |-----ACK---->|   |
    |   |             |   |
    |   |------SM---->|   | Sensor Master Registration*
    +-+-+             +-+-+
      |                 |
      |                 |
```

\* If a sensor has any facility, room or location data, it will send it to
   master in order to help the master in determining its locality.

### Runtime

Runtime messages are not expected to be sent or received in any particular
order. The diagram below is to be considered an example.

```
+------------+    +------------+
|   Sensor   |    |   Master   |
+------------+    +------------+
      |                 |
    +-+-+             +-+-+
    |   |<-----CU-----|   | Context Update*
    |   |             |   |
    |   |------SR---->|   | Sensor Report**
    |   |             |   |
    |   |------ER---->|   | Error Report
    +-+-+             +-+-+
      |                 |
      |                 |
```

\* The message is only sent if necessary, and typically only once.

\** Sensors report at sensible intervals to its master, but at least once every
29 seconds. A sensor failing to report for 30 seconds will be considered
`unresponsive` for another 30 seconds, after which it is forcibly deregistered
from its master. An `unresponsive` sensor succeeding to send a report to its
master before being deregistered regains normal status.

### De-registration

De-registration occurs by either party terminating the TCP session.

```
+------------+    +------------+
|   Sensor   |    |   Master   |
+------------+    +------------+
      |                 |
    +-+-+             +-+-+
    |   |<----FIN-----|   |
    |   |---FIN/ACK-->|   | TCP Finalization Handshake
    |   |<----ACK-----|   |
    +-+-+             +-+-+
      |                 |
      X                 X
```

## Sensor/Master Message Protocol

The below list contains all messages relevant to the sensor.

| Msg.| Prt.| Port  | Description                                              |
|:---:|:---:|:-----:|:---------------------------------------------------------|
| MD  | UDP | 14000 | _Broadcast._ Master node identifier.                     |
| SR  | TCP | 14001 | Sensor type, reported properties with types.             |
| CU  | TCP | 14001 | Facility and room identifiers.                           |
| SR  | TCP | 14001 | Current actuator state.                                  |
| ER  | TCP | 14001 | Message error report.                                    |

### Message Schemata

All messages strictly conform to the [JSON](http://www.json.org) specification.
The root structure is always an object.

#### [MD] Master Process Discovery
```
Schema:
  { "message": "MD" }        # Message type identifier. Is always "MD".
```
```
Example:
  { "message": "MD" }
```

#### [SM] Sensor Master Registration
```
Schema:
  {
    "message": "SM",         # Message type identifier. Is always "SM".
    "type": "<type>",        # Type of sensor, eg. "thermometer", "lock", etc.
    "properties": {
      "<name>": "<type>",    # Name and property type*.
      ...                    # May contain any amount of properties.
    },
    "context": {<context>}   # Data of CU message previously received, or null.
  }
```

\* A property type may be one of "boolean", "integer", "number", "string",
   "array" or "object".

```
Example:
  {
    "message": "SM",
    "type": "thermometer",
    "properties": {
      "celcius": "number",
      "fahrenheit": "number"
    },
    "context": null
  }
```

#### [CU] Context Update
```
Schema:
  {
    "message": "CU",         # Message type identifier. Is always "CU".
    "facility": "<name>",    # Facility identifier.
    "room": "<name>"         # Room identifier.
    "location": {            # Optional. Absolute coordinates.
      "x": <x>,
      "y": <y>,
      "z": <z>
    }
  }
```

```
Example:
  {
    "message": "CU",
    "facility": "A",
    "room": "1202",
    "location": {
      "x": 4.5,
      "y": 1.9,
      "z": 6.2
    }
  }
```

#### [SR] Sensor Report
```
Schema:
  {
    "message": "SR",         # Message type identifier. Is always "SR".
    "properties": {
      "<name>": <value>,     # Name and property value of relevant type.
      ...                    # May contain any amount of relevant properties.
    }
  }
```

```
Example:
  {
    "message": "SR",
    "properties": {
      "celcius": 81.239,
      "fahrenheit": 178.23
    }
  }
```

#### [ER] Error Report
```
Schema:
  {
    "message": "ER",         # Message type identifier. Is always "ER".
    "error": "<description>" # A text describing relevant error.
  }
```

````
Example:
  {
    "message": "ER",
    "error": "Unrecognized property 'openp'."
  }
```
