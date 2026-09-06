# Undocumented Commands Analysis

**Source**: LobbyApiUpdate decompilation (0x0031bdf0)  
**Date**: September 6, 2026

---

## Newly Documented Commands

### `addr` - Client Address Response

**Hex**: 0x61646472  
**ASCII**: `addr`  
**Direction**: Client → Server  
**Purpose**: Client sends its own IP/port in response to `@dir`

**Flow**:
1. Server sends `@dir` with redirect info
2. Client responds with `addr` containing its reachable address

**Payload Fields**:
| Field | Type | Description |
|-------|------|-------------|
| ADDR | IP | Client's reachable IP address |
| PORT | Int | Client's port number |

**Example**:
```
ADDR=192.168.1.100\x00PORT=3654\x00
```

---

## Internal State Codes (NOT Commands)

These are internal state values, not protocol commands:

| State | Hex | Description |
|-------|-----|-------------|
| rdir | 0x72646972 | Redirect state - awaiting @dir |
| conn | 0x636f6e6e | Connected state |
| idle | 0x69646c65 | Idle state |
| offl | 0x6f66666c | Offline state |
| term | 0x7465726d | Terminate state |
| time | 0x74696d65 | Timeout indicator |

---

## Field Keys Referenced in Code

These field keys are used internally but not all are documented:

| Key | Hex | Used In | Description |
|-----|-----|---------|-------------|
| NET_Field3 | - | addr, @dir | Address field |
| LOBBY_PortField | - | addr, @dir | Port field |
| LOBBY_DirectField | - | @dir handling | Direct connection flag |
| LOBBY_SessionField | - | @dir handling | Session ID |
| NET_StatusField | - | @dir handling | Status string |
| ladr | 0x6c616472 | - | Local address param |
| lprt | 0x6c707274 | - | Local port param |

---

## Connection Flow States

```
Initial → conn → skey → idle → auth → acct → Sele → pers → conn
                    ↓
                  @dir → addr → conn
```

State transitions are tracked in `piVar24[3]`:
- 0x636f6e6e (conn) - Connected, awaiting data
- 0x72646972 (rdir) - Ready to receive redirect
- 0x736b6579 (skey) - Session key exchange
- 0x69646c65 (idle) - Idle, authenticated
- 0x61757468 (auth) - Authenticating
- 0x61636374 (acct) - Account check
- 0x73656c65 (sele) - Selection phase
- 0x70657273 (pers) - Persona selection
