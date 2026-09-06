# Master Command List - NASCAR.ELF

**Source**: Ghidra decompilation + server implementation validation  
**Date**: September 6, 2026

---

## Wire Format

```
Offset 0x00: 4 bytes - Message Type (BIG-ENDIAN)
Offset 0x04: 4 bytes - Flags (BIG-ENDIAN)
Offset 0x08: 4 bytes - Length (BIG-ENDIAN, includes header)
Offset 0x0C: N bytes - Payload (KEY=value\x00 pairs)
```

---

## Protocol Field Keys

| Key | Type | Description |
|-----|------|-------------|
| A | Int | IP address (integer) |
| DESC | String | Description |
| F | String | Flags |
| H | String | Heading |
| HI | Int | Room index (Lobby) |
| I | Int | User/Room ID |
| JI | Int | Room index |
| L | Int | Limit (max users) |
| N | String | Name |
| NAME | String | Name |
| NI | Int | Room index |
| P | String | Password |
| PASS | String | Password |
| PERS | String | Persona |
| PI | Int | Room index |
| PROD | String | Product |
| R | String | Rank value |
| RI | Int | Room ID |
| RF | String | Rank flag |
| RT | String | Room type |
| S | String | Status/string |
| SLUS | String | Game SKU |
| ST | String | Status |
| T | Int | Type |
| U | String | Unknown |
| USER | String | Username |
| VERS | String | Version |
| Z | String | Room:count pairs |

---

## LobbyApi Commands

**Handler**: `LobbyApiUpdate` (0x0031bdf0)

---

### Command: auth (0x61757468)

Authentication request.

**Parameters**:
| Key | Required | Description |
|-----|----------|-------------|
| USER | Yes | Username |
| PASS | Yes | Password |
| PROD | Yes | Product (e.g., "NASCAR") |
| VERS | Yes | Version string |

**Packet Example**:
```
// auth request (type=auth)
61 75 74 68  00 00 00 00  1D 00 00 00
55 53 45 52 3D 74 65 73 74 00  // USER=test\x00
50 41 53 53 3D 70 77 64 00  // PASS=pwd\x00
50 52 4F 44 3D 4E 41 53 43 41 52 00  // PROD=NASCAR\x00
```

---

### Command: skey (0x736B6579)

Session key validation.

**Parameters**:
| Key | Required | Description |
|-----|----------|-------------|
| SKEY | Yes | Session key |

**Packet Example**:
```
// skey request
73 6B 65 79  00 00 00 00  12 00 00 00
53 4B 45 59 3D 41 42 43 44 45 46 47 00  // SKEY=ABCDEFG\x00
```

---

### Command: pers (0x70657273)

Persona selection.

**Parameters**:
| Key | Required | Description |
|-----|----------|-------------|
| PERS | Yes | Persona name |

**Packet Example**:
```
// pers request
70 65 72 73  00 00 00 00  0F 00 00 00
50 45 52 53 3D 52 61 63 65 72 00  // PERS=Racer\x00
```

---

### Command: news (0x6E657773)

Request news/room list.

**Parameters**:
| Key | Required | Description |
|-----|----------|-------------|
| NAME | Yes | Usually "0" for full news |

**Packet Example**:
```
// news request
6E 65 77 73  00 00 00 00  09 00 00 00
4E 41 4D 45 3D 30 00  // NAME=0\x00
```

---

### Command: move (0x6D6F7665)

Join a room.

**Parameters**:
| Key | Required | Description |
|-----|----------|-------------|
| NAME | Yes | Room name |
| PASS | No | Room password |

**Packet Example**:
```
// move request (join room "East")
6D 6F 76 65  00 00 00 00  0D 00 00 00
4E 41 4D 45 3D 45 61 73 74 00  // NAME=East\x00
```

**Server Response**:
```
// move response
6D 6F 76 65  00 00 00 00  1B 00 00 00
53 3D 31 00  // S=1\x00
4E 3D 45 61 73 74 00  // N=East\x00
46 3D 30 00  // F=0\x00
```

