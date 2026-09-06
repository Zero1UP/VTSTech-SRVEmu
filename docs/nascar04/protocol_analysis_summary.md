# Protocol Analysis Summary

**Binary**: NASCAR.ELF (NASCAR Thunder 2004)  
**Date**: September 6, 2026

---

## Architecture Overview

```
PS2 Client
    │
    ├─► DirServer (TCP:10600) - Server discovery
    │       └─► Returns login server address
    │
    ├─► LoginServer (TCP:10901) - Authentication & Lobby
    │       ├─► Handles auth, persona, room selection
    │       └─► Pushes +who, +rom, +usr, +pop
    │
    └─► BuddyServer (TCP:10899) - P2P messaging
            └─► Handles buddy list, chat, invites
```

---

## Wire Format

### Packet Structure (12-byte header)
```
Offset 0x00: 4 bytes - Message Type (BIG-ENDIAN)
Offset 0x04: 4 bytes - Flags (BIG-ENDIAN)
Offset 0x08: 4 bytes - Length (BIG-ENDIAN, includes header)
Offset 0x0C: N bytes - Payload (KEY=value\x00 pairs)
```

### Key-Value Format
```
KEY=value\x00
```
- Separator: `=`
- Case-insensitive key lookup
- Null-terminated

---

## LobbyApi Commands

### Connection Flow
1. `addr` - Initial connection acknowledgment
2. `skey` - Session key validation
3. `auth` - User authentication
4. `pers` - Persona selection
5. `news` - Get room list and buddy info
6. `move` - Join a room

### Push Commands (Server → Client)
| Command | Keys | Description |
|---------|------|-------------|
| +who | F, N, RI, RT, R, RF | User presence |
| +rom | I, N, H, A, T, L, F | Room listings |
| +usr | I, N, A, F, S, P | User info |
| +pop | Z | Population counts |

---

## BuddyApi Commands

### Command Codes (from binary)
| Command | Hex | Description |
|---------|-----|-------------|
| ADDR | 0x41444452 | Address |
| ROOM | 0x524F4F4D | Room |
| EWBC | 0x45574243 | East/West/Best |
| PRIV | 0x50524956 | Private |
| TEXT | 0x54455854 | Text/Chat |
| ATTR | 0x41545452 | Attribute |
| PERS | 0x50455253 | Persona |
| HOST | 0x484F5354 | Host |
| BLOC | 0x424C4F43 | Block |
| DECL | 0x4445434C | Decline |
| ACPT | 0x41435054 | Accept |

### Network Commands (from decompilation)
| Command | Hex | Description |
|---------|-----|-------------|
| PING | 0x50494E47 | Ping |
| AUTH | 0x41555448 | Auth response |
| ROST | 0x524F5354 | Roster update |
| RADD | 0x52414444 | Add roster entry |
| RDEL | 0x5244454C | Delete entry |
| RGET | 0x52474554 | Get roster |
| PGET | 0x50474554 | Get player config |
| SEND | 0x53454E44 | Send data |
| RECV | 0x52454356 | Receive data |

---

## Field Keys

### Login Flow Fields
| Key | Type | Description |
|-----|------|-------------|
| USER | String | Username |
| PASS | String | Password |
| PROD | String | Product |
| VERS | String | Version |
| SKEY | String | Session key |
| NAME | String | Room name |
| PERS | String | Persona |

### Room Fields
| Key | Type | Description |
|-----|------|-------------|
| I | Int | Room/User ID |
| N | String | Name |
| H | String | Heading |
| A | Int | Address (IP) |
| T | Int | Type (1=Lobby) |
| L | Int | Limit |
| F | String | Flags |
| RI | Int | Room ID |

### User Fields
| Key | Type | Description |
|-----|------|-------------|
| I | Int | User ID |
| N | String | Username |
| A | Int | Address (IP) |
| F | String | Flags |
| S | String | Status |
| P | String | Password |

---

## File References

| Document | Description |
|----------|-------------|
| `master_command_list.md` | Complete command reference with packet examples |
| `proto_api_commands.md` | Command codes and hex values |
| `buddy_api_reference.md` | BuddyApi command table |
| `validation_report.md` | Documentation validation |
| `agent-handoff.md` | Project handoff |

## Decompiled Functions

| Function | Address | Purpose |
|----------|---------|---------|
| LobbyApiUpdate | 0x0031bdf0 | Lobby protocol handler |
| BuddyApiUpdate | 0x00362020 | P2P messaging |
| ProtoAriesSend | - | Send packet |
| ProtoAriesPeek | - | Peek packet header |
| TagFieldFind | - | KV lookup |
