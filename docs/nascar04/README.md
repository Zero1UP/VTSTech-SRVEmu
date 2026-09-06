# NASCAR.ELF Protocol Documentation

## Overview
This directory contains documentation for the NASCAR (EA Sports) PS2 network protocol analysis.

## Key Files

### Protocol Documentation
| File | Description |
|------|-------------|
| `master_command_list.md` | Complete command inventory (45 commands) |
| `command_inventory.md` | Categorized command reference |
| `buddy_api_reference.md` | BuddyApi protocol details |
| `undocumented_commands.md` | Newly documented commands |

### Analysis Documents
| File | Description |
|------|-------------|
| `handler_dispatch_analysis.md` | Dispatch architecture |
| `handler_functions.md` | Handler function reference |
| `radare2_analysis_summary.md` | Radare2 analysis findings |
| `r2_analysis_report.md` | r2 usage guide |

### Implementation
| File | Description |
|------|-------------|
| `protocol_implementation_guide.md` | Server implementation guide |
| `implementation-checklist.md` | Implementation checklist |

## Command Summary

### LobbyApi (22 commands)
```
auth, acct, skey, addr, move, room, snap, pers, chat
sel~, ping, @dir, +ses, +msg, +who, +rom, +pop, +usr, +rnk, +snp
```

### BuddyApi (11 commands)
```
ADDR, ROOM, EWBC, PRIV, TEXT, ATTR, PERS, HOST, BLOC, DECL, ACPT
```

### Network Commands (12 commands)
```
PING, AUTH, RECV, SEND, ADMN, PGET, RGET, ROST, RADD, RDEL, dper, cper
```

## Wire Format
```
Offset 0x00: Type   (4 bytes BE) - Command identifier
Offset 0x04: Flags  (4 bytes BE)
Offset 0x08: Length (4 bytes BE) - Total message length
Offset 0x0C: Payload - key=value pairs, null-terminated
```

## Key Addresses

| Component | Address |
|-----------|---------|
| LobbyApiUpdate | 0x31bdf0 |
| BuddyApiUpdate | 0x362020 |
| NetworkEvent_MainDispatcher | 0x1c37c0 |
| ProtoAriesConnect | (see decompiled/) |

## Binary Information
- **File**: NASCAR.ELF
- **Architecture**: MIPS R3000
- **Base**: 0x100000
- **Size**: ~3.1MB
