# LobbyApiUpdate Function Analysis

## Overview
- **Address**: 0x0031bdf0
- **Size**: 6412 bytes (10232 instructions)
- **Basic Blocks**: 100+
- **Purpose**: Main message processing/dispatch function for lobby system

---

## Function Signature
```
fcn.0031bdf0(arg1, arg2, arg4, arg3)
- Uses 23 local variables (sp[0x10..0x410])
- Returns: int32 status code
```

---

## Message Dispatch Architecture

### Dispatch Table Location
- **Address**: 0x003da378
- **Type**: Sorted string table with hash-based dispatch
- **Format**: 4-byte message type + branch instruction to handler

### Message Type Table (Sorted)
| Offset | Type | Handler Branch |
|--------|------|----------------|
| 0x003da378 | ADDR | 0x003eb480 |
| 0x003da380 | ROOM | 0x003eb8ec |
| 0x003da388 | EWBC | - |
| 0x003da390 | PRIV | 0x003eecd4 |
| 0x003da398 | TEXT | - |
| 0x003da3a0 | ATTR | - |
| 0x003da3a8 | PERS | 0x003eb8ec |
| 0x003da3b0 | HOST | - |
| 0x003da3b8 | BLOC | - |
| 0x003da3c0 | DECL | - |
| 0x003da3c8 | ACPT | - |

### Dispatch Algorithm
1. Extract 4-byte message type from incoming packet
2. Hash lookup via `fcn.002b8be8` (132 xrefs - hash table lookup)
3. Binary search through sorted type table
4. Jump to handler if found
5. Return error code if not found

---

## Call Graph

### External Calls from LobbyApiUpdate

| Address | Function | Purpose |
|---------|----------|---------|
| 0x00319838 | fcn.00319838 | Key=value parser (called ~20x) |
| 0x00319658 | fcn.00319658 | Message builder (builds outgoing "mg" messages) |
| 0x00319628 | fcn.00319628 | Helper function (called ~5x) |
| 0x00319840 | fcn.00319840 | Unknown helper |
| 0x00319f30 | fcn.00319f30 | Key=value parsing loop |
| 0x003197a0 | fcn.003197a0 | Unknown helper |
| 0x002b8be8 | fcn.002b8be8 | Hash table lookup (message dispatch) |

### Helper Function: fcn.00319838 (Key=Value Parser)
- **Size**: 8 bytes
- **Purpose**: Parses key=value pairs from message body
- Called extensively throughout LobbyApiUpdate
- Uses GP-relative addressing for lookup tables

### Helper Function: fcn.00319658 (Message Builder)
- **Size**: 196 bytes
- **Purpose**: Builds outgoing messages with "mg" type prefix
- Constructs protocol messages with key=value format
- References "Public_Key" at 0x3df2b8

### Helper Function: fcn.00319628 (Helper)
- **Size**: ~100 bytes
- **Purpose**: Unknown - called in message building loops
- Uses GP-relative addressing

### Helper Function: fcn.002b8be8 (Hash Table Lookup)
- **XRefs**: 132 (heavily used)
- **Purpose**: Hash-based dispatch table lookup
- Algorithm: Computes hash of message type string, looks up handler

---

## Control Flow Structure

### Phase 1: Initialization (0x0031bdf0 - 0x0031be98)
```
- Setup local variable space (sp -= 0x410)
- Initialize key=value parser state
- Setup message parsing context at s0+0x158, 0x16c, 0x174, 0x17c
```

### Phase 2: Message Type Hash Lookup (0x0031bf48 - 0x0031bfb8)
```
- Load message type from buffer
- Call fcn.002b8be8 (hash table lookup)
- Compare against known types using binary search
- Dispatch to appropriate handler
```

### Phase 3: Message Parsing Loop (0x0031bfb8 - 0x0031c000)
```
- Parse key=value pairs using fcn.00319838 and fcn.00319f30
- Loop through message body
- Build parsed data structure
```

### Phase 4: Response Building (0x0031c000 - 0x0031c0e8)
```
- Build "mg" response message using fcn.00319658
- "mg" string built at: 0x51a0 = "mg" (0x676d)
- Encode status codes
- Prepare outgoing buffer
```

### Phase 5: Error Handling (0x0031c0c8 - 0x0031c138)
```
- If message type not found, send "DOWN" message
- "DOWN" string at 0x0031c144
- Build error response with fcn.00319658
```

### Phase 6: Cleanup and Return (0x0031c138+)
```
- Restore saved registers
- Return status code
```

---

## Key Data Structures

