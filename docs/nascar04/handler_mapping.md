# Handler Function Mapping - NASCAR.ELF

## LobbyApiUpdate Command Dispatch

### Complete Command Table (from LobbyApiUpdate at 0x0031bdf0)

| Hex (BE) | Command | Description | Handler Area |
|----------|---------|------------|-------------|
| 0x61757468 | auth | Authentication | Main dispatch |
| 0x61636374 | acct | Account command | Main dispatch |
| 0x736B6579 | skey | Session key | Main dispatch |
| 0x61646472 | addr | Client address | Main dispatch |
| 0x6D6F7665 | move | Room move | Main dispatch |
| 0x726F6F6D | room | Room message | Main dispatch |
| 0x736E6170 | snap | Snapshot | Main dispatch |
| 0x70657273 | pers | Persona | Main dispatch |
| 0x63686174 | chat | Chat message | Main dispatch |
| 0x73656C65 | sel~ | Select (variant) | Main dispatch |

### Internal States

| Hex (BE) | State | Purpose |
|----------|-------|---------|
| 0x636F6E6E | conn | Connection state |
| 0x6F66666C | offl | Offline state |
| 0x69646C65 | idle | Idle/authenticated |
| 0x7465726D | term | Terminate |
| 0x72646972 | rdir | Redirect pending |
| 0x74696D65 | time | Timer check |

## Handler Functions Reference

### LobbyApiUpdate (0x0031bdf0)
```
Purpose: Main lobby protocol command dispatcher
Size: 6412 bytes (214 basic blocks, complexity 111)
Input: Message structure pointer
Output: Processed message response

Call Flow:
1. Extract message type from offset 0x0C
2. Compare against known commands (lui/ori pairs)
3. Branch to appropriate handler
4. Process payload (key=value pairs)
5. Send response via ProtoAriesSend
```

### String/Parser Functions

| Address | Function | Purpose |
|---------|----------|---------|
| 0x31ddd0 | str_copy | String copy with formatting |
| 0x31e8b0 | parse_num | Parse ASCII digits (+/- prefix) |
| 0x31e988 | parse_num_ext | Parse with 16-bit bounds |
| 0x31e520 | format_str | Format string with table lookup |

### Message Response Functions

| Address | Function | Purpose |
|---------|----------|---------|
| 0x31af10 | send_response | Send "term" response to client |
| 0x31abd0 | format_message | Format protocol message with params |
| 0x31bdd0 | LobbyApiUpdate_thunk | Entry thunk |

### Network Functions

| Address | Function | Purpose |
|---------|----------|---------|
| 0x31a628 | net_callback | Network state change callback |
| 0x31a760 | net_process | Process network data |
| 0x31a898 | net_send | Send data to client |
| 0x322190 | proto_parse | Parse protocol message |
| 0x322040 | proto_encode | Encode protocol message |
| 0x3222f0 | proto_process | Process message buffer |
| 0x322608 | proto_init | Initialize protocol |

### Room Functions

| Address | Function | Purpose |
|---------|----------|---------|
| 0x31ed10 | room_update | Update room state |
| 0x31ef10 | room_handler | Room-specific handler |
| 0x31f328 | room_notify | Notify room changes |

## ProtoAries Layer Functions

### Connection Functions

| Function | Address | Purpose |
|----------|---------|---------|
| ProtoAriesConnect | (decompiled) | Establish server connection |
| ProtoAriesPeek | (decompiled) | Non-blocking message check |
| ProtoAriesRecv | (decompiled) | Receive message |
| ProtoAriesSend | (decompiled) | Send message |
| ProtoAriesSecure | (decompiled) | Authenticate connection |
| ProtoAriesTick | (decompiled) | Connection heartbeat |

### Network Abstraction

| Function | Purpose |
|----------|---------|
| RpcBind | Bind to RPC service |
| RpcCall | Make RPC call |
| Network_TimeoutCheck | Check connection timeout |
| Network_AuthComplete | Authentication complete callback |

## Dispatch Architecture

```
NetworkEvent_MainDispatcher (0x1c37c0)
    |
    +-> Game_CommandRouter (0x1c6b70)
    |       |-> System handlers
    |       |-> Connection handlers
    |       |-> Device handlers
    |       |-> Auth handlers
    |
    +-> NetworkEvent_FallbackDispatcher
    |
    +-> Protocol_CommandDispatcher
    |       |-> Protocol message handling
    |
    +-> ChallengeSystem_CommandDispatcher
    |       |-> Challenge commands (chal, dper, cper)
    |
    +-> Game_HandleSystemCommand
    |       |-> Internal system commands
    |
    +-> [Switch case 0-0x7F]
            |-> Timer, video, audio, input, memory
```

