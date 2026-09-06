# Handler Dispatch Analysis - NASCAR.ELF

## Overview
Analysis of command handler functions in NASCAR.ELF, mapping the dispatch architecture.

## Dispatch Architecture

From `NetworkEvent_MainDispatcher` (0x001c37c0):

```
NetworkEvent_MainDispatcher
    |
    +-> Game_CommandRouter        (0x001c6b70) - Game state commands
    |       |
    |       +-> SystemBasic_Handler
    |       +-> SystemConfig_Handler
    |       +-> Connection_Initialize
    |       +-> Game_HandleProtocolCommand
    |       +-> Device_* handlers
    |       +-> Auth_* handlers
    |       +-> Graphics_* handlers
    |       +-> Session_* handlers
    |
    +-> NetworkEvent_FallbackDispatcher
    |
    +-> Protocol_CommandDispatcher    - Network protocol commands
    |
    +-> ChallengeSystem_CommandDispatcher - Challenge commands
    |
    +-> Game_HandleSystemCommand     - System commands
    |
    +-> [Internal system commands]
```

## LobbyApiUpdate (0x0031bdf0)

Main handler for LobbyApi protocol commands.

### Commands Dispatched

| Command | Hex | Handler Offset | Description |
|---------|-----|----------------|-------------|
| auth | 0x61757468 | - | Authentication |
| acct | 0x61636374 | - | Account command |
| skey | 0x736B6579 | - | Session key |
| addr | 0x61646472 | - | Client address |
| move | 0x6D6F7665 | - | Room move |
| room | 0x726F6F6D | - | Room message |
| snap | 0x736E6170 | - | Snapshot |
| pers | 0x70657273 | - | Persona |
| chat | 0x63686174 | - | Chat message |
| sel~ | 0x73656C65 | - | Select variant |

### Internal States (Not Commands)

| State | Hex | Purpose |
|-------|-----|---------|
| conn | 0x636F6E6E | Connection state |
| offl | 0x6F66666C | Offline state |
| idle | 0x69646C65 | Idle/authenticated |
| term | 0x7465726D | Terminate |
| rdir | 0x72646972 | Redirect pending |
| time | 0x74696D65 | Timer check |

## Key Handler Functions

### String/Parser Functions

| Address | Name | Purpose |
|---------|------|---------|
| 0x31ddd0 | str_handler | String scanning/comparison |
| 0x31e8b0 | parse_num | Parse ASCII number (+/- prefix) |
| 0x31e988 | parse_num_ext | Parse number with bounds |

### Message Functions

| Address | Name | Purpose |
|---------|------|---------|
| 0x31af10 | send_response | Send "term" response |
| 0x31abd0 | format_message | Format protocol message |
| 0x31bdd0 | lobby_thunk | Entry thunk to LobbyApiUpdate |

### Network Functions

| Address | Name | Purpose |
|---------|------|---------|
| 0x31a628 | net_callback | Network state callback |
| 0x31a760 | net_process | Process network data |
| 0x322190 | proto_parse | Parse protocol message |
| 0x322040 | proto_encode | Encode protocol message |
| 0x322608 | proto_init | Initialize protocol |

### Room Functions

| Address | Name | Purpose |
|---------|------|---------|
| 0x31ed10 | room_update | Update room state |

## ProtoAries Layer

Low-level networking from decompiled files:

### Message Format
```
Offset 0x00: Type (4 bytes BE) - Command identifier
Offset 0x04: Flags (4 bytes BE)
Offset 0x08: Length (4 bytes BE)
Offset 0x0C: Payload - key=value pairs
```

### Functions

- `ProtoAriesConnect`: Establish connection
- `ProtoAriesPeek`: Check for data (non-blocking)
- `ProtoAriesRecv`: Receive data
- `ProtoAriesSend`: Send data
- `ProtoAriesSecure`: Authenticate connection

## BuddyApi Commands (from decompilation)

| Command | Hex | Description |
|---------|-----|-------------|
| PING | 0x50494E47 | Keepalive |
| AUTH | 0x41555448 | Authentication |
| RECV | 0x52454356 | Receive data |
| SEND | 0x53454E44 | Send data |
| ADMN | 0x41444D4E | Admin |
| PGET | 0x50474554 | Player get |
| RGET | 0x52474554 | Roster get |
| ROST | 0x524F5354 | Roster update |
| RADD | 0x52414444 | Roster add |
| RDEL | 0x5244454C | Roster delete |

## Call Flow Example

```
Incoming Message -> ProtoAriesPeek -> BuddyApiUpdate
                                              |
                                              +-> Parse message type (iStack_17c)
                                              |
                                              +-> Switch on type:
                                              |     case PING: ProtoAriesSend
                                              |     case AUTH: auth handler
                                              |     case ROST: roster handler
                                              |
                                              +-> ProtoAriesRecv -> next message
```

## See Also

- `/analysis/decompiled/BuddyApiUpdate.c`
- `/analysis/decompiled/NetworkEvent_MainDispatcher.c`
- `/analysis/decompiled/Game_CommandRouter.c`
- `/docs/master_command_list.md`

## System Commands (Internal)

From NetworkEvent_MainDispatcher switch statement (case 0-0x7F internal commands):

| ID | Handler | Purpose |
|----|---------|---------|
| 0 | System_GetTimerValue | Get timer |
| 1 | Network_ConfigureConnection | Configure network |
| 2 | System_GetResourceStatus | Check resource |
| 3 | Video_GetAspectRatio | Video mode |
| 4 | Network_InitializeSession | Init network session |
| 5-0x17 | Various | Reserved |
| 0x1B | System_CheckPermission | Permission check |
| 0x20 | Protocol_ResetChannel | Reset protocol channel |
| 0x21 | Protocol_GetChannelStatus | Get channel status |
| 0x40 | Network_SetQualityParams | Set network quality |
| 0x46 | Network_ConfigureProtocol | Configure protocol |
| 0x4D | Network_CloseConnection | Close connection |

## Protocol Commands (from LobbyApiUpdate)

The LobbyApiUpdate function dispatches lobby protocol commands. Commands are
identified by their 4-byte ASCII identifier at offset 0x0C of the message.

### Message Structure
```
+----------------+
| Type (4 bytes) |  LobbyApi command (e.g., "auth", "acct")
+----------------+
| Flags (4 bytes) |  Message flags
+----------------+
| Length (4 bytes)|  Total message length
+----------------+
| Payload         |  key=value pairs, null-terminated
+----------------+
```

### Command Flow
1. ProtoAriesPeek receives message
2. Message type extracted from offset 0x0C
3. LobbyApiUpdate dispatches to handler based on type
4. Handler processes payload (key=value pairs)
5. Response sent via ProtoAriesSend

## File References

- Binary base: 0x100000
- LobbyApiUpdate: 0x31bdf0
- BuddyApiUpdate: 0x362020
- NetworkEvent_MainDispatcher: 0x1c37c0
- ProtoAriesConnect: see decompiled