### Buffer Layout (s0 register points to message buffer)
```
s0+0x10  : Return address
s0+0x158 : Parser state area 1
s0+0x16c : Parser state area 2  
s0+0x174 : Parser state area 3
s0+0x17c : Parser state area 4
s0+0x180 : Message type (4 bytes)
s0+0x184 : Body length
s0+0x188 : Flags
s0+0x18f : Body data (key=value pairs)
```

### Message Header (12 bytes)
```
Offset 0x00 (4 bytes): Message type (e.g., "AUTH", "skey", "ROOM")
Offset 0x04 (4 bytes): Body length (little-endian uint32)
Offset 0x08 (4 bytes): Flags/unknown
Offset 0x0c+    : Body (key=value\x00 pairs)
```

---

## String References Found

| Address | String | Usage |
|---------|--------|-------|
| 0x003da308 | PASS | Password field |
| 0x003da300 | PASS | Protocol field |
| 0x003da2e0 | LKEY | License key field |
| 0x003da2f4 | TOS | Terms of service |
| 0x003da2f8 | NAME | Username field |
| 0x003da310 | DESC | Description field |
| 0x003da3a8 | PERS | Personal info field |
| 0x003da3b0 | HOST | Host field |
| 0x003da3c8 | ACPT | Accept message |
| 0x0031c144 | "DOWN" | Error/status |
| 0x3df2b8 | "Public_Key" | Crypto reference |

---

## Message Response Format

### Outgoing "mg" Message
```
4 bytes: "mg" (0x676d) 
4 bytes: Length
4 bytes: Status/flags
N bytes: key=value pairs
```

### Error Response "DOWN"
```
Similar format with "DOWN" type
Contains error details in body
```

---

## Critical Code Patterns

### Message Building Pattern
```c
// Build "mg" message prefix
fcn.00319658(buffer, msg_type);
// Then append key=value pairs
```

### Key=Value Parsing Pattern
```c
// Parse loop
do {
    result = fcn.00319838(buffer, state);
    if (result == 0) break;
    // Process key=value
} while (1);
```

### Hash Table Dispatch Pattern
```c
// Hash lookup
handler = fcn.002b8be8(msg_type, hash_table);
// Jump to handler
if (handler >= 0) {
    call handler;
} else {
    // Send "DOWN" error
}
```

---

## Constants and Magic Values

| Value | Location | Meaning |
|-------|----------|---------|
| 0x1c (28) | 0x00319658 | Header prefix size? |
| 0xff | Various | Padding/mask value |
| 0x2000 | 0x0031bf54 | Flag mask |
| 0xfff | 0x0031bf5c | Bitmask for flags |
| 0x7ffc | 0x0031c174 | Mask value |

---

## Memory Offsets (from s0)

| Offset | Size | Purpose |
|--------|------|---------|
| +0x10 | 8 | Saved RA |
| +0x158 | 8 | Parser state 1 |
| +0x16c | 8 | Parser state 2 |
| +0x174 | 8 | Parser state 3 |
| +0x17c | 8 | Parser state 4 |
| +0x184 | 4 | Body length |
| +0x188 | 4 | Flags |
| +0x18f | N | Body data |

---

## Emulator Implementation Notes

### For Server Emulator
1. **Parse incoming**: Extract 4-byte type, 4-byte length, parse body
2. **Dispatch**: Use hash table lookup for message type routing
3. **Build response**: Use "mg" message builder pattern
4. **Error handling**: Send "DOWN" on invalid messages

### Protocol Fields to Handle
- ADDR: Connection info
- ROOM: Room list, creation, joining
- PERS: Player personal data
- HOST: Game host status
- PRIV: Private messages (buddy system)
- EWBC: Wait for buddy change
- TEXT: Text messages
- ATTR: Room attributes
- BLOC: Block user
- DECL: Decline
- ACPT: Accept

### Key Parsing
The key=value parsing happens in fcn.00319838/fcn.00319f30 which:
1. Scans for '=' character
2. Extracts key string
3. Extracts value string  
4. Returns pair to caller

---

## Gaps Requiring Further Analysis

1. **fcn.00319840** - Full purpose unknown
2. **fcn.003197a0** - Called in error path, purpose unknown
3. **fcn.00319f30** - Key=value parsing loop, full implementation unknown
4. **Crypto handling** - Public_Key referenced but not fully traced
5. **Session management** - skey validation logic not found
6. **Room state machine** - Exact room join/leave protocol unknown
7. **Handler addresses** - Actual handler function code not yet located

---

## Next Analysis Steps

1. Trace handler function code from dispatch table branches
2. Analyze database query functions (SQL references found in strings)
3. Map lobby state machine transitions
4. Document challenge-response authentication flow
5. Analyze network send/receive loop

---

*Generated from radare2 analysis of NASCAR.ELF*
*Analysis date: 2025*
