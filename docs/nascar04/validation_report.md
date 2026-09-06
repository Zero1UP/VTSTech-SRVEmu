# Documentation Validation Report

**Date**: September 6, 2026
**Source**: Ghidra decompilation of NASCAR.ELF
**Functions Validated**: 14 decompiled functions

---

## Wire Format Validation ✓

**Claim**: 12-byte header (Type, Flags, Length, Payload)

**Evidence** from `ProtoAriesSend.c`:
```c
iVar2 = (int)param_5 + 0xc;  // Add 12 bytes for header
uStack_a0 = 0xc;              // Header size = 12
// param_2 = Type (split into 4 bytes BE)
// param_3 = Flags (split into 4 bytes BE)
// iVar2 = Length (split into 4 bytes BE)
// param_4 = Payload pointer
```

**Status**: ✓ VALIDATED

---

## LobbyApi Commands Validation ✓

**Source**: `LobbyApiUpdate.c`

| Hex | Command | Status |
|-----|---------|--------|
| 0x2B736573 | +ses | ✓ |
| 0x2B6D7367 | +msg | ✓ |
| 0x2B77686F | +who | ✓ |
| 0x2B726F6D | +rom | ✓ |
| 0x2B706F70 | +pop | ✓ |
| 0x2B757372 | +usr | ✓ |
| 0x2B726E6B | +rnk | ✓ |
| 0x2B736E70 | +snp | ✓ |
| 0x61757468 | auth | ✓ |
| 0x61636374 | acct | ✓ |
| 0x736B6579 | skey | ✓ |
| 0x73656C65 | Sele | ✓ |
| 0x736E6170 | snap | ✓ |
| 0x70657273 | pers | ✓ |
| 0x7E706E67 | ~png | ✓ |
| 0x40646972 | @dir | ✓ |
| 0x6D6F7665 | move | ✓ |
| 0x726F6F6D | room | ✓ |

**Total**: 18 commands validated

---

## BuddyApi Commands Validation ✓

**Source**: `BuddyApiUpdate.c`

| Hex | Command | Status |
|-----|---------|--------|
| 0x50494E47 | PING | ✓ |
| 0x41555448 | AUTH | ✓ |
| 0x52454356 | RECV | ✓ |
| 0x53454E44 | SEND | ✓ |
| 0x41444D4E | ADMN | ✓ |
| 0x50474554 | PGET | ✓ |
| 0x52474554 | RGET | ✓ |
| 0x524F5354 | ROST | ✓ |
| 0x52414444 | RADD | ✓ |
| 0x5244454C | RDEL | ✓ |

**Total**: 10 commands validated

**Note**: Initial documentation had RGET incorrectly mapped. Fixed.

---

## Key-Value Format Validation ✓

**Claim**: KEY=value format with '=' separator

**Evidence** from `TagFieldFind.c`:
```c
if (bVar1 == 0x3d) {  // 0x3d = '='
    bVar1 = pbVar5[1];
    // ... match key
}
```

**Status**: ✓ VALIDATED

---

## String Quoting Validation ✓

**Claim**: Supports single and double quoted strings

**Evidence** from `TagFieldGetString.c`:
```c
if ((*param_1 == 0x22) || (bVar6 = 0, *param_1 == 0x27)) {
    // 0x22 = '"', 0x27 = '''
    bVar6 = *param_1;
    param_1 = param_1 + 1;
}
```

**Status**: ✓ VALIDATED

---

## Issues Found

### Issue #1: RGET/PGET Confusion (FIXED)
- **Initial doc**: Both mapped to 0x50474554 (PGET)
- **Actual code**: RGET = 0x52474554, PGET = 0x50474554
- **Fix**: Updated proto_api_commands.md with correct mapping

---

## Summary

| Category | Items | Validated | Issues |
|----------|-------|-----------|--------|
| Wire Format | 1 | 1 | 0 |
| LobbyApi Commands | 18 | 18 | 0 |
| BuddyApi Commands | 10 | 10 | 1 (fixed) |
| Key-Value Format | 1 | 1 | 0 |
| String Quoting | 1 | 1 | 0 |

**Overall Status**: ✓ ALL VALIDATED
