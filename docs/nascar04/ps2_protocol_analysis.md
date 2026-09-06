# PS2 EA Protocol Binary Analysis

## Executive Summary

Analysis of NASCAR.ELF (PS2) reveals a complex multiplayer protocol system with multiple service types. The game uses a custom key=value message protocol over TCP for game lobby and buddy presence services.

---

## 1. Network Architecture

### Server Endpoints (Validated)

| Address | Port | Service | Protocol |
|---------|------|---------|----------|
| `ps2nascar04.ea.com` (0x003dabf8) | 10600 | Directory Server | Custom KV |
| `ps2nascar04.ea.com` (0x003dabf8) | 10901 | Login Server | Custom KV |
| `buddy.ea.com` (0x003e0cf8) | 10899 | Buddy Server | Custom KV |
| 0x003e1335 | 6667 | Chat (IRC-style) | IRC-like |

### Service Path
```
/cso/nascar-ps2-2004
```

---

## 2. Message Protocol Format

### Wire Format
```
[4 bytes: msg_type] [4 bytes: body_len] [4 bytes: flags?] [body: key=value\x00...]
```

### 12-Byte Header
- **Bytes 0-3**: Message type (4 ASCII chars, e.g., "AUTH", "skey")
- **Bytes 4-7**: Body length (little-endian uint32)
- **Bytes 8-11**: Flags/unknown

### Body Format
```
key1=value1\x00key2=value2\x00...\x00\x00
```

---

## 3. Message Type Dispatch Table

**Location**: 0x003da378 (sorted lookup table for Buddy/Chat server)

| Type | Offset | Description |
|------|--------|-------------|
| ADDR | 0x003da378 | Address/connection info |
| ROOM | 0x003da380 | Room management |
| EWBC | 0x003da388 | Wait for buddy change? |
| PRIV | 0x003da390 | Private message |
| TEXT | 0x003da398 | Text message |
| ATTR | 0x003da39c | Attribute update |
| PERS | 0x003da3a8 | Personal info |
| HOST | 0x003da3b0 | Host status |
| BLOC | 0x003da3b8 | Block user |
| DECL | 0x003da3c0 | Decline request |
| ACPT | 0x003da3c8 | Accept request |

---

## 4. Protocol Field Keys

**Location**: 0x003da2e0

### Authentication Fields
| Key | Location | Purpose |
|-----|----------|---------|
| LKEY | 0x003da2e0 | License key |
| PASS | 0x003da300 | Password |
| TOS | 0x003da2f4 | Terms of Service acceptance |
| NAME | 0x003da2f8 | Username |

### User Profile Fields
| Key | Location | Purpose |
|-----|----------|---------|
| PERS | 0x003da308 | Personal descriptor |
| DESC | 0x003da310 | Description |
| NONE | 0x003da318 | No value field |

### Game/Room Fields
| Key | Location | Purpose |
|-----|----------|---------|
| MAX | 0x003da320 | Maximum rooms |
| TITL | 0x003da330 | Title |
| STAT | Various | Status |
| TSRD | DB query | Track session data |

### Chat/Presence Fields
| Key | Location | Purpose |
|-----|----------|---------|
| PING | 0x003da4e4 | Keepalive |
| PONG | - | Keepalive response |
| AUTH | 0x003dba48 | Auth message |
| SEND | - | Send message |
| mesg | - | Message |

---

## 5. Database Schema (TSRD Table)

Based on SQL query analysis in binary:

### TSRD Table Fields
```
TSRD.DIRD  -- Driver ID
TSRD.RAEY  -- Race year?
TSRD.RTSR  -- Race time?
TSRD.KNRC  -- Rank
TSRD.TNPC  -- Total pits/crashes
TSRD.NIWC  -- Wins count
TSRD.NIWN  -- Wins (alternate)
TSRD.LOPN  -- Laps?
TSRD.DLLN  -- DLL name?
TSRD.DPST  -- Display?
TSRD.PALN  -- Palette?
TSRD.SPST  -- Speed status?
TSRD.SPFT  -- Speed font?
TSRD.PNFB  -- Points for?
TSRD.5POT  -- 5 points?
TSRD.01PT  -- 01 points?
TSRD.SNWW  -- Something wins?
TSRD.NRAE  -- NRAE?
```

