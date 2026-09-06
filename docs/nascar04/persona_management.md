# Persona Management - NASCAR.ELF

## Overview

The NASCAR protocol supports multiple personas per account. Personas are alternate racing identities that can be created, deleted, and selected.

## Persona Commands

### pers (0x70657273) - Persona Selection

**Direction**: Bidirectional  
**Handler**: LobbyApiUpdate (0x0031bdf0)

The `pers` command is used to select a persona for the current session.

**Client Request**:
```
Type:   0x70657273 (pers)
Payload:
PERS=<persona_name>\x00
```

**Server Response**:
```
Type:   0x70657273 (pers)
Payload:
PERS=<persona_name>\x00
... additional persona data ...
```

---

### cper (0x63706572) - Create Persona

**Direction**: Client → Server (outbound only)

Creates a new alternate persona.

**Client Request**:
```
PERS=<new_persona_name>\x00
```

**Server Response**:
```
PERS=<created_persona>\x00
ALTS=<total_alternates>\x00
STATUS=<1=success, 0=failure>\x00
```

---

### dper (0x64706572) - Delete Persona

**Direction**: Client → Server (outbound only)

Deletes an alternate persona.

**Client Request**:
```
PERS=<persona_to_delete>\x00
```

**Server Response**:
```
PERS=<deleted_persona>\x00
ALTS=<remaining_alternates>\x00
STATUS=<1=success, 0=failure>\x00
```

---

## Persona Data Flow

```
1. Client logs in (auth)
2. Client receives persona list (acct response)
3. Client selects persona (pers)
4. Optional: Create persona (cper)
5. Optional: Delete persona (dper)
6. Optional: Switch persona (pers)
```

---

## Persona Limits

| Limit | Value |
|-------|-------|
| Max personas per account | 4 |
| Primary persona | Cannot be deleted |
| Persona name | String, max ~31 chars |

---

## Persona States

| State | Description |
|-------|-------------|
| Primary | Default persona (same as username) |
| Alternate | User-created personas |
| Active | Currently selected persona |

---

## See Also

- `/docs/cper_dper_commands.md` - cper/dper details
- `/docs/master_command_list.md` - Full command list
