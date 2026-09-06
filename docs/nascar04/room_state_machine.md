# PS2 Lobby Room State Machine Analysis

## Overview
This document analyzes the room state machine implemented in the EA Sports PS2 lobby protocol, based on reverse engineering of the NASCAR.ELF binary.

## Room State Diagram

```
                                    ┌─────────────────┐
                                    │                 │
                    ┌───────────────│  NO_ROOM        │◄──────────────┐
                    │               │                 │               │
                    │               └─────────────────┘               │
                    │                                                 │
                    │                                                 │
                    ▼                                                 │
    ┌───────────────────────┐         ┌─────────────────┐             │
    │                       │         │                 │             │
    │   LOBBY_LOOKING      │────────▶│  IN_ROOM       │─────────────┘
    │   (browsing list)    │  JOIN   │                 │   LEAVE
    │                       │         │                 │
    └───────────────────────┘         └─────────────────┘
           │                                     ▲
           │ CREATE                               │
           │                                     │
           ▼                                     │
    ┌───────────────────────┐                   │
    │                       │                   │
    │   ROOM_CREATING      │───────────────────┘
    │   (waiting for host)  │      CANCEL
    │                       │
    └───────────────────────┘

    ┌───────────────────────┐         ┌─────────────────┐
    │                       │  START  │                 │
    │   GAME_STARTING      │────────▶│   IN_GAME      │
    │                       │         │                 │
    └───────────────────────┘         └─────────────────┘

    ┌───────────────────────┐         ┌─────────────────┐
    │                       │ TRANSFER│                 │
    │   HOST_MIGRATING     │────────▶│   IN_GAME      │
    │                       │         │   (new host)   │
    └───────────────────────┘         └─────────────────┘
```

## State Definitions

### NO_ROOM (State 0)
**Description**: Client not currently in any room
**Valid Transitions**:
- `JOIN` → LOBBY_LOOKING (if room list received)
- `CREATE` → ROOM_CREATING
- `LIST` → (stays in NO_ROOM, receives room list)

### LOBBY_LOOKING (State 1)
**Description**: Client is viewing room list, preparing to join
**Valid Transitions**:
- `JOIN <room_id>` → IN_ROOM
- `CANCEL` → NO_ROOM
- `CREATE` → ROOM_CREATING
- `REFRESH` → (stays in LOBBY_LOOKING, receives updated list)

### IN_ROOM (State 2)
**Description**: Client is a member of a room
**Valid Transitions**:
- `LEAVE` → NO_ROOM
- `START` (host only) → GAME_STARTING
- `TEXT <message>` → (stays in IN_ROOM, broadcasts)
- `ATTR <changes>` → (stays in IN_ROOM, updates)
- `KICK <user>` (host only) → (stays in IN_ROOM)
- `HOST` (host migration) → HOST_MIGRATING

### ROOM_CREATING (State 3)
**Description**: Room created, waiting for other players to join
**Valid Transitions**:
- `CANCEL` → NO_ROOM
- `START` → GAME_STARTING (host only)
- Player joins → (stays in ROOM_CREATING)
- Player leaves → (stays in ROOM_CREATING)

### GAME_STARTING (State 4)
**Description**: Countdown in progress before game starts
**Valid Transitions**:
- `CANCEL` (host only) → IN_ROOM
- Timer expires → IN_GAME
- All players ready required

### IN_GAME (State 5)
**Description**: Game session in progress
**Valid Transitions**:
- `END` → IN_ROOM
- `HOST` (migration) → HOST_MIGRATING

### HOST_MIGRATING (State 6)
**Description**: Host is transferring to another player
**Valid Transitions**:
- `CONFIRM` (new host) → IN_GAME or IN_ROOM
- Timeout → IN_ROOM (with new host assigned)

## Message Types for Room Operations