---

### Command: room (0x726F6F6D)

Room info request.

**Parameters**:
| Key | Required | Description |
|-----|----------|-------------|
| NAME | Yes | Room name |

**Packet Example**:
```
// room request
72 6F 6F 6D  00 00 00 00  0D 00 00 00
4E 41 4D 45 3D 45 61 73 74 00  // NAME=East\x00
```

---

## Server Push Commands

These are sent from server to client.

---

### Command: +who (0x2B77686F)

User's own presence info (sent after pers).

**Keys**:
| Key | Description |
|-----|-------------|
| F | Flags (friend status) |
| N | Username |
| RI | Room index |
| RT | Room type |
| R | Rank |
| RF | Rank flag |

**Packet Example**:
```
// +who push
2B 77 68 6F  00 00 00 00  1C 00 00 00
46 3D 55 00  // F=U\x00
4E 3D 74 65 73 74 00  // N=test\x00
52 49 3D 30 00  // RI=0\x00
52 54 3D 34 00  // RT=4\x00
52 3D 30 00  // R=0\x00
52 46 3D 30 00  // RF=0\x00
```

---

### Command: +rom (0x2B726F6D)

Room listings (sent after news).

**Keys**:
| Key | Description |
|-----|-------------|
| I | Room ID/index |
| N | Room name |
| H | Heading/description |
| A | Address (integer) |
| T | Type (1=Lobby, 0=other) |
| L | Limit (max users) |
| F | Flags |

**Packet Example**:
```
// +rom push (Lobby room)
2B 72 6F 6D  00 00 00 00  31 00 00 00
49 3D 30 00  // I=0\x00
4E 3D 4C 6F 62 62 79 00  // N=Lobby\x00
48 3D 4D 61 69 6E 20 4C 6F 62 62 79 20 48 75 62 00  // H=Main Lobby Hub\x00
41 3D 43 37 46 45 30 30 30 00  // A=C7FE0000\x00 (hex IP)
54 3D 31 00  // T=1\x00 (Lobby)
4C 3D 31 30 30 00  // L=100\x00
46 3D 30 00  // F=0\x00
```

---

### Command: +usr (0x2B757372)

User info in room.

**Keys**:
| Key | Description |
|-----|-------------|
| I | User ID |
| N | Username |
| A | IP address (integer) |
| F | Flags |
| S | Status text |
| P | Password (empty) |

**Packet Example**:
```
// +usr push
2B 75 73 72  00 00 00 00  2C 00 00 00
49 3D 31 32 33 34 35 36 00  // I=123456\x00
4E 3D 74 65 73 74 00  // N=test\x00
41 3D 43 37 46 45 30 30 30 00  // A=C7FE0000\x00
46 3D 31 00  // F=1\x00
53 3D 4F 6E 6C 69 6E 65 00  // S=Online\x00
50 3D 00  // P=\x00
```

---

### Command: +pop (0x2B706F70)

Population counts per room.

**Keys**:
| Key | Description |
|-----|-------------|
| Z | Room:count pairs (e.g., "0:1 1:0 2:0 3:0") |

**Packet Example**:
```
// +pop push
2B 70 6F 70  00 00 00 00  15 00 00 00
5A 3D 30 3A 31 20 31 3A 30 20 32 3A 30 20 33 3A 30 00  // Z=0:1 1:0 2:0 3:0\x00
```

---

### Command: +snp (0x2B736E70)

Snapshot broadcast.

**Keys**:
| Key | Description |
|-----|-------------|
| S | Status value |
| ... | Additional fields |

**Packet Example**:
```
// +snp push
2B 73 6E 70  00 00 00 00  09 00 00 00
53 3D 30 00  // S=0\x00
```

---

### Command: snap (0x736E6170)

Snapshot request.

**Packet Example**:
```
// snap request
73 6E 61 70  00 00 00 00  09 00 00 00
53 3D 30 00  // S=0\x00
```

---

## BuddyApi Commands

