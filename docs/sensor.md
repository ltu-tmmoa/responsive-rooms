# Sensor Specification

A sensor is a process able to query its environment for data. This document
outlines the states, communications and messages a sensor is expected to conform
to in order to be part of a responsive rooms system.

## Sensor State Diagram

```
TODO
```

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
    |   |<-----M------|   | Master Discovery Broadcast
    |   |             |   |
    |   |-----SYN---->|   |
    |   |<--SYN/ACK---|   | TCP Handshake
    |   |-----ACK---->|   |
    |   |             |   |
    |   |-----SMR---->|   | Sensor Master Registration
    +-+-+             +-+-+
      |                 |
      |                 |
```

| Msg.| Prt.| Port  | Description                                              |
|:---:|:---:|:-----:|:---------------------------------------------------------|
|  M  | UDP | 14000 | _Broadcast._ Master node identifier.                     |
| SMR | TCP | 14001 | Sensor type, names of reported data, location data*.     |

\* If a sensor has any facility, room or location data, it will send it to
   master in order to help the master in determining its locality.

### Runtime

```
+------------+    +------------+
|   Sensor   |    |   Master   |
+------------+    +------------+
      |                 |
    +-+-+             +-+-+
    |   |<----SCU-----|   | Sensor Context Update
    |   |             |   |
    |   |------SR---->|   | Sensor Report
    +-+-+             +-+-+
      |                 |
      |                 |
```

| Msg.| Prt.| Port  | Description                                              |
|:---:|:---:|:-----:|:---------------------------------------------------------|
| SCU | TCP | 14001 | Facility and room identifiers, optionally locality data*.|
|  SR | TCP | 14001 | Contains reports about sensor state**.                   |

\* The message is only sent if necessary, and typically only once.

\** Sensors report at sensible intervals to its master, but at least once every
29 seconds. A sensor failing to report for 30 seconds will be considered
`unresponsive` for another 30 seconds, after which it is forcibly deregistered
from the master. An `unresponsive` sensor succeeding to send a report to its
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

TODO