## Message Processing Flow

```
Incoming UDP/TCP Packet
        |
        v
ProtoAriesPeek()
        |
        v
Extract Header (Big-Endian)
  - Type (offset 0x00)
  - Flags (offset 0x04)
  - Length (offset 0x08)
        |
        v
Parse Payload (key=value pairs)
        |
        v
LobbyApiUpdate() or BuddyApiUpdate()
        |
        v
Command Dispatch (switch on type)
        |
        v
Handler Function
        |
        v
ProtoAriesSend() or ProtoAriesRecv()
        |
        v
Response to Client
```

## BuddyApi Commands (from string table 0x003d8378)

| Hex (BE) | Command | Description |
|----------|---------|-------------|
| 0x41444452 | ADDR | Address lookup |
| 0x524F4F4D | ROOM | Room operations |
| 0x45574243 | EWBC | East/West/Best |
| 0x50524956 | PRIV | Private message |
| 0x54455854 | TEXT | Text message |
| 0x41545452 | ATTR | User attributes |
| 0x50455253 | PERS | Persona data |
| 0x484F5354 | HOST | Host game |
| 0x424C4F43 | BLOC | Block user |
| 0x4445434C | DECL | Decline invitation |
| 0x41435054 | ACPT | Accept invitation |

## Network Protocol Commands (from BuddyApiUpdate decompilation)

| Hex (BE) | Command | Description |
|----------|---------|-------------|
| 0x50494E47 | PING | Keepalive |
| 0x41555448 | AUTH | Authentication |
| 0x52454356 | RECV | Receive data |
| 0x53454E44 | SEND | Send data |
| 0x41444D4E | ADMN | Admin command |
| 0x50474554 | PGET | Player get |
| 0x524F5354 | ROST | Roster update |
| 0x52414444 | RADD | Roster add |
| 0x5244454C | RDEL | Roster delete |

## Binary String Tables

### BuddyApi Commands (0x003d8378)
```
ADDR ROOM EWBC PRIV TEXT ATTR PERS HOST BLOC DECL ACPT
```

### IP Format (0x003d83e8)
```
"%d.%d.%d.%d:%d"
```

### Challenge/Filter (0x003d8400)
Contains profanity filter words for chat moderation.

## See Also

- `/docs/handler_dispatch_analysis.md` - Dispatch architecture
- `/docs/master_command_list.md` - Complete command inventory
- `/analysis/decompiled/BuddyApiUpdate.c` - BuddyApi decompiled
- `/analysis/decompiled/NetworkEvent_MainDispatcher.c` - Dispatcher decompiled

## BuddyApi Functions (from decompilation)

### Core Functions

| Function | Purpose |
|----------|---------|
| BuddyApiUpdate | Main entry point |
| ProtoAriesTick | Connection heartbeat |
| ProtoAriesUpdate | Update connection state |
| ProtoAriesConnect | Establish connection |
| ProtoAriesSecure | Authenticate connection |
| ProtoAriesPeek | Check for messages |
| ProtoAriesSend | Send message |
| ProtoAriesRecv | Receive message |

### Buddy System Functions

| Function | Purpose |
|----------|---------|
| Buddy_ProcessUsername | Process username string |
| Buddy_FindUserByString | Find user in roster |
| Buddy_AddUser | Add user to roster |
| Buddy_GetUserData | Get user data structure |
| Buddy_RemoveUser | Remove user from roster |
| Buddy_ConfigUpdate | Update buddy configuration |

### Network Functions

| Function | Purpose |
|----------|---------|
| Network_TimeoutCheck | Check connection timeout |
| Network_AuthComplete | Authentication complete callback |
| Network_HandleReceive | Handle received data |
| Network_SendPlayerData | Send player data |
| Lobby_ClearProtocolState | Clear protocol state |

### Tag Field Functions

| Function | Purpose |
|----------|---------|
| TagFieldFind | Find field in message |
| TagFieldGetNumber | Get numeric field value |
| TagFieldGetString | Get string field value |

### Internal Functions

| Function | Purpose |
|----------|---------|
| _BuddyApiTransact | Transaction wrapper |
| _BuddyApiStatus | Set status |
| _BuddyApiDebug | Debug output |
| DispListOrder | Display list ordering |

## BuddyApi Message Structure

Messages use TagField format for payload:
```
KEY=value\x00KEY2=value2\x00...
```

### Common Field Names

| Field | Type | Description |
|-------|------|-------------|
| TYPE | number | Message type |
| BUDDY | string | Buddy identifier |
| USER | string | Username |
| NICK | string | Nickname |
| GRUP | string | Group name |
| DATA | binary | Additional data |