**Handler**: `BuddyApiUpdate` (0x00362020)

### Command: PING (0x50494E47)

Ping request. Server echoes back.

**Packet Example**:
```
// PING request → response is identical
50 49 4E 47  00 00 00 00  08 00 00 00
```

---

### Command: AUTH (0x41555448)

Authentication.

**Keys**:
| Key | Required | Description |
|-----|----------|-------------|
| USER | Yes | Username |
| PERS | Yes | Persona |
| LKEY | Yes | Login key |

**Packet Example**:
```
// AUTH request
41 55 54 48  00 00 00 00  20 00 00 00
55 53 45 52 3D 74 65 73 74 00  // USER=test\x00
50 45 52 53 3D 52 61 63 65 72 00  // PERS=Racer\x00
4C 4B 45 59 3D 41 42 43 44 00  // LKEY=ABCD\x00
```

---

### Command: ROST (0x524F5354)

Roster update.

**Keys**:
| Key | Required | Description |
|-----|----------|-------------|
| TYPE | Yes | 1=add/update, 2=remove |
| USER | Yes | Username |
| NICK | No | Nickname |
| GROUP | No | Group name |

**Packet Examples**:
```
// ROST - user add (TYPE=1)
52 4F 53 54  00 00 00 00  1D 00 00 00
54 59 50 45 3D 31 00  // TYPE=1\x00
55 53 45 52 3D 6A 6F 65 00  // USER=joe\x00

// ROST - roster end (TYPE=2)
52 4F 53 54  00 00 00 00  09 00 00 00
54 59 50 45 3D 32 00  // TYPE=2\x00
```

---

### Command: RADD (0x52414444)

Add/update roster entry.

**Keys**:
| Key | Required | Description |
|-----|----------|-------------|
| USER | Yes | Username |
| NICK | No | Nickname |
| GROUP | No | Group name |

**Packet Example**:
```
// RADD request
52 41 44 44  00 00 00 00  1A 00 00 00
55 53 45 52 3D 6A 6F 65 00  // USER=joe\x00
4E 49 43 4B 3D 4A 4F 45 00  // NICK=JOE\x00
```

---

### Command: RDEL (0x5244454C)

Delete roster entry.

**Keys**:
| Key | Required | Description |
|-----|----------|-------------|
| TYPE | Yes | Delete type |

**Packet Example**:
```
// RDEL request
52 44 45 4C  00 00 00 00  09 00 00 00
54 59 50 45 3D 31 00  // TYPE=1\x00
```

---

## Directory Server Messages

---

### Request: @dir

**Parameters**:
| Key | Required | Description |
|-----|----------|-------------|
| PROD | Yes | Product (e.g., "NASCAR") |
| VERS | Yes | Version |
| LANG | No | Language |
| SLUS | Yes | SKU |

**Packet Example**:
```
// @dir request
40 64 69 72  00 00 00 00  2E 00 00 00
50 52 4F 44 3D 4E 41 53 43 41 52 00  // PROD=NASCAR\x00
56 45 52 53 3D 31 2E 30 00  // VERS=1.0\x00
4C 41 4E 47 3D 45 4E 00  // LANG=EN\x00
53 4C 55 53 3D 53 4C 55 53 5F 32 30 38 2E 34 34 00  // SLUS=SLUS_208.44\x00
```

### Response: @dir

**Keys**:
| Key | Description |
|-----|-------------|
| ADDR | Login server IP |
| PORT | Login server port |
| LKEY | Session key |
| SESS | Session ID |
| MASK | Server mask |

**Packet Example**:
```
// @dir response
40 64 69 72  00 00 00 00  3B 00 00 00
41 44 44 52 3D 43 37 46 45 30 30 30 00  // ADDR=C7FE0000\x00
50 4F 52 54 3D 32 41 39 44 00  // PORT=2A9D\x00 (10637)
4C 4B 45 59 3D 54 45 53 54 4B 45 59 00  // LKEY=TESTKEY\x00
53 45 53 53 3D 31 32 33 34 00  // SESS=1234\x00
4D 41 53 4B 3D 46 46 46 46 00  // MASK=FFFF\x00
```

