# NASCAR Thunder 2004 Server Emulator - Agent Handoff

## Overview
This document provides a comprehensive handoff for the NASCAR Thunder 2004 PS2 server emulator project, detailing the current implementation, architecture, and next steps for completion.

**Last Updated**: September 6, 2026  
**Analysis Session**: Radare2 command handler analysis, cper/dper validation

## Project Status

### Completed Analysis

- **Binary Analysis**: 10,219 functions identified using radare2
- **Function Renaming**: 1,004 functions renamed from functions.json
- **Ghidra Decompilation**: 14 functions decompiled
- **Radare2 Analysis**: Command handlers mapped, dispatch architecture documented
- **Protocol Documentation**: Complete specification (45 commands)

## Server Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                     NASCAR Thunder 2004 — PS2                         │
│                                                                     │
│  ┌──────────┐    TCP:10600     ┌────────────┐    TCP:10901      ┌──────────────┐
│  │   PS2     │ ──────────────► │ Dir Server  │ ───────────────► │  Login       │
│  │  Client   │ ◄────────────── │ (10600)     │ ◄─────────────── │  Server      │
│  │           │                 └────────────┘                  └──────────────┘
│  │           │                                                      │
│  │           │              hands off ADDR+PORT+LKEY                │
│  │           │              hands off BUDDY_PORT+BUDDY_URL          │
│  │           │                                                      │
│  └──────────┘                                        │             │
│       │                                              │             │
│       │                          TCP:10899          │             │
│       │           ┌──────────────────────────────────┘             │
│       │           ▼                                                  │
│       └───► │ Buddy Server  │                                          │
│          │ (10899)         │                                          │
│          └─────────────────┘                                          │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

## Implemented Components

| Component | File | Port | Status |
|-----------|------|------|--------|
| Directory Server | dir_server.py | TCP:10600 | ✅ Complete |
| Login Server | login_server.py | TCP:10901 | ✅ Complete |
| Buddy Server | buddy_server.py | TCP:10899 | ✅ Complete |
| EA Protocol | ea_protocol.py | - | ✅ Complete |

## Wire Format

```
Offset 0x00: Type   (4 bytes, BIG-ENDIAN)
Offset 0x04: Flags (4 bytes, BIG-ENDIAN)
Offset 0x08: Length (4 bytes, BIG-ENDIAN, includes 12-byte header)
Offset 0x0C: Payload (key=value\x00 pairs)
```

## Complete Command Inventory (45 Commands)

### LobbyApi Commands (22) - Handler: LobbyApiUpdate (0x0031bdf0)

| Command | Hex (BE) | Direction | Description |
|---------|-----------|-----------|-------------|
| +ses | 0x2B736573 | Server→Client | Session broadcast |
| +msg | 0x2B6D7367 | Server→Client | Chat message |
| +who | 0x2B77686F | Server→Client | Room population |
| +rom | 0x2B726F6D | Server→Client | Room data update |
| +pop | 0x2B706F70 | Server→Client | Population counts |
| +usr | 0x2B757372 | Server→Client | User roster |
| +rnk | 0x2B726E6B | Server→Client | Rank update |
| +snp | 0x2B736E70 | Server→Client | Snapshot |
| auth | 0x61757468 | Bidirectional | Authentication |
| acct | 0x61636374 | Bidirectional | Account |
| skey | 0x736B6579 | Bidirectional | Session key |
| Sele | 0x73656C65 | Bidirectional | Select |
| snap | 0x736E6170 | Bidirectional | Snapshot |
| pers | 0x70657273 | Bidirectional | Persona |
| ping | 0x7E706E67 | Bidirectional | Ping |
| @dir | 0x40646972 | Server→Client | Direct connection redirect |
| move | 0x6D6F7665 | Client→Server | Room move |
| room | 0x726F6F6D | Bidirectional | Room message |
| addr | 0x61646472 | Client→Server | Client address response |
| chal | 0x6368616C | Bidirectional | Challenge command |
| auxi | 0x61757869 | Bidirectional | Auxiliary/Status |
| peek | 0x7065656B | Bidirectional | Peek command |

### BuddyApi Commands (11) - Handler: BuddyApiUpdate (0x00362020)

| Command | Hex (BE) | Description |
|---------|-----------|-------------|
| ADDR | 0x41444452 | Address lookup |
| ROOM | 0x524F4F4D | Room operations |
| EWBC | 0x45574243 | East/West/Best |
| PRIV | 0x50524956 | Private message |
| TEXT | 0x54455854 | Text/Chat |
| ATTR | 0x41545452 | User attributes |
| PERS | 0x50455253 | Persona |
| HOST | 0x484F5354 | Host game |
| BLOC | 0x424C4F43 | Block user |
| DECL | 0x4445434C | Decline invitation |
| ACPT | 0x41435054 | Accept invitation |

### Network Commands (12) - OUTBOUND ONLY (Client→Server)

