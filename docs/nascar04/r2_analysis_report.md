# Radare2 Analysis Report - NASCAR.ELF

## Overview
Analysis of NASCAR.ELF using Radare2 (`pdcc` command) to extract protocol commands from disassembly.

## Environment
```bash
LD_LIBRARY_PATH=/home/vtstech/workspace/lib /home/vtstech/workspace/r2.sh
```

## Commands Used
```bash
# Load binary
L nascar

# Analyze function
s 0x0031bdf0
af

# Disassemble with pdcc for pseudo-C output
pdcc

# Or raw disassembly
pd 2000
```

## Commands Discovered in LobbyApiUpdate (0x0031bdf0)

### Valid Protocol Commands (from assembly analysis)

| Hex | Command | Description |
|-----|---------|-------------|
| 0x61636374 | acct | Account |
| 0x61646472 | addr | Client address response |
| 0x61757468 | auth | Authentication |
| 0x63686174 | chat | Chat message |
| 0x6D6F7665 | move | Room move |
| 0x70657273 | pers | Persona |
| 0x73656C65 | sel~ | Select (variant) |
| 0x736B6579 | skey | Session key |
| 0x736E6170 | snap | Snapshot |
| 0x726F6F6D | room | Room message |

### Internal States (not protocol commands)

| Hex | State | Purpose |
|-----|-------|---------|
| 0x636F6E6E | conn | Connection state |
| 0x69646C65 | idle | Idle/authenticated state |
| 0x6F66666C | offl | Offline state |
| 0x7465726D | term | Terminate state |
| 0x72646972 | rdir | Redirect pending state |
| 0x74696D65 | time | Timer/state check |

## Command Dispatch Structure

From `pdcc` output, the LobbyApiUpdate function:

1. Loads message type from structure (offset 0x0C)
2. Compares against known command values
3. Branches to appropriate handler
4. Falls through if no match

Example dispatch pattern:
```c
// Load command from message
a0 = [s2 + 0x0C]

// Compare against "offl"
lui v0, 0x6f66
ori v0, v0, 0x666c
beq a0, v0, 0x31be98

// Compare against "term"
lui v0, 0x7465
ori v0, v0, 0x726d
beq a0, v0, 0x31be98

// etc.
```

## Key Findings

1. **Command strings are built at runtime** using lui/ori MIPS instruction pairs
2. **String table at 0x003d8378** contains BuddyApi commands (ADDR, ROOM, PRIV, etc.)
3. **LobbyApiUpdate at 0x0031bdf0** handles LobbyApi protocol commands
4. **NetworkEvent_MainDispatcher** routes to appropriate subsystem

## Using r2 Effectively

### Recommended Workflow

1. **Load binary and create project**
```bash
r2 -w NASCAR.ELF
# Then in r2:
L nascar
aa
```

2. **Analyze specific function**
```bash
s 0x0031bdf0
af
```

3. **Get disassembly**
```bash
pd 200
```

4. **Get pseudo-C (limited)**
```bash
pdcc | head -100
```

5. **Search for strings**
```bash
[0x0031bdf0]> / search
iz
```

6. **Find cross-references**
```bash
[0x0031bdf0]> axt 0x003d8378
```

## Limitations

- `pdcc` output is not as readable as Ghidra decompilation
- ESIL emulation provides limited decompilation
- Better to use Ghidra for high-level analysis
- Use r2 for:
  - Quick disassembly checks
  - Cross-reference analysis
  - Binary patching
  - Finding string references

## See Also

- `/analysis/decompiled/` - Ghidra decompiled functions
- `/docs/master_command_list.md` - Complete command inventory
- `/docs/buddy_api_reference.md` - BuddyApi protocol details
