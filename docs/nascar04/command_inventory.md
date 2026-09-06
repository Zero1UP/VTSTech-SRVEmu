# Command Inventory

**Source Analysis**: Binary string tables + decompiled code + user knowledge  
**Date**: September 6, 2026

---

## Complete Command List

### LobbyApi Commands

| Command | Hex (BE) | Direction | Description |
|---------|----------|-----------|-------------|
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
| ping | 0x7E706E67 | Bidirectional | Ping (~png) |
| @dir | 0x40646972 | Server→Client | Direct connection redirect |
| move | 0x6D6F7665 | Client→Server | Room move |
| room | 0x726F6F6D | Bidirectional | Room message |
| addr | 0x61646472 | Client→Server | Client address response |
| chal | 0x6368616C | Bidirectional | Challenge command |
| auxi | 0x61757869 | Bidirectional | Auxiliary/Status |
| peek | 0x7065656B | Bidirectional | Peek command |

**Total LobbyApi**: 22 commands

### BuddyApi Commands (from binary at 0x003d8378)

| Command | Hex (BE) | Description |
|---------|----------|-------------|
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

**Total BuddyApi**: 11 commands

### Network Commands (sent by client only)

| Command | Hex (BE) | Direction | Description |
|---------|----------|-----------|-------------|
| PING | 0x50494E47 | Client→Server | Keepalive |
| AUTH | 0x41555448 | Client→Server | Auth request |
| RECV | 0x52454356 | Client→Server | Receive data request |
| SEND | 0x53454E44 | Client→Server | Send data |
| ADMN | 0x41444D4E | Client→Server | Admin |
| PGET | 0x50474554 | Client→Server | Player get |
| RGET | 0x52474554 | Client→Server | Roster get |
| ROST | 0x524F5354 | Client→Server | Roster update |
| RADD | 0x52414444 | Client→Server | Roster add |
| RDEL | 0x5244454C | Client→Server | Roster delete |
| **dper** | 0x64706572 | Client→Server | **Delete persona** |
| **cper** | 0x63706572 | Client→Server | **Create persona** |

**Note**: cper and dper are outbound-only commands sent by the client. They may not have handlers in the binary since they're client-generated.

**Total Network**: 12 commands

---

## Summary

| Category | Count |
|----------|-------|
| LobbyApi | 22 |
| BuddyApi | 11 |
| Network | 12 |
| **Total** | **45** |

---

## Command Direction Key

| Direction | Meaning |
|-----------|---------|
| Client→Server | Sent by PS2 client only |
| Server→Client | Sent by server only |
| Bidirectional | Can be sent by either |

---

## Internal State Codes (NOT Protocol Commands)

| State | Hex | Purpose |
|-------|-----|---------|
| conn | 0x636F6E6E | Connection state |
| idle | 0x69646C65 | Idle |
| offl | 0x6F66666C | Offline |
| term | 0x7465726D | Terminate |
| rdir | 0x72646972 | Redirect pending |

---

## Binary String Tables

| Location | Contents |
|----------|----------|
| 0x003d8378 | BuddyApi commands (11 strings) |
| 0x003d8400 | Challenge-related strings, profanity filter |
| 0x003d83e8 | IP format string ("%d.%d.%d.%d:%d") |
