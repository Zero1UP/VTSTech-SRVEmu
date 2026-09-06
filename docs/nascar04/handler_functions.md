# LobbyApi Command Handler Functions

This document catalogs the specific command handler functions called from LobbyApiUpdate (0x0031bdf0).

## Handler Functions Called from LobbyApiUpdate

### String/Buffer Functions

| Address | Function | Purpose |
|---------|----------|---------|
| 0x31ddd0 | strcmp/scan | String comparison and scanning |
| 0x31e8b0 | parse_number | Parse ASCII digits to integer |
| 0x31e988 | parse_number | Parse number with validation |
| 0x31e520 | - | Unknown |
| 0x31e1e0 | - | Unknown |

### Message/Response Functions

| Address | Function | Purpose |
|---------|----------|---------|
| 0x31af10 | send_response | Sends formatted response back to client |
| 0x31abd0 | format_message | Formats message with parameters |
| 0x31bdd0 | LobbyApiUpdate | Main entry (thunk) |

### Network/Protocol Functions

| Address | Function | Purpose |
|---------|----------|---------|
| 0x31a628 | Network_Callback | Network state callback handler |
| 0x31a760 | Network_Process | Network data processing |
| 0x322190 | Protocol_Parse | Parse protocol message |
| 0x322040 | Protocol_Encode | Encode protocol message |
| 0x322608 | Protocol_Init | Initialize protocol state |

### Room/Lobby Functions

| Address | Function | Purpose |
|---------|----------|---------|
| 0x31ed10 | Room_Update | Update room state |
| 0x31ef10 | - | Unknown |
| 0x31f328 | - | Unknown |
| 0x31f948 | - | Unknown |

## Handler Function Analysis

### 0x31ddd0 - String Handler
```
Purpose: String comparison and buffer scanning
Input: Two string pointers
Output: Comparison result
Called from: Multiple locations in LobbyApiUpdate
```

### 0x31e8b0 - Number Parser
```
Purpose: Parse ASCII digits to integer
Input: String pointer
Output: Parsed integer value
Logic:
  - Handles '+' (0x2b) and '-' (0x2d) prefixes
  - Converts ASCII '0'-'9' to numeric value
  - Returns parsed integer
Used for: Parsing numeric values in protocol messages
```

### 0x31e988 - Number Parser (Extended)
```
Purpose: Parse number with bounds checking
Input: String pointer, max value
Output: Parsed integer (limited to 16-bit)
Logic:
  - Similar to 0x31e8b0
  - Masks result with 0xFFFF
  - Checks for decimal point '.'
Used for: Parsing user IDs, room IDs, etc.
```

### 0x31af10 - Response Sender
```
Purpose: Send formatted response to client
Input: Context, format string, parameters
Logic:
  - Loads "term" command (0x7465726d)
  - Stores in message buffer
  - Calls lower-level send function
  - Handles response callback
```

### 0x31abd0 - Message Formatter
```
Purpose: Format protocol messages
Input: Context, message type, parameters
Output: Formatted message buffer
Functions called:
  - 0x31ddd0 (string ops)
  - 0x31e988 (parse number)
  - 0x31ed10 (room update)
  - 0x31a898 (network send)
```

## Call Flow

```
LobbyApiUpdate (0x31bdf0)
    |
    +---> Command validation
    |         |
    |         +---> 0x31e8b0 (parse number)
    |         +---> 0x31e988 (parse number)
    |         +---> 0x31ddd0 (string compare)
    |
    +---> Handler execution
    |         |
    |         +---> 0x31a760 (network process)
    |         +---> 0x31af10 (send response)
    |         +---> 0x31ed10 (room update)
    |
    +---> Message formatting
                |
                +---> 0x31abd0 (format message)
                      |
                      +---> 0x31a898 (send to client)
```

## Key Observations

1. **0x31e8b0 and 0x31e988** are used for parsing numeric values from protocol messages
   - Used to extract user IDs, room IDs, etc.
   - Handle ASCII digit conversion

2. **0x31af10** is a common response handler
   - Builds "term" response messages
   - Called at end of many command handlers

3. **0x31abd0** is a complex formatter
   - Handles multiple parameter types
   - Coordinates with room and network systems

4. **0x31a628** handles network callbacks
   - Called when network state changes
   - Triggers appropriate protocol actions

## See Also

- `/analysis/decompiled/BuddyApiUpdate.c` - BuddyApi protocol handler
- `/analysis/decompiled/NetworkEvent_MainDispatcher.c` - Network event routing
- `/docs/master_command_list.md` - Complete command inventory

## ProtoAries Protocol Layer

The ProtoAries functions handle the low-level network communication:

### ProtoAriesConnect
```
Purpose: Establish connection to server
Input: IP address, port, connection context
Logic:
  - Initializes connection structure
  - Calls RpcBind with "sess" and "conn" (0x73657373, 0x636f6e6e)
  - Calls RpcCall to initiate connection
  - Returns status
```

### ProtoAriesPeek
```
Purpose: Check for incoming data without consuming
Input: Connection context, pointers for output
Output: Message type, flags, length, payload pointer
Logic:
  - Checks if data is available in buffer
  - Extracts header (type, flags, length) from big-endian format
  - Returns -1 if no data, otherwise returns message info
Wire Format:
  Offset 0x00: Message Type (4 bytes BE)
  Offset 0x04: Flags (4 bytes BE)
  Offset 0x08: Length (4 bytes BE)
  Offset 0x0C: Payload
```

### ProtoAriesSend
```
Purpose: Send data to server
```

### ProtoAriesRecv
```
Purpose: Receive data from server
```

### ProtoAriesSecure
```
Purpose: Secure/authenticate connection
Input: AUTH command (0x41555448)
```

## RPC Functions

### RpcBind
```
Purpose: Bind to a RPC service
Input: Service name, session ID, connection ID
```

### RpcCall
```
Purpose: Make RPC call
Input: Service address, call type, parameters...
```

## Message Format

The ProtoAries layer uses this message format:

```
+----------------+
| Type (4 bytes) |  BE uint32 - Command identifier
+----------------+
| Flags (4 bytes) |  BE uint32 - Message flags
+----------------+
| Length (4 bytes)|  BE uint32 - Total message length
+----------------+
| Payload (var)   |  Key=value pairs, null-terminated
+----------------+
```

## See Also

- `/analysis/decompiled/ProtoAriesConnect.c` - Connection handler
- `/analysis/decompiled/ProtoAriesPeek.c` - Message receiving
- `/analysis/decompiled/ProtoAriesRecv.c` - Data reception
- `/analysis/decompiled/ProtoAriesSend.c` - Data transmission
