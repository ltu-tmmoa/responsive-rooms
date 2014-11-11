# Actuator Specification

An actuator is a process capable of performing real-world interaction. This
document outlines the states, communications and messages an actuator is
expected to conform to in order to be part of a responsive rooms system.

## Actuator States

The actuator conceptually conforms to the below state diagram. Conformance is
not a strict requirement.

![Alt Diagram](pics/actuator_state_diagram.png)

### Registration States (Yellow)

| State    | Description                                                       |
|:---------|:------------------------------------------------------------------|
| Bind     | Binds UDP port to use when listening for master broadcasts.       |
| Listen   | Listens for master discovery broadcasts (message M).              |
| Unbind   | Removes UDP port binding.                                         |
| Wait     | Waits for some suitable time.                                     |
| Connect  | Connects to discovered master using TCP.                          |
| Register | Sends registration message to master (message AMR).               |

### Runtime States (Blue)

| State    | Description                                                       |
|:---------|:------------------------------------------------------------------|
| Schedule | Determines when to receive message and report state.              |
| Receive  | Attempts to receive (non-blocking) message from master.           |
| Action   | Carries out received action (in message A).                       |
| Update   | Updates local context data (using message ACU).                   |
| Report   | Sends curent state to master (message AR).                        |

### Error States (Red)

| State    | Description                                                       |
|:---------|:------------------------------------------------------------------|
| Unbind   | Removes UDP port binding.                                         |
| Wait     | Waits for some suitable time.                                     |

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
    |   |<-----M------|   | [M] Master Process Discovery (Broadcast UDP)
    |   |             |   |
    |   |-----SYN---->|   |
    |   |<--SYN/ACK---|   | TCP Handshake.
    |   |-----ACK---->|   |
    |   |             |   |
    |   |-----AMR---->|   | [AMR] Actuator Master Registration (TCP)
    +-+-+             +-+-+
      |                 |
      |                 |
```

| Msg.| Prt.| Port  | Description                                              |
|:---:|:---:|:-----:|:---------------------------------------------------------|
|  M  | UDP | 14000 | _Broadcast._ Master node identifier.                     |
| AMR | TCP | 14001 | Actuator type, allowed actions with parameter names*.    |

\* If a sensor has any facility, room or location data, it will send it to
   master in order to help the master in determining its locality.

### Runtime

```
+------------+    +------------+
|  Actuator  |    |   Master   |
+------------+    +------------+
      |                 |
    +-+-+             +-+-+
    |   |<----ACU-----|   | Actuator Context Update
    |   |             |   |
    |   |<-----A------|   | Action Statement
    |   |             |   |
    |   |------AR---->|   | Actuator Report
    +-+-+             +-+-+
      |                 |
      |                 |
```

| Msg.| Prt.| Port  | Description                                              |
|:---:|:---:|:-----:|:---------------------------------------------------------|
| ACU | TCP | 14001 | Facility and room identifiers, optionally locality data*.|
|  A  | TCP | 14001 | Target action and action state.                          |
|  AR | TCP | 14001 | Current action states**.                                 |

\* The message is only sent if necessary, and typically only once.

\** Actuators report at sensible intervals to its master, but at least once
every 29 seconds. An actuator failing to report for 30 seconds will be
considered `unresponsive` for another 30 seconds, after which it is forcibly
deregistered from the master. An `unresponsive` actuator succeeding to send a
report to its master before being deregistered regains normal status.

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

```
[M] Master Process Discovery
Protocol: UDP Broadcast
Port: 14000

Schema:
  message: string          # Message type identifier. Is always "M".

Example:
  { "message": "M" }
```

```
[AMR] Actuator Master Registration
Protocol: TCP Unicast
Port: 14001

Schema:
  message: string          # Message type identifier. Is always "AMR".
  type: string             # Type of actuator, eg. "door", "alarm", etc.
  actions: [               # List of available actions.
    name: string           # Name of action, eg. "open", "trigger", etc.
    parameters: [          # List of action parameters.
      :string              # Parameter name, eg. "intensity", "speed", etc.
    ]
  ]
  locality: object         # Contents of any ACU message previously received.

Example:
  {
    "message": "AMR",
    "type": "door",
    "actions": [
      {
        "name": "open",
        "parameters": [ "speed" ]
      },
      {
        "name": "close",
        "parameters": [ "speed" ]
      }
    ]
  }
```

```
[ACU] Actuator Master Registration
Protocol: TCP Unicast
Port: 14001

Schema:
  message: string          # Message type identifier. Is always "ACU".
  facility: string         # Facility identifier.
  room: string             # Room identifier.
  position:                # Optional. Position data.
    x: number
    y: number
    z: number

Example:
  {
    "message": "ACU",
    "facility": "A",
    "room": "A1202"
  }
```

```
[A] Action Statement
Protocol: TCP Unicast
Port: 14001

Schema:
  TODO

Example:
  TODO
```

```
[AR] Actuator Report
Protocol: TCP Unicast
Port: 14001

Schema:
  TODO

Example:
  TODO
```