---

## Response Patterns

### Success Response
```
// addr response
61 64 64 72  00 00 00 00  0B 00 00 00
53 54 41 54 55 53 3D 31 00  // STATUS=1\x00
```

### Error Response (mgDOWN)
```
// error response
6D 67 44 4F 57 4E  00 00 00 00  12 00 00 00
45 52 52 3D 49 6E 76 61 6C 69 64 00  // ERR=Invalid\x00
```

---

## Notes

1. **Big-endian** byte order for multi-byte values
2. **Null-terminated** key-value pairs
3. **Field separator**: `=`
4. **IP addresses** stored as integer strings (not dotted notation)
5. **Room indices** are 0-based integers
6. **Length field** includes the 12-byte header

### IP Conversion

```python
# Dotted notation to integer
import socket
ip_int = int.from_bytes(socket.inet_aton("192.168.1.1"), 'big')
# Result: 0xC0A80101

# Integer to dotted notation
ip_str = socket.inet_ntoa(ip_int.to_bytes(4, 'big'))
```

---

## Additional Commands (from decompilation analysis)

### `addr` - Client Address Response

**Hex (BE)**: 0x61646472  
**ASCII**: `addr`  
**Direction**: Client → Server  
**Purpose**: Client sends its reachable IP/port after receiving `@dir`

**When Used**: After receiving `@dir` redirect, client responds with its address.

**Payload**:
| Field | Type | Description |
|-------|------|-------------|
| ADDR | String | Client's reachable IP (dotted notation) |
| PORT | Int | Client's port number |

**Server Response**: Connection continues with `conn` state

**Example**:
```
// Client receives @dir then responds:
Type=0x61646472, Flags=0, Length=36
Payload: ADDR=192.168.1.100\x00PORT=3654\x00
```

### Internal State Codes

These are NOT protocol commands but internal client states:

| State | Hex | Purpose |
|-------|-----|---------|
| conn | 0x636F6E6E | Connected state |
| rdir | 0x72646972 | Redirect pending |
| idle | 0x69646C65 | Authenticated, idle |
| skey | 0x736B6579 | Session key exchange |
| auth | 0x61757468 | Authentication |
| acct | 0x61636374 | Account check |
| Sele | 0x73656C65 | Selection phase |
| pers | 0x70657273 | Persona selection |

---

## Network Commands (Client → Server only)

**Handler**: ProtoAries layer (sent by client, no handler in binary)

---

### Command: cper (0x63706572)

Create persona request.

**Direction**: Client → Server (outbound only)

**Parameters**:
| Key | Required | Description |
|-----|----------|-------------|
| PERS | Yes | Persona name to create |

**Server Response**:
| Key | Description |
|-----|-------------|
| PERS | Created persona name |
| ALTS | Total alternate personas |
| STATUS | 1=success, 0=failure |

---

### Command: dper (0x64706572)

Delete persona request.

**Direction**: Client → Server (outbound only)

**Parameters**:
| Key | Required | Description |
|-----|----------|-------------|
| PERS | Yes | Persona name to delete |

**Server Response**:
| Key | Description |
|-----|-------------|
| PERS | Deleted persona name |
| ALTS | Remaining alternate personas |
| STATUS | 1=success, 0=failure |

---

### Command: PING (0x50494E47)

Keepalive ping.

**Note**: Outbound-only command sent periodically by client.

---

### Command: RECV (0x52454356)

Request to receive data.

**Note**: Outbound command to request data from server.

---

### Command: SEND (0x53454E44)

Send data to server.

**Note**: Outbound command for sending data.

---

### Command: ROST (0x524F5354)

Roster update.

**Note**: Outbound command for roster synchronization.

---

### Command: RADD (0x52414444)

Roster add user.

**Note**: Outbound command to add user to roster.

---

### Command: RDEL (0x5244454C)

Roster delete user.

**Note**: Outbound command to remove user from roster.