### LIST (Room Listing)
```
Client → Server: LIST\n
Server → Client: ROOMS=<count> USERS=<count> RANKS=<count> MESGS=<count>\n
              <room1_data>\n
              <room2_data>\n
              ...
```

### JOIN (Join Room)
```
Client → Server: JOIN ROOM=<room_id> [PASS=<password>]\n
Server → Client: mgADDR HOST=<host> PORT=<port> SESS=<session>\n
                  [Error: mgDOWN <code> <msg>]
```

### CREATE (Create Room)
```
Client → Server: CREATE TITL=<title> MAX=<max_players> [PASS=<password>]\n
Server → Client: mgROOM ID=<room_id> HOST=<host> PORT=<port>\n
                  [Error: mgDOWN <code> <msg>]
```

### LEAVE (Leave Room)
```
Client → Server: LEAVE\n
Server → Client: mgok\n
```

### START (Start Game - Host Only)
```
Client → Server: START\n
Server → Client: mgGO\n
Broadcast to room: mgSTART\n
```

### TEXT (Chat Message)
```
Client → Server: TEXT BODY=<message>\n
Broadcast to room members:
  mgTEXT FROM=<user> BODY=<message> TIME=<timestamp>\n
```

### ATTR (Room Attributes)
```
Client → Server: ATTR [MAX=<max>] [TITL=<title>] [LOCK=<0|1>]\n
Server → Client: mgATTR MAX=<max> TITL=<title> LOCK=<lock>\n
Broadcast to room members: (for other players)
  mgATTR MAX=<max> TITL=<title> LOCK=<lock>\n
```

### PERS (Persona/Profile)
```
Client → Server: PERS NAME=<name> PROD=<product_id>\n
Server → Client: mgPERS ID=<persona_id> STAT=<status>\n
```

## Room Data Structure

Based on binary analysis of room handling functions:

```c
struct Room {
    uint32_t id;           // Room identifier
    char title[64];        // Room name/title
    uint32_t host_ip;      // Host IP address (network order)
    uint16_t host_port;    // Host port number
    uint8_t max_players;   // Maximum players allowed
    uint8_t cur_players;   // Current player count
    uint8_t game_type;     // Game mode/type
    uint8_t rank_min;      // Minimum rank to join
    uint8_t rank_max;      // Maximum rank allowed
    uint8_t flags;         // Room flags (password, locked, etc.)
    uint32_t created;       // Creation timestamp
    uint32_t host_persona; // Host's persona ID
    char password_hash[32]; // Hashed password (if set)
};
```

## Room Flags

| Bit | Name | Description |
|-----|------|-------------|
| 0 | PRIVATE | Room requires password |
| 1 | LOCKED | Room is locked (no joins) |
| 2 | RANKED | Ranked match |
| 3 | CLAN | Clan/team room |
| 4 | EVENT | Special event room |
| 5 | EA_STAFF | EA Staff moderated |

## Server Emulator Implementation

