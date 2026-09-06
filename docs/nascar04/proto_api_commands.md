# ProtoAries Protocol Command Reference

**Validated against decompiled code from Ghidra**

## Wire Format (Validated)

### Packet Structure (12-byte header)
```
Offset 0x00: Message Type (4 bytes, BIG-ENDIAN)
Offset 0x04: Flags (4 bytes, BIG-ENDIAN)
Offset 0x08: Length (4 bytes, BIG-ENDIAN, includes 12 for header)
Offset 0x0C: Payload data
```

From `ProtoAriesSend.c`:
- Header size: 0xC (12 bytes)
- Type, Flags, Length are all split into bytes in BIG-ENDIAN order
- Payload follows immediately after header

### Key-Value Format
```
KEY=value\x00
```
- Separators: `=` or `:` (from `TagFieldFind.c`)
- Case-insensitive key lookup
- Null-terminated strings
- Quoted strings supported (single or double quotes)

---

## LobbyApi Commands (Lowercase/+ Prefix)

**Source**: `LobbyApiUpdate` decompilation

### Broadcast Commands (+ prefix)
| Hex (BE) | Command | Description |
|----------|---------|-------------|
| 0x2B736573 | +ses | Session broadcast |
| 0x2B6D7367 | +msg | Chat message |
| 0x2B77686F | +who | Room population |
| 0x2B726F6D | +rom | Room data update |
| 0x2B706F70 | +pop | Population update |
| 0x2B757372 | +usr | User/player roster |
| 0x2B726E6B | +rnk | Rank update |
| 0x2B736E70 | +snp | Snapshot broadcast |

### Internal State Commands (lowercase)
| Hex (BE) | Command | Description |
|----------|---------|-------------|
| 0x61757468 | auth | Authentication request |
| 0x61636374 | acct | Account |
| 0x736B6579 | skey | Session key |
| 0x73656C65 | Sele | Select |
| 0x736E6170 | snap | Snapshot |
| 0x70657273 | pers | Persona |

### Binary Message Types (lowercase)
| Hex (BE) | Command | Description |
|----------|---------|-------------|
| 0x7E706E67 | ~png | Ping request |
| 0x40646972 | @dir | Direct connection |
| 0x6D6F7665 | move | Room move request |
| 0x726F6F6D | room | Room message type |

---

## BuddyApi Commands (UPPERCASE)

**Source**: `BuddyApiUpdate` decompilation

### Server → Client Commands
| Hex (BE) | Command | Description |
|----------|---------|-------------|
| 0x50494E47 | PING | Ping request |
| 0x41555448 | AUTH | Authentication response |
| 0x52454356 | RECV | Receive data from peer |
| 0x53454E44 | SEND | Send data to peer command |
| 0x41444D4E | ADMN | Admin/manifest |
| 0x50474554 | PGET | Player config get |
| 0x52474554 | RGET | Get roster entry |
| 0x524F5354 | ROST | Roster update |
| 0x52414444 | RADD | Add/update roster entry |
| 0x5244454C | RDEL | Delete roster entry |

### Client → Server Responses
| Hex (BE) | Command | Description |
|----------|---------|-------------|
| 0x61757468 | auth | Auth response |
| 0x73656E64 | send | Send response |
| 0x61646475 | addu | Add user response |
| 0x64656C75 | delu | Delete user response |
| 0x656E6472 | endr | End roster sync |

---

## TagField Keys

**Source**: `TagFieldFind.c`, `BuddyApiUpdate.c`

### BuddyApi Fields
| Key | Usage |
|-----|-------|
| TYPE | Message type field |
| RQST | Request type |
| USER | Username |
| NICK | Nickname |
| GROUP | Group |

### Network Fields
| Key | Description |
|-----|-------------|
| NET_PingField | Ping value |
| LKEY | Login key |
| PASS | Password |
| TOS | Terms of service |
| NAME | Name |
| PERS | Persona |
| DESC | Description |
| TITL | Title |

---

## Command Dispatch Index

From `LobbyApiUpdate.c`:
- `piVar24[0xc4]` - Room hash table (for +rom, +pop)
- `piVar24[0xc9]` - User roster hash table (for +usr)
- `piVar24[0xce]` - Rank hash table (for +rnk)
- `piVar24[0x147]` - Chat callback (for +msg)
- `piVar24[0x142]` - Snapshot index (for +snp, must be 4-7)

From `BuddyApiUpdate.c`:
- `piVar21[0x131]` - Auth callback
- `piVar21[0x12a]` - Roster hash table
- `piVar21[0x129]` - User list
- `piVar21[0x12e]` - Roster complete callback
- `piVar21[0x136]` - User add callback

---

## Validation Status

| Item | Status |
|------|--------|
| Wire format (12-byte header) | ✓ Validated |
| LobbyApi commands | ✓ Validated (18 commands) |
| BuddyApi commands | ✓ Validated (10 commands) |
| Key-value format | ✓ Validated |
| Command hex values | ✓ All match |
