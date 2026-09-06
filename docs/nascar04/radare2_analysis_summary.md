# Radare2 Analysis Summary - NASCAR.ELF

## Overview
Comprehensive analysis of NASCAR.ELF using Radare2 to understand the network protocol architecture.

## Binary Information
- **File**: NASCAR.ELF
- **Architecture**: MIPS R3000 (little-endian)
- **Base Address**: 0x100000
- **Size**: ~3.1MB

## Key Findings

### Protocol Architecture
The EA NASCAR games use a multi-layered protocol architecture:

1. **ProtoAries Layer** - Low-level networking
2. **LobbyApi Layer** - Lobby/room management
3. **BuddyApi Layer** - Friend system
4. **Protocol Layer** - In-game protocol
5. **ChallengeSystem Layer** - Challenge commands

### Message Format
All protocol messages use big-endian 32-bit values:

```
Offset 0x00: Message Type (4 bytes BE)
Offset 0x04: Flags (4 bytes BE)
Offset 0x08: Length (4 bytes BE, includes header)
Offset 0x0C: Payload (key=value pairs, null-terminated)
```

## Commands Discovered

### LobbyApi Commands (from LobbyApiUpdate at 0x0031bdf0)

| Command | Hex (BE) | Description |
|---------|----------|-------------|
| auth | 0x61757468 | Authentication request |
| acct | 0x61636374 | Account operations |
| skey | 0x736B6579 | Session key exchange |
| addr | 0x61646472 | Client address response |
| move | 0x6D6F7665 | Room move command |
| room | 0x726F6F6D | Room message/join |
| snap | 0x736E6170 | Snapshot data |
| pers | 0x70657273 | Persona operations |
| chat | 0x63686174 | Chat message |
| sel~ | 0x73656C65 | Selection command |

### Internal States (not protocol commands)

| State | Hex | Purpose |
|-------|-----|---------|
| conn | 0x636F6E6E | Connection established |
| offl | 0x6F66666C | Offline mode |
| idle | 0x69646C65 | Idle/authenticated |
| term | 0x7465726D | Terminate session |
| rdir | 0x72646972 | Redirect pending |
| time | 0x74696D65 | Timer check |

### BuddyApi Commands (from string table at 0x003d8378)

| Command | Hex (BE) | Description |
|---------|----------|-------------|
| ADDR | 0x41444452 | Address lookup |
| ROOM | 0x524F4F4D | Room operations |
| EWBC | 0x45574243 | East/West/Best competition |
| PRIV | 0x50524956 | Private message |
| TEXT | 0x54455854 | Text message |
| ATTR | 0x41545452 | User attributes |
| PERS | 0x50455253 | Persona data |
| HOST | 0x484F5354 | Host game |
| BLOC | 0x424C4F43 | Block user |
| DECL | 0x4445434C | Decline invitation |
| ACPT | 0x41435054 | Accept invitation |

### BuddyApi Network Commands (from BuddyApiUpdate decompilation)

| Command | Hex (BE) | Description |
|---------|----------|-------------|
| PING | 0x50494E47 | Keepalive ping |
| AUTH | 0x41555448 | Authentication |
| RECV | 0x52454356 | Receive data |
| SEND | 0x53454E44 | Send data |
| ADMN | 0x41444D4E | Admin command |
| PGET | 0x50474554 | Player get |
| ROST | 0x524F5354 | Roster update |
| RADD | 0x52414444 | Roster add |
| RDEL | 0x5244454C | Roster delete |

## Handler Functions

### LobbyApi Handlers (from LobbyApiUpdate)

| Address | Function | Purpose |
|---------|----------|---------|
| 0x31bdf0 | LobbyApiUpdate | Main lobby handler |
| 0x31ddd0 | str_handler | String comparison/scan |
| 0x31e8b0 | parse_num | Parse ASCII number (+/-) |
| 0x31e988 | parse_num_ext | Parse with 16-bit bounds |
| 0x31af10 | send_response | Send "term" response |
| 0x31abd0 | format_message | Format protocol message |
| 0x31a628 | net_callback | Network state callback |
| 0x31a760 | net_process | Network data processing |
| 0x31ed10 | room_update | Room state update |

### ProtoAries Functions

| Function | Purpose |
|----------|---------|
| ProtoAriesConnect | Establish connection to server |
| ProtoAriesPeek | Check for data (non-blocking) |
| ProtoAriesRecv | Receive data from server |
| ProtoAriesSend | Send data to server |
| ProtoAriesSecure | Authenticate connection |

### Dispatch Chain

```
NetworkEvent_MainDispatcher (0x1c37c0)
    |
    +-> Game_CommandRouter (0x1c6b70)
    |       Handles: System, Connection, Device, Auth, Graphics, Session
    |
    +-> NetworkEvent_FallbackDispatcher
    |
    +-> Protocol_CommandDispatcher
    |       Handles: Network protocol commands
    |
    +-> ChallengeSystem_CommandDispatcher
    |       Handles: Challenge system commands
    |
    +-> Game_HandleSystemCommand
    |       Handles: Internal system commands
    |
    +-> [Switch case 0-0x7F]
            Various internal game commands
```

## String Tables

### BuddyApi Commands (0x003d8378)
```
ADDR ROOM EWBC PRIV TEXT ATTR PERS HOST BLOC DECL ACPT
```

### Challenge/Chat Filter (0x003d8400)
Contains profanity filter words used for chat moderation.

### IP Format String (0x003d83e8)
```
"%d.%d.%d.%d:%d" - IP address formatting
```

## Using Radare2

### Basic Commands
```bash
# Load binary
L nascar

# Analyze function
s 0x0031bdf0
af

# Disassemble
pd 200

# Find function calls
pd 2000 | grep "jal 0x"
```

### Finding Commands in Assembly
Commands are built using lui/ori MIPS instruction pairs:

```python
# Example: Building "auth" (0x61757468)
lui v0, 0x6175  # 'au'
ori v0, v0, 0x7468  # 'th'
```

### Useful r2 Commands
- `axt addr` - Find xrefs to address
- `axf addr` - Find function xrefs
- `afl` - List functions
- `pdf` - Disassemble function
- `pdcc` - Pseudo-C output (limited)

## See Also
- `/docs/master_command_list.md` - Complete command inventory
- `/docs/buddy_api_reference.md` - BuddyApi protocol details
- `/docs/handler_dispatch_analysis.md` - Dispatch architecture
- `/analysis/decompiled/*.c` - Decompiled function files
