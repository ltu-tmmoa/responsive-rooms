# Actuator Specification

An actuator is a process capable of performing real-world interaction. This
document outlines the states, communications and messages an actuator is
expected to conform to in order to be part of a responsive rooms system.

## Actuator States

![Diagram](pics/actuator_state_diagram.png)

### Registration States (Yellow)

| State    | Description                                                       |
|:---------|:------------------------------------------------------------------|
| Bind     | Binds UDP port to use when listening for master broadcasts.       |
| Listen   | Listens for master discovery broadcasts (message MD).             |
| Unbind   | Removes UDP port binding.                                         |
| Connect  | Connects to discovered master using TCP.                          |
| Register | Sends registration message to master (message AM).                |

### Runtime States (Blue)

| State    | Description                                                       |
|:---------|:------------------------------------------------------------------|
| Schedule | Determines when to receive message and report state.              |
| Receive  | Attempts to receive (non-blocking) message from master.           |
| Action   | Carries out received action (in message AU).                      |
| Update   | Updates local context data (using message CU).                    |
| Report   | Sends curent state to master (message AR).                        |

### Error States (Red)

| State    | Description                                                       |
|:---------|:------------------------------------------------------------------|
| Unbind   | Removes UDP port binding.                                         |
| Wait     | Waits for some suitable time.                                     |
| Invalid  | Received message that is invalid or of unknown type.              |
| Rep. Er. | Reports to master about received message error (message ER).      |

## Actuator/Master Communication

An actuator may be connected to one, and only one, master process, which may
change and query its state.

### Registration

```
+------------+    +------------+
|  Actuator  |    |   Master   |
+------------+    +------------+
      |                 |
    +-+-+             +-+-+
    |   |<-----MD-----|   | Master Process Discovery (UDP Broadcast)
    |   |             |   |
    |   |-----SYN---->|   |
    |   |<--SYN/ACK---|   | TCP Handshake.
    |   |-----ACK---->|   |
    |   |             |   |
    |   |------AM---->|   | Actuator Master Registration*
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
|  Actuator  |    |   Master   |
+------------+    +------------+
      |                 |
    +-+-+             +-+-+
    |   |<-----CU-----|   | Context Update*
    |   |             |   |
    |   |<-----AU-----|   | Actuator State Update
    |   |             |   |
    |   |------AR---->|   | Actuator Report**
    |   |             |   |
    |   |------ER---->|   | Error Report
    +-+-+             +-+-+
      |                 |
      |                 |
```

\* The message is only sent if necessary, and typically only once.

\** Actuators report at sensible intervals to its master, but at least once
every 29 seconds. An actuator failing to report for 30 seconds will be
considered `unresponsive` for another 30 seconds, after which it is forcibly
de-registered from its master. An `unresponsive` actuator succeeding to send a
report to its master before being de-registered regains normal status.

### De-registration

De-registration occurs by either party terminating the TCP session.

```
+------------+    +------------+
|  Actuator  |    |   Master   |
+------------+    +------------+
      |                 |
    +-+-+             +-+-+
    |   |<----FIN-----|   |
    |   |---FIN/ACK-->|   | TCP Finalization Handshake.
    |   |<----ACK-----|   |
    +-+-+             +-+-+
      |                 |
      X                 X
```

## Actuator/Master Message Protocol

The below list contains all messages relevant to the actuator.

| Msg.| Prt.| Port  | Description                                              |
|:---:|:---:|:-----:|:---------------------------------------------------------|
| MD  | UDP | 14000 | _Broadcast._ Master node identifier.                     |
| AM  | TCP | 14001 | Actuator type, allowed actions with parameter names.     |
| CU  | TCP | 14001 | Facility and room identifiers.                           |
| AU  | TCP | 14001 | Target property and state.                               |
| AR  | TCP | 14001 | Current actuator state.                                  |
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

#### [AM] Actuator Master Registration
```
Schema:
  {
    "message": "AM",         # Message type identifier. Is always "AM".
    "type": "<type>",        # Type of actuator, eg. "door", "alarm", etc.
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
    "message": "AM",
    "type": "door",
    "properties": {
      "open": "boolean"
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

#### [AU] Actuator State Update
```
Schema:
  {
    "message": "AU",         # Message type identifier. Is always "AU".
    "properties": {
      "<name>": <value>,     # Name and property value of relevant type.
      ...                    # May contain any amount of relevant properties*.
    }
  }
```

\* Existing properties not included do not have their state changed.

```
Example:
  {
    "message": "AU",
    "properties": {
      "open": false
    }
  }
```

#### [AR] Actuator Report
```
Schema:
  {
    "message": "AR",         # Message type identifier. Is always "AR".
    "properties": {
      "<name>": <value>,     # Name and property value of relevant type.
      ...                    # May contain any amount of relevant properties.
    }
  }
```

```
Example:
  {
    "message": "AR",
    "properties": {
      "open": true
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