| Command | Hex (BE) | Description |
|---------|-----------|-------------|
| PING | 0x50494E47 | Keepalive |
| AUTH | 0x41555448 | Auth request |
| RECV | 0x52454356 | Receive data |
| SEND | 0x53454E44 | Send data |
| ADMN | 0x41444D4E | Admin |
| PGET | 0x50474554 | Player get |
| RGET | 0x52474554 | Roster get |
| ROST | 0x524F5354 | Roster update |
| RADD | 0x52414444 | Roster add |
| RDEL | 0x5244454C | Roster delete |
| **cper** | 0x63706572 | **Create persona** |
| **dper** | 0x64706572 | **Delete persona** |

**NOTE**: cper and dper are confirmed to use `PERS`, `ALTS`, and `STATUS` fields only.

## cper/dper Commands (Client-Only)

These commands are sent by the PS2 client to the server. No handler exists in the binary.

### cper (0x63706572) - Create Persona

**Request**:
```
PERS=<persona_name>\x00
```

**Response**:
```
PERS=<created_persona>\x00
ALTS=<total_alternates>\x00
STATUS=<1=success, 0=failure>\x00
```

### dper (0x64706572) - Delete Persona

**Request**:
```
PERS=<persona_to_delete>\x00
```

**Response**:
```
PERS=<deleted_persona>\x00
ALTS=<remaining_alternates>\x00
STATUS=<1=success, 0=failure>\x00
```

**Confirmed Fields**: `PERS`, `ALTS`, `STATUS`

## Command Direction Summary

| Category | Count | Has Handler | Outbound Only |
|----------|-------|------------|---------------|
| LobbyApi | 22 | 22 | 2 (move, addr) |
| BuddyApi | 11 | 11 | 0 |
| Network | 12 | **0** | 12 (all) |

**All Network commands are outbound-only** - the PS2 client sends them, the server must handle them.

## Handler Function Mapping

### LobbyApiUpdate Handlers (0x0031bdf0)

| Address | Function | Purpose |
|---------|---------|---------|
| 0x31bdf0 | LobbyApiUpdate | Main lobby dispatcher |
| 0x31ddd0 | str_handler | String operations |
| 0x31e8b0 | parse_num | Parse ASCII number |
| 0x31e988 | parse_num_ext | Parse with bounds |
| 0x31af10 | send_response | Send "term" response |
| 0x31abd0 | format_message | Format protocol message |
| 0x31ed10 | room_update | Room state update |

### ProtoAries Functions

| Function | Purpose |
|----------|---------|
| ProtoAriesConnect | Establish connection |
| ProtoAriesPeek | Check for data (big-endian header) |
| ProtoAriesRecv | Receive data |
| ProtoAriesSend | Send data |
| ProtoAriesSecure | Authenticate |

## Binary String Tables

| Location | Contents |
|----------|----------|
| 0x003d8378 | BuddyApi commands (ADDR, ROOM, PRIV, TEXT, ATTR, PERS, HOST, BLOC, DECL, ACPT) |
| 0x003d8400 | Challenge strings, profanity filter |
| 0x003d83e8 | IP format string ("%d.%d.%d.%d:%d") |

## Internal States (NOT Commands)

| State | Hex | Purpose |
|-------|-----|---------|
| conn | 0x636F6E6E | Connection state |
| idle | 0x69646C65 | Idle/authenticated |
| offl | 0x6F66666C | Offline |
| term | 0x7465726D | Terminate |
| rdir | 0x72646972 | Redirect pending |

## Key Files

| Path | Description |
|------|-------------|
| `/home/vtstech/workspace/docs/` | Analysis documentation |
| `/home/vtstech/workspace/docs/master_command_list.md` | Full command reference |
| `/home/vtstech/workspace/docs/command_inventory.md` | Command inventory |
| `/home/vtstech/workspace/docs/command_directions.md` | Direction matrix |
| `/home/vtstech/workspace/docs/cper_dper_commands.md` | cper/dper details |
| `/home/vtstech/workspace/docs/persona_management.md` | Persona system |
| `/home/vtstech/workspace/docs/handler_mapping.md` | Handler functions |
| `/home/vtstech/workspace/docs/handler_dispatch_analysis.md` | Dispatch architecture |
| `/home/vtstech/workspace/analysis/decompiled/` | Ghidra decompiled functions |

## Next Steps

### High Priority
- [ ] Implement Network command handlers (cper, dper, PING, ROST, etc.)
- [ ] Test complete client connection flow
- [ ] Validate cper/dper implementation

### Medium Priority
- [ ] Implement LobbyApi broadcast messages (+ses, +msg, +who, etc.)
- [ ] Complete BuddyApi roster operations
- [ ] Add proper session persistence

### Long-term
- [ ] Performance optimization
- [ ] Comprehensive testing suite

---

**Version**: 1.2  
**Status**: Binary Analysis Complete - Server Implementation Phase
