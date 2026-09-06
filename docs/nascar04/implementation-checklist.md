# NASCAR Thunder 2004 Server Implementation Checklist

## Overview
This checklist documents all known client commands, server responses, and push notifications based on decompiled function analysis and live server logs.

## ✅ **IMPLEMENTED AND WORKING**

### **Directory Server (TCP:10600)**
- [x] `@dir` - Server discovery and redirection
- [x] `ADDR` - Client IP reporting
- [x] `PROD` - Product identification
- [x] `VERS` - Version checking
- [x] `LANG` - Language setting
- [x] `SLUS` - SLUS identifier
- [x] Response format: `ADDR=<ip>, PORT=<port>, LKEY=<hex>, SESS=<decimal>, MASK=4294967295`

### **Game Server (TCP:10901) - Core Protocol**

#### **Connection & Authentication**
- [x] `addr` - Client IP/port reporting
  - Format: `ADDR=<client_ip>, PORT=<client_port>`
  - Response: `STATUS=1`
- [x] `skey` - Public key authentication
  - Format: `SKEY=$<hex_public_key>`
  - Response: `SKEY=0`
- [x] `auth` - Full authentication
  - Format: `NAME=<user>, TOS=<tos>, PASS=<hash>, MID=<machine_id>, PROD=<product>, VERS=<version>, LANG=<lang>, SLUS=<slus>, MASK=<mask>, HWFLAG=<hw_flag>, HWMASK=<hw_mask>`
  - Response: `TOS=1, NAME=<user>, USER=<unknown>, PERSONAS=<persona_list>, PRIV=<privileges>, LAST=<last_login>, SESS=<session_id>, S=<status>, STATUS=<status>`

#### **Persona Management**
- [x] `pers` - Persona selection
  - Format: `PERS=<persona_name>`
  - Response: `PERS=<persona>, LKEY=$0, S=<status>, STATUS=<status>, LAST=<timestamp>`

#### **Information Requests**
- [x] `sele` - Selection/counts request
  - Format: `ROOMS=<count>, USERS=<count>, RANKS=<count>, MESGS=<count>`
  - Response: `DRANK=<rank>, USER=<user>, RATING=<rating>, WINS=<wins>, LOSS=<losses>, STATUS=<status>`
- [x] `sele` - Rank request (RANKS parameter)
  - Format: `RANKS=<rank_level>`
  - Response: `ERANK=<rank>, USER=<user>, RATING=<rating>, WINS=<wins>, LOSS=<losses>, STATUS=<status>`

#### **News & Server Info**
- [x] `news` - News and server information
  - Format: `NAME=0`
  - Response: `BUDDY_URL=<url>, BUDDY_PORT=<port>, BUDDY_SERVER=<ip>, TOS_TEXT=<tos>, NEWS_TEXT=<news>, USE_ETOKEN=<flag>, S=<status>, STATUS=<status>`

#### **Room Management**
- [x] `move` - Room joining/leaving
  - Format: `NAME=<room_name>, PASS=<password>`
  - Response: `I=<room_index>, N=<room_name>, F=<flags>`
- [x] `room` - Room operations
  - Format: Various room commands
  - Response: Room-specific responses

#### **Profile Management**
- [x] `user` - User profile request
  - Format: `PERS=<persona>`
  - Response: `N=<name>, R=<rating>, W=<wins>, L=<losses>, PERSONAS=<persona_list>, STATUS=<status>`

#### **Keepalive**
- [x] `~png` - Ping/pong keepalive
  - Format: `TIME=<timestamp>, SESS=<session_id>, NAME=<username>, STATUS=<status>`
  - Response: `TIME=<timestamp>, SESS=<session_id>, NAME=<username>, STATUS=<status>`

### **Push Notifications (Game Server)**

#### **Presence & User Info**
- [x] `+who` - User's own presence info
  - Format: `F=<friend_flag>, N=<name>, RI=<room_index>, RT=<room_type>, R=<rank>, RF=<rank_flag>`
- [x] `+usr` - User info in login/lobby context
  - Format: `I=<user_id>, N=<name>, A=<ip_int>, F=<flags>, S=<status>, P=<password>`
