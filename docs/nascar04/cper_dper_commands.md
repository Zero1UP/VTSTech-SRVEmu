# cper/dper Commands - NASCAR.ELF

## Overview

`cper` and `dper` are client-only (outbound) commands for persona management.

## cper (0x63706572) - Create Persona

**ASCII**: `cper`  
**Direction**: Client → Server (outbound only)  
**Purpose**: Create a new alternate persona

### Client Request Payload
```
Type:   0x63706572 (cper)
Flags:  0x00000000
Length: Variable
Payload:
PERS=<persona_name>\x00
```

### Server Response
```
Type:   0x63706572 (cper)
Flags:  0x00000000  
Length: Variable
Payload:
PERS=<created_persona>\x00
ALTS=<total_alternates>\x00
STATUS=<1=success, 0=failure>\x00
```

---

## dper (0x64706572) - Delete Persona

**ASCII**: `dper`  
**Direction**: Client → Server (outbound only)  
**Purpose**: Delete an alternate persona

### Client Request Payload
```
Type:   0x64706572 (dper)
Flags:  0x00000000
Length: Variable
Payload:
PERS=<persona_to_delete>\x00
```

### Server Response
```
Type:   0x64706572 (dper)
Flags:  0x00000000  
Length: Variable
Payload:
PERS=<deleted_persona>\x00
ALTS=<remaining_alternates>\x00
STATUS=<1=success, 0=failure>\x00
```

---

## Confirmed Fields

| Field | Type | Description |
|-------|------|-------------|
| PERS | String | Persona name |
| ALTS | Int | Alternate persona count |
| STATUS | Int | 1=success, 0=failure |

---

## Implementation Notes

1. **No binary handler**: These are outbound commands - the PS2 client sends them but doesn't receive handlers
2. **Server must implement**: The server emulator must handle these commands
3. **Max personas**: Typically limited to 4 personas per account
4. **ALTS field**: Returns the total number of alternate personas after the operation
5. **Cannot delete primary**: The primary persona (usually same as username) cannot be deleted

---

## Related Commands

| Command | Hex | Purpose |
|---------|-----|---------|
| pers | 0x70657273 | Persona selection |
| acct | 0x61636374 | Account operations |

---

## See Also

- `/docs/master_command_list.md` - Full command documentation
- `/docs/command_inventory.md` - Command inventory
