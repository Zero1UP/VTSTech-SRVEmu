# LobbyApi Binary Protocol Commands

## Source
Decompiled from `LobbyApiUpdate` at 0x0031bdf0 in NASCAR.ELF using Ghidra 12.1.3

## Message Format
Messages are identified by a 4-byte command code in BIG-ENDIAN format at `iStack_b0`.
The LobbyApiUpdate function dispatches based on these command codes.

## Command Codes (Hex Big-Endian)

### Internal State Commands (connection state machine)
| Hex | Command | Description |
|-----|---------|-------------|
| 0x61757468 | auth | Authentication request |
| 0x61636374 | acct | Account |
| 0x736b6579 | skey | Session key |
| 0x73656c65 | sele | Select |
| 0x736e6170 | snap | Snapshot |
| 0x70657273 | pers | Persona |

### Broadcast Commands (+ prefix)
| Hex | Command | Description |
|-----|---------|-------------|
| 0x2b736573 | +ses | Session broadcast |
| 0x2b6d7367 | +msg | Chat message |
| 0x2b77686f | +who | Room population |
| 0x2b726f6d | +rom | Room data update |
| 0x2b706f70 | +pop | Population update |
| 0x2b757372 | +usr | User/player roster |
| 0x2b726e6b | +rnk | Rank update |
| 0x2b736e70 | +snp | Snapshot broadcast |

### Binary Message Types
| Hex | Command | Description |
|-----|---------|-------------|
| 0x7e706e67 | ping | Ping request |
| 0x40646972 | @dir | Direct connection |
| 0x6d6f7665 | move | Room move request |
| 0x726f6f6d | room | Room message type |

## Flow Analysis
From LobbyApiUpdate decompilation:
1. Check piVar24[0xc4] - room hash table (for +rom, +pop)
2. Check piVar24[0xc9] - user roster (for +usr)
3. Check piVar24[0xce] - rank table (for +rnk)
4. Check piVar24[0x147] - chat callback (for +msg)
5. Check piVar24[0x142] - snapshot index (for +snp, must be 4-7)

## Byte Order
MIPS is little-endian, so network wire format uses big-endian.
- Search LE bytes: `echo -n "+msg" | xxd -e -g1` gives `67 73 6d 2b`

## Verified Strings
All command strings verified present in NASCAR.ELF binary:
- `+msg` at 0x003dXXXX
- `ping` at 0x003dXXXX