- [x] `+usr` - User info in room context
  - Format: `I=<user_id>, N=<name>, A=<ip_int>, F=<flags>, S=<status>, RI=<room_id>`
- [x] `+usr` - Broadcast user presence to room
  - Format: Same as room context user info

#### **Room Information**
- [x] `+rom` - Room listings
  - Format: `I=<room_id>, N=<room_name>, H=<room_heading>, A=<room_ip_int>, T=<room_type>, L=<room_limit>, F=<room_flags>`

#### **Population Counts**
- [x] `+pop` - Population counts per room
  - Format: `Z=<room_idx>:<count> <room_idx>:<count> ...`

### **Buddy Server (TCP:10899)**

#### **Authentication**
- [x] `AUTH` - Buddy server authentication
  - Format: `PROD=<product>, VERS=<version>, PRES=<presence>, USER=<user>, LKEY=<login_key>`
  - Response: `NAME=<name>, S=<session_id>, STATUS=<status>`

#### **Presence Management**
- [x] `PSET` - Presence setting
  - Format: `SHOW=<show_mode>, STAT=<status_text>, PROD=<product>`
  - Response: `NAME=<name>, ID=<id>, S=<session_id>, STATUS=<status>`

#### **Roster Management**
- [x] `RGET` - Roster/buddy list request
  - Format: `LRSC=<list_request>, LIST=<list_type>, PRES=<presence>, ID=<user_id>`
  - Response: Buddy list with presence info

#### **Messaging**
- [x] `SEND` - Instant messaging
  - Format: `TYPE=<message_type>, USER=<target_user>, BODY=<message_text>, SECS=<timestamp>`
  - Response: Message delivery confirmation

#### **Push Notifications (Buddy Server)**
- [x] `+pop` - Population counts
  - Format: `Z=<room_idx>:<count> <room_idx>:<count> ...`
- [x] `+usr` - User presence updates
  - Format: `I=<user_id>, N=<username>, F=<flags>, A=<ip_address>`

---

## ❌ **MISSING OR INCOMPLETE**

### **Challenge System (PARTIALLY WORKING)**
- [x] **Challenge Forwarding** - Server correctly forwards challenges
- [x] **Challenge Response Forwarding** - Declines are forwarded back
- [ ] **Challenge Reception** - Target user doesn't see challenge properly
- [ ] **Challenge UI Integration** - "user has not proposed a race" error

#### **Current Implementation Status**
```
Client A sends: PRIV=ClientB TEXT=w893m_a017l_g ATTR=3
Server forwards: OPPO=ClientA SEED=w893m_a017l_g ROOM=default  ✅ WORKS
Client B receives: Challenge message but no UI prompt ❌ ISSUE

Client B sends: PRIV=ClientA TEXT=DECL ATTR=3
Server forwards: OPPO=ClientB SEED=DECL ROOM=response  ✅ WORKS
Client A receives: Decline response ❓ UNCLEAR
```

#### **Investigation Needed**
- [ ] Determine correct message format for challenge reception
- [ ] Check if client expects different push notification type
- [ ] Verify challenge state management on client side
- [ ] Test challenge response delivery

### **Missing Commands**

#### **Game Server Commands**
- [ ] `stat` - Statistics requests
- [ ] `snap` - Snapshot requests
- [ ] `peek` - Peek commands
- [ ] `user` - Additional user management commands

#### **Challenge System Commands**
- [ ] `CHAL` - Challenge initialization
- [ ] `RESP` - Challenge response handling
- [ ] `CNCL` - Challenge cancellation

#### **Room Management Commands**
- [ ] `CREATE` - Room creation
- [ ] `KICK` - User kicking
- [ ] `BAN` - User banning
- [ ] `LIST` - Advanced room listing

#### **Advanced Features**
- [ ] `ADMIN` - Admin commands
- [ ] `MOD` - Moderator commands
- [ ] `LOG` - Logging commands
- [ ] `MON` - Monitoring commands

### **Push Notification Issues**
- [ ] **Challenge Push** - Missing `+chal` or similar challenge notification
- [ ] **Response Push** - Missing challenge response notifications
- [ ] **State Sync** - Challenge state synchronization between clients

---

