# NASCAR.ELF LobbyApi Analysis

## Binary Info
- **File**: NASCAR.ELF (NASCAR Thunder 2004)
- **Architecture**: MIPS R3000 (little-endian)
- **Base Address**: 0x100000
- **Size**: 3.1MB

## Key Functions

### LobbyApiUpdate (0x0031bdf0)
Main message dispatch loop for LobbyApi protocol.
- Size: 6412 bytes
- Calls: ProtoAriesTick(), Lobby_ChangeConnectionState(), Lobby_ProcessNetworkEvents()
- Processes: Internal state commands, broadcast messages, binary message types

### NetworkReceive_CommandDispatcher (0x001012c8)
Lower-level packet dispatcher that calls LobbyApiUpdate.
- Handles incoming network data
- Routes to appropriate handler based on message type

## Protocol Architecture

```
NetworkReceive_CommandDispatcher (0x001012c8)
    └─> LobbyApiUpdate (0x0031bdf0)
         ├─> ProtoAriesPeek() - read incoming message
         ├─> Dispatch by command type:
         │    ├─> Internal state (auth, acct, skey, etc.)
         │    ├─> Broadcast (+ses, +msg, +who, etc.)
         │    └─> Binary messages (ping, room, move)
         └─> ProtoAriesSend() - send response
```

## Command Classification

### LobbyApi Commands (lowercase)
Used internally by the client for session management and broadcasting.

### BuddyApi Commands (UPPERCASE)
Used for peer-to-peer messaging between clients in same room.

## References
- String table: 0x003d8378 (ADDR, ROOM, EWBC, PRIV, TEXT, etc.)
- Buddy field keys: 0x003d9a40 (WHEN, AUTH, REPT, NAME0, etc.)