### Room Manager Class
```python
class RoomManager:
    def __init__(self):
        self.rooms = {}  # room_id -> Room object
        self.clients = {}  # client_id -> {room_id, state, ...}
        
    async def handle_list(self, client):
        """Return room listing"""
        header = f"ROOMS={len(self.rooms)} USERS={sum(r.cur_players for r in self.rooms.values())} "
        header += f"RANKS=1 MESGS=1\n"
        
        rooms_data = ""
        for room in self.rooms.values():
            rooms_data += f"{room.host}:{room.port}|{room.title}|{room.cur_players}/{room.max_players}|"
            rooms_data += f"{room.game_type}\n"
            
        return f"mg{header}{rooms_data}"
        
    async def handle_join(self, client, room_id, password=None):
        """Join a room"""
        room = self.rooms.get(room_id)
        if not room:
            return "mgDOWN 1 Room not found"
            
        if room.password_hash and room.password_hash != hash(password):
            return "mgDOWN 2 Invalid password"
            
        if room.cur_players >= room.max_players:
            return "mgDOWN 3 Room is full"
            
        # Add client to room
        room.cur_players += 1
        room.players.append(client)
        client.room_id = room_id
        client.state = "IN_ROOM"
        
        # Return P2P address for host
        return f"mgADDR HOST={room.host} PORT={room.port} SESS={client.session}"
        
    async def handle_create(self, client, title, max_players, password=None):
        """Create a new room"""
        room_id = generate_room_id()
        room = Room(
            id=room_id,
            title=title,
            host=client.ip,
            port=client.port,
            max_players=max_players,
            password_hash=hash(password) if password else None,
            host_persona=client.persona_id
        )
        self.rooms[room_id] = room
        
        # Add creator to room
        room.players.append(client)
        client.room_id = room_id
        client.state = "ROOM_CREATING"
        
        return f"mgROOM ID={room_id} HOST={room.host} PORT={room.port}"
        
    async def handle_leave(self, client):
        """Leave current room"""
        if client.room_id:
            room = self.rooms.get(client.room_id)
            if room:
                room.cur_players -= 1
                room.players.remove(client)
                
                if room.cur_players == 0:
                    # Delete empty room
                    del self.rooms[client.room_id]
                elif room.host_persona == client.persona_id:
                    # Migrate host
                    room.host_persona = room.players[0].persona_id
                    
        client.room_id = None
        client.state = "NO_ROOM"
        return "mgok"
        
    async def handle_text(self, client, message):
        """Broadcast message to room"""
        if not client.room_id:
            return "mgDOWN 4 Not in a room"
            
        room = self.rooms.get(client.room_id)
        broadcast = f"mgTEXT FROM={client.persona} BODY={message} TIME={time()}\n"
        
        # Send to all room members (except sender)
        for player in room.players:
            if player != client:
                await player.send(broadcast)
                
        return "mgok"
        
    async def handle_start(self, client):
        """Start the game (host only)"""
        room = self.rooms.get(client.room_id)
        if not room:
            return "mgDOWN 1 Not in a room"
            
        if room.host_persona != client.persona_id:
            return "mgDOWN 5 Not the host"
            
        # Broadcast START to all room members
        for player in room.players:
            await player.send("mgSTART\n")
            
        client.state = "GAME_STARTING"
        return "mgGO\n"
```

## State Transitions Code

```python
VALID_TRANSITIONS = {
    "NO_ROOM": ["LOBBY_LOOKING", "ROOM_CREATING"],
    "LOBBY_LOOKING": ["IN_ROOM", "NO_ROOM", "ROOM_CREATING"],
    "IN_ROOM": ["NO_ROOM", "GAME_STARTING", "IN_ROOM"],
    "ROOM_CREATING": ["GAME_STARTING", "NO_ROOM", "IN_ROOM"],
    "GAME_STARTING": ["IN_GAME", "IN_ROOM"],
    "IN_GAME": ["IN_ROOM", "HOST_MIGRATING"],
    "HOST_MIGRATING": ["IN_GAME", "IN_ROOM"]
}

def can_transition(current_state, new_state):
    return new_state in VALID_TRANSITIONS.get(current_state, [])
```

## Error Codes

| Code | Name | Description |
|------|------|-------------|
| 0 | SUCCESS | Operation succeeded |
| 1 | NOT_FOUND | Room/user not found |
| 2 | INVALID | Invalid parameter |
| 3 | FULL | Room is full |
| 4 | NOT_IN_ROOM | Not currently in a room |
| 5 | NOT_HOST | Not the room host |
| 6 | ALREADY_IN_ROOM | Already in a room |
| 7 | RANK_RESTRICTED | Rank restrictions prevent joining |

## References

- LobbyApiUpdate function: 0x0031bdf0
- Room handler dispatch: via hash table lookup at 0x003da378
- Room state structures: Referenced from 0x003da2e0 (protocol keys)