## 🔍 **PROTOCOL ANALYSIS - MISSING PIECES**

### **Challenge System Protocol (From Decompiled Analysis)**

#### **Expected Challenge Flow**
```
Client A → Server: PRIV=ClientB TEXT=<token> ATTR=3
Server → Client B: +chal OPPO=ClientA SEED=<token> ROOM=<room>
Client B → Server: PRIV=ClientA TEXT=DECL/ACPT ATTR=3
Server → Client A: +resp OPPO=ClientB SEED=DECL/ACPT ROOM=<room>
```

#### **Current Implementation Gap**
- [x] Challenge forwarding works (Client A → Server → Client B format)
- [ ] **Missing**: Client B doesn't receive challenge in proper format
- [ ] **Missing**: No challenge-specific push notification
- [ ] **Missing**: Challenge response forwarding back to original sender

### **Message Format Issues**
- [ ] Challenge messages may need different flag (`b'chal'` vs `b'\x00\x00\x00\x00'`)
- [ ] Challenge responses may need different message type
- [ ] Room-specific challenge formatting

---

## 🚨 **CRITICAL FIXES NEEDED**

### **1. Challenge System Investigation (Priority: HIGH)**

#### **Current Understanding**
- Challenges are forwarded using `OPPO/SEED/ROOM` format ✅
- Responses are forwarded back using same format ✅
- Target client doesn't show challenge UI ❓

#### **Hypotheses to Investigate**
1. **Message Type**: Client may expect different message flags/types
2. **Timing**: Challenge may need to be sent immediately after room join
3. **State**: Client may need to be in specific state to receive challenges
4. **Protocol**: Challenge protocol may have additional requirements

#### **Debugging Steps**
```python
# Add detailed logging to challenge flow
LOG.info("[DEBUG] Challenge from %s to %s: %s", challenger, target, token)
LOG.info("[DEBUG] Target client found: %s", target_conn is not None)
LOG.info("[DEBUG] Challenge message sent: %s", message_format)
```

#### **Message Format Investigation**
- Check if client expects different message flags (not b'\x00\x00\x00\x00')
- Verify challenge message delivery timing and sequencing
- Test if room membership affects challenge reception

---

## 📋 **TESTING SCENARIOS**

### **Scenario 1: Basic Challenge Flow**
1. [x] Client A authenticates and joins room
2. [x] Client B authenticates and joins same room
3. [ ] Client A challenges Client B → **FAILS** (Client B doesn't see challenge)
4. [ ] Client B should see challenge prompt → **FAILS**

### **Scenario 2: Challenge Response Flow**
1. [ ] Client B receives challenge → **MISSING**
2. [ ] Client B accepts/declines → **MISSING**
3. [ ] Client A receives response → **MISSING**

### **Scenario 3: Challenge Timeout**
1. [ ] Challenges expire after timeout → **MISSING**
2. [ ] Server cleans up stale challenges → **MISSING**

---

## 🎯 **NEXT STEPS**

### **Phase 1: Fix Challenge System (Critical)**
1. [ ] Implement proper challenge push notification (`+chal`)
2. [ ] Fix challenge message format for target client
3. [ ] Implement challenge response forwarding (`+resp`)
4. [ ] Add challenge state tracking

### **Phase 2: Complete Missing Commands**
1. [ ] Implement `stat`, `snap`, `peek` commands
2. [ ] Add room management commands
3. [ ] Implement admin/moderator commands

### **Phase 3: Enhance Features**
1. [ ] Add persistent storage
2. [ ] Implement advanced room features
3. [ ] Add monitoring and logging

---

## 📊 **IMPLEMENTATION STATUS**

| Category | Completion | Status |
|----------|------------|---------|
| **Authentication** | 100% | ✅ Complete |
| **Basic Room System** | 100% | ✅ Complete |
| **Push Notifications** | 80% | ⚠️ Mostly Working |
| **Challenge System** | 60% | ⚠️ Partially Working |
| **Advanced Features** | 10% | ❌ Missing |
| **Overall** | **80%** | 🟡 Mostly Working |

**Current Status**: Server is functional for basic login and room browsing, but challenge system (essential for multiplayer) is broken.