### SQL Query Pattern
```sql
SELECT TSRD.DIRD, TSRD.RAEY, ... 
FROM TSRD 
INNER JOIN SRAC ON ...
INNER JOIN RVRD ON ...
```

### Related Tables
- **SRAC** - Driver/career stats
- **DIRD** - Driver info
- **DIRC** - Driver configuration
- **RVRD** - Racing records
- **FNIG** - Figure?
- **DHCS** - 
- **DICS** -
- **LPSC** - ?

---

## 6. Key Functions

### Network Receive/Command Dispatcher
- **Address**: 0x001012c8
- **Size**: 316 bytes
- **Purpose**: Initial message routing

### Lobby API Update
- **Address**: 0x0031bdf0
- **Size**: 6412 bytes
- **Purpose**: Main message processing logic
- **Calls**: fcn.00319838 (key=value parsing)

### Connection Logging
- **Address**: 0x003e1238
- **String**: `connecting to %08x:%d`
- **Purpose**: Log server connection attempts

---

## 7. Protocol State Machine

### Connection Flow
```
1. TCP Connect to Dir Server (10600)
2. Send "addr" with server info
3. Receive server list
4. TCP Connect to Login Server (10901)
5. Send "LKEY" + "PASS" for auth
6. Receive "skey" session key
7. Browse rooms, join/create
8. Optionally connect to Buddy Server (10899)
9. Maintain with PING/PONG
10. Disconnect with "bye"
```

### Buddy Server Flow
```
1. Connect to buddy.ea.com:10899
2. Send AUTH message
3. Receive challenge
4. Send PSET for presence
5. RGET for roster
6. Handle PRIV/TEXT messages
7. Send/receive mesg
8. PING keepalive
```

---

## 8. Unknown/Gap Analysis

### Missing Protocol Details
1. **Challenge-Response**: Key field format unknown
2. **Session Key**: skey format/validation unknown
3. **Crypto**: Encryption algorithm unknown (if any)
4. **Room Join**: Complete room protocol unknown
5. **Buddy List**: RGET response format unknown

### Functions Needing Analysis
- fcn.00319838 - Key=value parser
- fcn.00319658 - Message builder
- fcn.00319628 - Unknown helper
- fcn.002b8be8 - Called from LobbyApiUpdate

---

## 9. Recommendations for Emulator

### Priority Implementation
1. ✅ Dir Server handshake (@addr)
2. ✅ Login auth (LKEY/PASS)
3. ⚠️ Session key (skey) handling
4. ⚠️ PING keepalive
5. ❌ Challenge-response crypto
6. ❌ Full buddy presence system

### Security Considerations
- No evidence of TLS/encryption on PS2 protocol
- Session likely validated by skey only
- No certificate validation observed

---

## 10. Binary Validation Summary

| Item | Address | Status |
|------|---------|--------|
| Server hostname | 0x003dabf8 | ✅ Validated |
| Service path | 0x003d997d | ✅ Validated |
| Dir Server port | 10600 | ✅ Found |
| Login Server port | 10901 | ✅ Found |
| Buddy Server URL | 0x003e0cf8 | ✅ Found |
| Buddy Server port | 10899 | ✅ Found |
| Chat port | 6667 | ✅ Found |
| Message types | 0x003da378 | ✅ Mapped |
| Protocol fields | 0x003da2e0 | ✅ Mapped |
| SQL schema | Various | ✅ Documented |

---

*Generated from binary analysis of NASCAR.ELF*
