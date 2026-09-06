# BuddyApi Command Reference

**Source**: Binary string table at 0x003d8378 (verified via radare2)  
**Date**: September 6, 2026

## Command Codes

| Command | Hex (BE) | Description |
|---------|-----------|-------------|
| ADDR | 0x41444452 | Server/peer address |
| ROOM | 0x524F4F4D | Room operations |
| EWBC | 0x45574243 | East/West/Best Connected |
| PRIV | 0x50524956 | Private message |
| TEXT | 0x54455854 | Text/chat message |
| ATTR | 0x41545452 | Attribute update |
| PERS | 0x50455253 | Persona |
| HOST | 0x484F5354 | Host migration |
| BLOC | 0x424C4F43 | Block user |
| DECL | 0x4445434C | Decline invite |
| ACPT | 0x41435054 | Accept invite |

## String Table Location
```
0x003d8378: ADDR (4 bytes)
0x003d8380: ROOM (4 bytes)
0x003d8388: EWBC (4 bytes)
0x003d8390: PRIV (4 bytes)
0x003d8398: TEXT (4 bytes)
0x003d83a0: ATTR (4 bytes)
0x003d83a8: PERS (4 bytes)
0x003d83b0: HOST (4 bytes)
0x003d83b8: BLOC (4 bytes)
0x003d83c0: DECL (4 bytes)
0x003d83c8: ACPT (4 bytes)
```

## Handler Reference
- `BuddyApiUpdate` at 0x00362020 handles all BuddyApi commands
- Referenced by `BuddySystem_Scheduler`
