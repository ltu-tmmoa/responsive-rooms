# Actuator Specification

An actuator is a process capable of performing real-world interaction. This
document outlines the states, communications and messages an actuator is
expected to conform to in order to be part of a responsive rooms system.

## Actuator State Diagram

![Alt Diagram](pics/actuator_state_diagram.svg)

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
    |   |<-----M------|   | [M] Master Node Discovery (Broadcast UDP)
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
| AMR | TCP | 14001 | Actuator type, allowed actions with typed parameters*.   |

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
| SCU | TCP | 14001 | Facility and room identifiers, optionally locality data*.|
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

TODO
