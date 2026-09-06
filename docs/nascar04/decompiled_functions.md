# Decompiled Functions Reference

Source: https://github.com/VTSTech/VTSTech-SRVEmu/tree/main/docs/nascar04/decom

## Downloaded Functions

| Function | Lines | Purpose |
|----------|-------|---------|
| LobbyApiUpdate | 764 | Main LobbyApi protocol handler |
| BuddyApiUpdate | 518 | Peer-to-peer messaging |
| NetworkEvent_MainDispatcher | 517 | Main event routing |
| Game_CommandRouter | 526 | Game command dispatcher |
| NetworkEvent_MainDispatcher | 116 | Network event dispatcher |
| Lobby_ProcessNetworkEvents | 116 | Network event processing |
| ProtoAriesSend | 62 | Send packet |
| ProtoAriesRecv | 44 | Receive packet |
| ProtoAriesPeek | 54 | Peek at packet |
| TagFieldFind | 76 | Key-value lookup |
| TagFieldGetString | 136 | Get string value |
| TagFieldGetFlags | 24 | Get flags value |

## Call Hierarchy

```
NetworkEvent_MainDispatcher
├── Game_CommandRouter
├── NetworkEvent_FallbackDispatcher  
├── Protocol_CommandDispatcher
│   └── LobbyApiUpdate
│       ├── ProtoAriesPeek
│       └── ProtoAriesSend
├── ChallengeSystem_CommandDispatcher
└── Game_HandleSystemCommand
```

## Key Functions

### ProtoAriesSend (0x1622 bytes)
```
ProtoAriesSend(connection, type, flags, payload, payload_len)
```
- Builds 12-byte header
- Calls RpcCall to send

### ProtoAriesPeek (0x1514 bytes)
```
ProtoAriesPeek(connection, *type_out, *flags_out, *payload_out)
```
- Reads 12-byte header
- Returns: type, flags, payload pointer

### LobbyApiUpdate (0x0031bdf0)
- Main message loop
- Handles all LobbyApi commands
- Timeout management
- State machine

### BuddyApiUpdate (0x00362020)
- Roster management
- P2P message routing
- Buddy list operations

## Location
`/home/vtstech/workspace/analysis/decompiled/`
