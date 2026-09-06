# LobbyApi Commands (NASCAR.ELF)

## Command Types

- **LobbyApi**: lowercase commands (+ prefix or 4-char lowercase)
- **BuddyApi**: UPPERCASE 4-char commands

## LobbyApi Broadcast Commands (+ prefix)

| Command | Hex (BE) | LE Search | Description |
|---------|----------|----------|-------------|
| +ses | 0x2b736573 | 7373652b | Session management |
| +msg | 0x2b6d7367 | 67736d2b | Chat message |
| +who | 0x2b77686f | 6f68772b | Room population update |
| +rom | 0x2b726f6d | 6d6f722b | Room data update |
| +pop | 0x2b706f70 | 706f702b | Population update |
| +usr | 0x2b757372 | 7273752b | User/player roster update |
| +rnk | 0x2b726e6b | 6b6e722b | Rank update |
| +snp | 0x2b736e70 | 706e732b | Snapshot |

## LobbyApi Internal State Commands

| Command | Hex (BE) | Description |
|---------|----------|-------------|
| time | 0x74696d65 | Connection timeout check |
| term | 0x7465726d | Terminate connection |
| offl | 0x6f66666c | Offline mode |
| rdir | 0x72646972 | Directory response |
| conn | 0x636f6e6e | Connection state |
| skey | 0x736b6579 | Session key |
| idle | 0x69646c65 | Idle state |
| auth | 0x61757468 | Authentication |
| acct | 0x61636374 | Account |
| @dir | 0x40646972 | Direct connection |

## Binary Message Types

| Command | Hex (BE) | Description |
|---------|----------|-------------|
| ping | 0x7e706e67 | Ping response |
| room | 0x726f6f6d | Room message type |
| move | 0x6d6f7665 | Room move |

## Key Data Structures

From decompilation, LobbyApiUpdate uses:
- piVar24[0xc4] - Room hash table
- piVar24[0xc9] - User roster hash table  
- piVar24[0xce] - Rank hash table
- piVar24[0x147] - Chat message callback
- piVar24[0x14d] - Session callback
