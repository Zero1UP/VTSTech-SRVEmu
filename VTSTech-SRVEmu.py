import codecs, os, sys, socket, struct, select, time, string, random, hashlib, array, math
from pythonping import ping
from _thread import *

GameSocket = socket.socket()
BuddySocket = socket.socket()
LISTENERSocket = socket.socket()

TOTALARGS = len(sys.argv)
BUILD="0.1-ALPHA R0.63"
SERVER_IP = '192.168.0.228'
SERVER_IP_BIN = b'ADDR=192.168.0.228'
SERVER_PORT_BIN= b'PORT=10901'
PORT_NFSU_PS2 = 10900 #ps2nfs04.ea.com:10900
PORT_BO3U_PS2 = 21800	#ps2burnout05.ea.com:21800
PORT_BO3R_PS2 = 21840 #ps2lobby02.beta.ea.com:21840
PORT_BOP_PS3 = 21870  #ps3burnout08.ea.com:21870
PORT_BOP_PC = 21841  #ps3burnout08.ea.com:21870
LISTENER = 10901
BUDDY_PORT = 10899
THREADCOUNT = 0
EMU_MODE = "nfsu"
SKEYREPLY = b''
SKEYSENT=0
authsent=0
SKEY = ''
z=0
a=''
NO_DATA=False
news_cnt=0
ping_cnt=0
ping_sent=0
ping_start=time.time()
ping_time=time.time()
curr_time=time.time()

msgType=b''
msgSize=b''
clientNAME=''
clientVERS=''
clientMAC=''
clientPERS=''
clientLAST=''
clientPLAST=''
clientMAIL=''
clientADDR=''
clientMADDR=''
clientBORN=''
clientPASS=''
clientUSER=''
clientMINSIZE=''
clientMAXSIZE=''
clientCUSTFLAGS=''
clientPARAMS=''
clientPRIV=''
clientPERSONAS=''
clientSEED=''
clientSYSFLAGS=''

pad = codecs.decode('00000000000000','hex_codec')
pad2 = codecs.decode('00000038','hex_codec')
oddByte = codecs.decode('00','hex_codec')
x0A = codecs.decode('0A','hex_codec')
x00 = codecs.decode('00','hex_codec')
reply=''
SKEY="$5075626c6963204b6579"

def usage():
	print("Usage:")
	print("-nfsu Run in Need for Speed Underground Mode (PS2)")
	print("-bo3r Run in Burnout 3 Takedown Review Copy Mode (PS2)")
	print("-bo3u Run in Burnout 3 Takedown Retail Copy Mode (PS2)")
	print("-bop3 Run in Burnout Paradise Mode (PS3)")
	print("-bopc Run in Burnout Paradise Mode (PC)")
	print("-p 12345 Run in Custom Game Mode on this TCP Port")
	quit()
	
def bind():
	global GameSocket, BuddySocket, LISTENERSocket, SERVER_IP, PORT_NFSU_PS2, PORT_BO3U_PS2, PORT_BO3R_PS2, PORT_BO3P_PS2, PORT_BOP_PS3, TOTALARGS
	for x in range(0,TOTALARGS,1):
		if (TOTALARGS >= 4):	
			print("Too many arguments! Check command line.")
			usage()
		elif (TOTALARGS==1):
			usage()
		elif (sys.argv[x] == "-nfsu"):
			EMU_MODE = "nfsu"
			GameSocket.bind((SERVER_IP, PORT_NFSU_PS2))
			print("Now running in Need for Speed: Underground Mode\n")
		elif (sys.argv[x] == "-bo3r"):
			EMU_MODE = "bo3r"
			print("IP: "+SERVER_IP+" Port: "+str(PORT_BO3U_PS2))
			GameSocket.bind((SERVER_IP, PORT_BO3R_PS2))
			print("Now running in Burnout 3 Review Mode (PS2)\n")
		elif (sys.argv[x] == "-bo3u"):
			EMU_MODE = "bo3u"
			GameSocket.bind((SERVER_IP, PORT_BO3U_PS2))
			print("Now running in Burnout 3 Retail Mode (PS2)\n")
		elif (sys.argv[x] == "-bop3"):
			EMU_MODE = "bop"
			GameSocket.bind((SERVER_IP, PORT_BOP_PS3))
			print("Now running in Burnout Paradise Mode (PS3)\n")   
		elif (sys.argv[x] == "-bopc"):
			EMU_MODE = "bop"
			GameSocket.bind((SERVER_IP, PORT_BOP_PC))
			print("Now running in Burnout Paradise Mode (PC)\n")   
		elif (sys.argv[x] == "-p"):
			EMU_MODE = "custom"
			GameSocket.bind((SERVER_IP, int(sys.argv[x+1])))
			print("Now running in Custom Game Mode\n")   
	LISTENERSocket.bind((SERVER_IP, LISTENER))
	BuddySocket.bind((SERVER_IP, BUDDY_PORT))
	LISTENERSocket.listen(1)
	GameSocket.listen(1)
	BuddySocket.listen(1)
	print("Bind complete.\n")

print("VTSTech-SRVEmu v"+BUILD+"\nGitHub: https://github.com/Veritas83/VTSTech-SRVEmu\nContributors: No23\n")
bind()
print('Waiting for connections.. ')
reply=b''

def parse_data(data):
	tmp = data.split(codecs.decode('0A','hex_codec'))
	global clientALTS, clientNAME, clientVERS, clientMAC, clientPERS, clientPERSONAS, clientBORN, clientMAIL, clientSKU, clientDEFPER, clientLAST, clientPLAST, clientMADDR, clientUSER, clientMINSIZE, clientMAXSIZE, clientPARAMS, clientCUSTFLAGS, clientPRIV, clientMINSIZE, clientMAXSIZE, clientPARAMS, clientCUSTFLAGS, clientPRIV, clientSEED, clientSEED, clientSYSFLAGS, clientSEED, clientSYSFLAGS
	global pad,pad2,x00,x0A,oddByte,reply,msgType,msgSize,authsent,NO_DATA,news_cnt,news_cnt

	for x in range(0,len(tmp)):
		#print("DEBUG: "+str(x))
		if (tmp[x].decode('latin1')[:3] == "MID") | (tmp[x].decode('latin1')[:3] == "MAC"):
			clientMAC = tmp[x].decode('latin1')[4:]
		elif (tmp[x].decode('latin1')[:3] == "SKU"):
			clientSKU = tmp[x].decode('latin1')[4:]
		elif (tmp[x].decode('latin1')[:4] == "ALTS"):
			clientALTS = tmp[x].decode('latin1')[5:]	
		elif (tmp[x].decode('latin1')[:4] == "BORN"):
			clientBORN = tmp[x].decode('latin1')[5:]
		elif (tmp[x].decode('latin1')[:4] == "SLUS"):
			clientSLUS = tmp[x].decode('latin1')[5:]				
		elif (tmp[x].decode('latin1')[:4] == "VERS"):
			clientVERS = tmp[x].decode('latin1')[5:]
		elif (tmp[x].decode('latin1')[:4] == "NAME"):
			clientNAME = tmp[x].decode('latin1')[5:]
		elif (tmp[x].decode('latin1')[:4] == "PASS"):
			clientPASS = tmp[x].decode('latin1')[5:]	
		elif (tmp[x].decode('latin1')[:4] == "PERS"):
			clientPERS = tmp[x].decode('latin1')[5:]	
		elif (tmp[x].decode('latin1')[:4] == "SEED"):
			clientSEED = tmp[x].decode('latin1')[5:]	
		elif (tmp[x].decode('latin1')[:4] == "MAIL"):
			clientMAIL = tmp[x].decode('latin1')[5:]
		elif (tmp[x].decode('latin1')[:4] == "LAST"):
			clientLAST = tmp[x].decode('latin1')[5:]
		elif (tmp[x].decode('latin1')[:4] == "PRIV"):
			clientPRIV = tmp[x].decode('latin1')[5:]
		elif (tmp[x].decode('latin1')[:5] == "PLAST"):
			clientPLAST = tmp[x].decode('latin1')[6:]
		elif (tmp[x].decode('latin1')[:5] == "MADDR"):
			clientMADDR = tmp[x].decode('latin1')[6:]
		elif (tmp[x].decode('latin1')[:6] == "DEFPER"):
			clientDEFPER = tmp[x].decode('latin1')[7:]
		elif (tmp[x].decode('latin1')[:6] == "PARAMS"):
			clientPARAMS = tmp[x].decode('latin1')[7:]
		elif (tmp[x].decode('latin1')[:6] == "SDKVER"):
			clientSDKVER = tmp[x].decode('latin1')[7:]
		elif (tmp[x].decode('latin1')[:7] == "MINSIZE"):
			clientMINSIZE = tmp[x].decode('latin1')[8:]
		elif (tmp[x].decode('latin1')[:7] == "MAXSIZE"):
			clientMAXSIZE = tmp[x].decode('latin1')[8:]
		elif (tmp[x].decode('latin1')[:8] == "SYSFLAGS"):
			clientSYSFLAGS = tmp[x].decode('latin1')[9:]
		elif (tmp[x].decode('latin1')[:9] == "CUSTFLAGS"):
			clientCUSTFLAGS = tmp[x].decode('latin1')[10:]
		elif (tmp[x].decode('latin1')[:9] == "PERSONAS"):
			clientPERSONAS = tmp[x].decode('latin1')[10:]				

#Thx No23
def create_packet(cmd, subcmd, payload):
    payload += '\0'
    size = len(payload)
    return struct.pack(">4s4sL%ds" % size, bytearray(cmd, 'ascii'), bytearray(subcmd, 'ascii'), size + 12, bytearray(payload, 'ascii'))
#Thx No23
def cmd_news(payload):
    print("News Payload: "+str(payload))
    p = 'BUDDY_SERVER=192.168.0.228\n'
    p+= 'BUDDY_PORT='+str(BUDDY_PORT)+'\n'
    p+= 'EACONNECT_WEBOFFER_URL=http://ps3burnout08.ea.com/EACONNECT.txt\n'
    p+= 'TOSAC_URL=http://ps3burnout08.ea.com/TOSAC.txt\n'
    p+= 'TOSA_URL=http://ps3burnout08.ea.com/TOSA.txt\n'
    p+= 'TOS_URL=http://ps3burnout08.ea.com/TOS.txt\n'           
    #p+= 'USE_GLOBAL_ROAD_RULE_SCORES=0\n'
    #p+= 'QOS_LOBBY=192.168.0.228\n'
    #p+= 'OS_PORT=17582\n'
    p+= 'ROAD_RULES_SKEY=frscores\n'
    p+= 'CHAL_SKEY=chalscores\n'
    p+= 'NEWS_DATE='+time.strftime("%Y.%m.%d-%I:%M:%S",time.localtime())+'\n'
    p+= 'NEWS_URL=http://ps3burnout08.ea.com/news.txt\n'
    p+= 'USE_ETOKEN=0\n'
    
    packet = create_packet('news', 'new8', p)
    if (payload == "NAME=7") | (payload == "BP"):
	    packet = create_packet('news', 'new7', p)
	    #payload=''
	    if (clientVERS =='BURNOUT5/ISLAND'):
	     packet = create_packet('news', 'new1', p)
    return packet
        
def reply_skey():
	oddByte = codecs.decode('99','hex_codec')
	replyTmp=b'skey'+pad
	#skeyStr="SKEY="+SKEY+str(random.randint(1000,9999))+"f570e6"+str(random.randint(10,99))
	#skeyStr="PLATFORM=PS2"
	#reply=skeyStr.encode('ascii')+x0A
	skeyStr="SKEY=$37940faf2a8d1381a3b7d0d2f570e6a7"
	reply=skeyStr.encode('ascii')+codecs.decode('0A00','hex_codec') #repeat me 0A6E6577736E6577370000000d00
	oddByte=len(codecs.decode(replyTmp+reply,'latin1'))+1
	#oddByte=51
	oddByte = codecs.decode('{0:x}'.format(int(oddByte)),'hex_codec')
	reply=replyTmp+oddByte+reply
	SKEYSENT=1
	print("Debug: skey sent")
	return reply
	
def reply_acct(data):
	tmp = data[11:].split(codecs.decode('0A','hex_codec'))
	global clientALTS, clientNAME, clientVERS, clientMAC, clientPERS, clientPERSONAS, clientBORN, clientMAIL, clientSKU, clientDEFPER, clientLAST, clientPLAST, clientMADDR, clientUSER, clientMINSIZE, clientMAXSIZE, clientPARAMS, clientCUSTFLAGS, clientPRIV, clientMINSIZE, clientMAXSIZE, clientPARAMS, clientCUSTFLAGS, clientPRIV, clientSEED, clientSEED, clientSYSFLAGS
	global pad,pad2,x00,x0A,oddByte,reply,msgType,msgSize,authsent,NO_DATA,news_cnt,news_cnt
	reply=b''
	MD5=hashlib.md5()
	MD5.update(clientPASS.encode('ascii'))
	db = open("acct.db","a+")
	if sys.getsizeof(db)>1:
		line = db.readlines()
		for x in list(line):
			clientUSER = x.split("#")[0]
			if (clientNAME == clientUSER):
				reply=b'authimst'#if account exists, cannot create
				return reply
			print("DEBUG: "+clientUSER)
		clientUSER = x.split("#")[0]
		clientMAIL = x.split("#")[2]
		acctStr="TOS=1"
		reply=acctStr.encode('ascii')+x0A
		acctStr="NAME="+clientNAME.lower()
		reply+=acctStr.encode('ascii')+x0A
		acctStr="AGE=21"
		reply+=acctStr.encode('ascii')+x0A   
		acctStr="PERSONAS="+clientNAME.lower()		
		reply+=acctStr.encode('ascii')+x0A
		clientLAST=time.strftime("%Y.%m.%d %I:%M:%S",time.localtime())
		acctStr="SINCE="+clientLAST
		reply+=acctStr.encode('ascii')+x0A
		acctStr="LAST="+clientLAST
		reply+=acctStr.encode('ascii')+x0A+x00
		db.write(clientNAME+"#"+clientBORN+"#"+clientMAIL+"#"+MD5.hexdigest()+"#"+clientPERS+"#"+clientLAST)
		db.close
		return reply			
	else:
		acctStr="TOS=1"+x0A
		reply=acctStr.encode('ascii')+x0A
		acctStr="NAME="+clientNAME.lower()
		reply+=acctStr.encode('ascii')+x0A
		acctStr="AGE=21"
		reply+=acctStr.encode('ascii')+x0A   
		acctStr="PERSONAS="+clientNAME.lower()		
		reply+=acctStr.encode('ascii')+x0A
		acctStr="SINCE="+time.strftime("%Y.%m.%d-%I:%M:%S",time.localtime())
		reply+=authStr.encode('ascii')+x0A         
		acctStr="LAST="+time.strftime("%Y.%m.%d-%I:%M:%S",time.localtime())			
		reply+=codecs.decode('00','hex_codec')
		db.write(clientNAME+"#"+clientBORN+"#"+clientMAIL+"#"+MD5.hexdigest()+"#"+clientPERS+"#"+clientLAST)
		db.close
		return reply		

def reply_auth(data):
	tmp = data[11:].split(codecs.decode('0A','hex_codec'))
	global clientALTS, clientNAME, clientVERS, clientMAC, clientPERS, clientPERSONAS, clientBORN, clientMAIL, clientSKU, clientDEFPER, clientLAST, clientPLAST, clientMADDR, clientUSER, clientMINSIZE, clientMAXSIZE, clientPARAMS, clientCUSTFLAGS, clientPRIV, clientMINSIZE, clientMAXSIZE, clientPARAMS, clientCUSTFLAGS, clientPRIV, clientSEED, clientSEED, clientSYSFLAGS
	global pad,pad2,x00,x0A,oddByte,reply,msgType,msgSize,authsent,NO_DATA,news_cnt
	reply=b''

	if (clientVERS == 'BURNOUT5/ISLAND'): #Burnout Paradise
		clientNAME = clientMADDR.split("$")
		#authStr="TOS=1"
		#reply=authStr.encode('ascii')+x0A
		authStr="NAME=VTSTech"
		reply=authStr.encode('ascii')+x0A
		authStr="MAIL=nospam@vts-tech.org"
		reply+=authStr.encode('ascii')+x0A
		authStr="PERSONAS=VTSTech"
		reply+=authStr.encode('ascii')+x0A
		authStr="BORN=19800325"
		reply+=authStr.encode('ascii')+x0A   
		authStr="GEND=M"
		reply+=authStr.encode('ascii')+x0A         
		authStr="FROM=US"
		reply+=authStr.encode('ascii')+x0A         
		authStr="LANG=en"
		reply+=authStr.encode('ascii')+x0A
		authStr="SPAM=NN"
		reply+=authStr.encode('ascii')+x0A         
		authStr="SINCE="+time.strftime("%Y.%m.%d-%I:%M:%S",time.localtime())
		reply+=authStr.encode('ascii')+x0A        
		authStr="LAST="+time.strftime("%Y.%m.%d-%I:%M:%S",time.localtime())
		reply+=authStr.encode('ascii')+x0A
		authStr="ADDR=24.141.39.62"
		reply+=authStr.encode('ascii')+x0A
		authStr="_LUID=$000000000b32588d"
		reply+=authStr.encode('ascii')
		#authStr="DEFPER=1"
		#reply+=authStr.encode('ascii')+x0A            
		reply+=codecs.decode('0A00','hex_codec')
		print("AUTHSENT: ",authsent)
		if authsent >=3:
			reply=b''
		return reply
		
	authStr="TOS=1"
	reply=authStr.encode('ascii')+x0A
	authStr="NAME="+clientNAME.lower()
	reply+=authStr.encode('ascii')+x0A
	authStr="MAIL="+clientMAIL
	reply+=authStr.encode('ascii')+x0A
	authStr="PERSONAS="+clientNAME.lower()
	reply+=authStr.encode('ascii')+x0A
	authStr="BORN=19800325"
	reply+=authStr.encode('ascii')+x0A   
	authStr="GEND=M"
	reply+=authStr.encode('ascii')+x0A         
	authStr="FROM=US"
	reply+=authStr.encode('ascii')+x0A         
	authStr="LANG=en"
	reply+=authStr.encode('ascii')+x0A
	authStr="SPAM=NN"
	reply+=authStr.encode('ascii')+x0A         
	authStr="SINCE="+time.strftime("%Y.%m.%d-%I:%M:%S",time.localtime())
	reply+=authStr.encode('ascii')+x0A        
	authStr="LAST="+time.strftime("%Y.%m.%d-%I:%M:%S",time.localtime())
	#reply+=authStr.encode('ascii')+x0A
	#authStr="ADDR=24.143.43.66"
	reply+=authStr.encode('ascii')
	#authStr="_LUID=$000000000b32588d"
	#authStr="DEFPER=1"
	#reply+=authStr.encode('ascii')+x0A            
	reply+=codecs.decode('0A00','hex_codec')
	print("AUTHSENT: ",authsent)
	if authsent >=3:
		reply=b''
	return reply		

def reply_cper(data):
	tmp = data[11:].split(codecs.decode('0A','hex_codec'))
	global clientALTS, clientNAME, clientVERS, clientMAC, clientPERS, clientPERSONAS, clientBORN, clientMAIL, clientSKU, clientDEFPER, clientLAST, clientPLAST, clientMADDR, clientUSER, clientMINSIZE, clientMAXSIZE, clientPARAMS, clientCUSTFLAGS, clientPRIV, clientMINSIZE, clientMAXSIZE, clientPARAMS, clientCUSTFLAGS, clientPRIV, clientSEED, clientSEED, clientSYSFLAGS
	global pad,pad2,x00,x0A,oddByte,reply,msgType,msgSize,authsent,NO_DATA,news_cnt
	reply=b''
	cperStr="PERS="+clientPERS
	reply=cperStr.encode('ascii')+x0A
	cperStr="ALTS="+clientALTS
	reply+=cperStr.encode('ascii')+x0A
	reply+=codecs.decode('00','hex_codec')
	return reply
	
def reply_rom():
	global clientALTS, clientNAME, clientVERS, clientMAC, clientPERS, clientPERSONAS, clientBORN, clientMAIL, clientSKU, clientDEFPER, clientLAST, clientPLAST, clientMADDR, clientUSER, clientMINSIZE, clientMAXSIZE, clientPARAMS, clientCUSTFLAGS, clientPRIV, clientMINSIZE, clientMAXSIZE, clientPARAMS, clientCUSTFLAGS, clientPRIV, clientSEED, clientSEED, clientSYSFLAGS
	global pad,pad2,x00,x0A,oddByte,reply,msgType,msgSize,authsent,NO_DATA,news_cnt
	oddByte = codecs.decode('00','hex_codec')          
	replyTmp=b'+rom'+pad
	romStr="TI=1001"
	reply=romStr.encode('ascii')+x0A
	romStr="N=room"
	reply+=romStr.encode('ascii')+x0A
	romStr="H=vtstech"
	reply+=romStr.encode('ascii')+x0A
	romStr="D=burnout 3 revival"
	reply+=romStr.encode('ascii')+x0A
	romStr="F=CK"
	reply+=romStr.encode('ascii')+x0A
	romStr="A=24.141.39.62"
	reply+=romStr.encode('ascii')+x0A
	romStr="T=0"
	reply+=romStr.encode('ascii')+x0A
	romStr="L=5"
	reply+=romStr.encode('ascii')+x0A
	romStr="P=0"
	reply+=romStr.encode('ascii')+x0A						
	reply+=romStr.encode('ascii')+codecs.decode('0A00','hex_codec')
	oddByte=len(codecs.decode(reply,'latin1'))+12
	oddByte = codecs.decode('{0:x}'.format(int(oddByte)),'hex_codec')
	reply=replyTmp+oddByte+reply
	print("REPLY: "+reply.decode('latin1'))
	if (clientVERS == "BURNOUT5/ISLAND"):
		reply=b''
	return reply
	
def reply_who():
	global pad,pad2,x00,x0A,oddByte,reply,msgType,msgSize,authsent,NO_DATA,news_cnt
	oddByte = codecs.decode('00','hex_codec')          
	replyTmp=b'+who'+pad
	uatrStr="M=VTSTech"
	reply=uatrStr.encode('ascii')+x0A
	uatrStr="N=VTSTech"
	reply+=uatrStr.encode('ascii')+x0A
	uatrStr="MA="+clientMAC
	reply+=uatrStr.encode('ascii')+x0A
	uatrStr="A=24.141.39.62"
	reply+=uatrStr.encode('ascii')+x0A
	uatrStr="LA=192.168.0.133"
	reply+=uatrStr.encode('ascii')+x0A
	uatrStr="G=0"
	reply+=uatrStr.encode('ascii')+x0A
	uatrStr="HW=0"
	reply+=uatrStr.encode('ascii')+x0A
	uatrStr="I=71615"
	reply+=uatrStr.encode('ascii')+x0A
	uatrStr="LO=enUS"
	reply+=uatrStr.encode('ascii')+x0A
	uatrStr="LV=1049601"
	reply+=uatrStr.encode('ascii')+x0A         
	uatrStr="MD=0"
	reply+=uatrStr.encode('ascii')+x0A         
	uatrStr="PRES="
	reply+=uatrStr.encode('ascii')+x0A         
	uatrStr="RP=0"
	reply+=uatrStr.encode('ascii')+x0A         
	uatrStr="S="
	reply+=uatrStr.encode('ascii')+x0A         
	uatrStr="X="         
	reply+=uatrStr.encode('ascii')+x0A                           
	uatrStr="P=1"
	reply+=uatrStr.encode('ascii')+codecs.decode('0A00','hex_codec')
	oddByte=len(codecs.decode(reply,'latin1'))+12
	oddByte = codecs.decode('{0:x}'.format(int(oddByte)),'hex_codec')
	reply=replyTmp+oddByte+reply
	print("REPLY: "+reply.decode('latin1'))
	return reply

def reply_mgm():
	p =  'CUSTFLAGS='+clientCUSTFLAGS+'\n'
	p += 'MINSIZE='+clientMINSIZE+'\n'
	p += 'MAXSIZE='+clientMAXSIZE+'\n'
	p += 'NAME=VTSTech\n'
	p += 'PARAMS='+clientPARAMS+'\n'
	p += 'PRIV='+clientPRIV+'\n'
	p += 'PRIV='+clientSEED+'\n'
	p += 'SYSFLAGS='+clientSYSFLAGS+'\n'
	p += 'MADDR='+clientMAC+'\n'
	p += 'COUNT=1\n'
	p += 'NUMPART=1\n'
	p += 'PARTSIZE0='+clientMAXSIZE+'\n'
	p += 'GPSREGION=2\n'
	p += 'GAMEPORT=9657\n'
	p += 'VOIPPORT=9667\n'
	p += 'EVGID=0\n'
	p += 'EVID=0\n'
	p += 'IDENT=6450\n'
	p += 'GAMEMODE=0\n'
	p += 'PARTPARAMS0=\n'
	p += 'ROOM=0\n'
	p += 'WHEN='+time.strftime("%Y.%m.%d-%I:%M:%S",time.localtime())+'\n'
	p += 'WHENC='+time.strftime("%Y.%m.%d-%I:%M:%S",time.localtime())+'\n'
	p += 'GPSHOST=VTSTech\n'
	p += 'HOST=VTSTech\n'
	packet = create_packet('+mgm', '', p)
	print("REPLY: "+packet.decode('latin1'))
	return packet	
	
def reply_ping(data):
	global clientALTS, clientNAME, clientVERS, clientMAC, clientPERS, clientPERSONAS, clientBORN, clientMAIL, clientSKU, clientDEFPER, clientLAST, clientPLAST, clientMADDR, clientUSER, clientMINSIZE, clientMAXSIZE, clientPARAMS, clientCUSTFLAGS, clientPRIV, clientMINSIZE, clientMAXSIZE, clientPARAMS, clientCUSTFLAGS, clientPRIV, clientSEED, clientSEED, clientSYSFLAGS
	global SKEYREPLY, SKEYSENT, z, ping_cnt, ping_start, curr_time, ping_time, msgType, msgSize, ping_sent, pad, NO_DATA
	print("Ping Recv: "+str(ping_cnt)+" Ping Sent: "+str(ping_sent))
	oddByte = codecs.decode('00','hex_codec')          
	replyTmp = b'~png'+pad
	reply = b'REF='+bytes(time.strftime("%Y.%m.%d-%I:%M:%S",time.localtime()),'ascii')+b'\n'
	reply += b'TIME=2\n'+x00
	oddByte=len(codecs.decode(reply,'latin1'))+12
	oddByte = codecs.decode('{0:x}'.format(int(oddByte)),'hex_codec')
	reply=replyTmp+oddByte+reply
	if (ping_sent>=1):
		ping_sent+=1
	else:
		ping_sent=1
	msgType=b''
	return reply
	
def build_reply(data):
  global SKEYREPLY, SKEY
  global clientALTS, clientNAME, clientVERS, clientMAC, clientPERS, clientPERSONAS, clientBORN, clientMAIL, clientSKU, clientDEFPER, clientLAST, clientPLAST, clientMADDR, clientUSER, clientMINSIZE, clientMAXSIZE, clientPARAMS, clientCUSTFLAGS, clientPRIV, clientMINSIZE, clientMAXSIZE, clientPARAMS, clientCUSTFLAGS, clientPRIV, clientSEED, clientSEED, clientSYSFLAGS
  global pad,pad2,x00,x0A,oddByte,reply,msgType,msgSize,authsent,NO_DATA,news_cnt,ping_cnt
  reply=b''
  if (msgType == codecs.decode('801C0100','hex_codec')):
    print("DEBUG: enc in")
    reply = codecs.decode('83DA04000A00','hex_codec')
  if (msgType == b'@dir'):
    tmp = data.split(codecs.decode('0A','hex_codec'))
    clientVERS = tmp[0].decode('latin1')[6:]
    if (clientVERS == "nfs-ps2-2003"):
     clientVersion = tmp[1].decode('latin1')[6:-1]
     clientSLUS = tmp[4].decode('latin1')[5:]
    elif (clientVERS == "FLM/A1"):
      clientVersion = tmp[1].decode('latin1')[4:]
      clientSLUS = tmp[2].decode('latin1')[5:]
    elif (clientVERS == "BURNOUT5/ISLAND"):
      clientSLUS = tmp[2].decode('latin1')[5:]
    
    sessStr="SESS="+str(random.randint(1000,9999))+str(random.randint(1000,9999))+str(random.randint(10,99))
    maskStr="MASK="+str(random.randint(1000,9999))+"f3f70ecb1757cd7001b9a7a"+str(random.randint(1000,9999))         	
    replyTmp=msgType+pad
    reply=SERVER_IP_BIN+x0A+SERVER_PORT_BIN+x0A
    reply+=bytes(sessStr.encode("ascii"))+x0A+bytes(maskStr.encode("ascii"))+x0A+x00
    oddByte=len(codecs.decode(reply+replyTmp,'latin1'))+1
    oddByte = codecs.decode('{0:x}'.format(int(oddByte)),'hex_codec')
    reply=replyTmp+oddByte+SERVER_IP_BIN+x0A+SERVER_PORT_BIN+x0A
    reply+=bytes(sessStr.encode("ascii"))+x0A+bytes(maskStr.encode("ascii"))+x0A+x00       
    print("REPLY: "+reply.decode('latin1'))
  if (msgType == b'skey'):
    tmp = data.split(codecs.decode('0A','hex_codec'))
    SKEY = tmp[0].decode('latin1')[5:]
    print("Client sKey: "+SKEY)              
    reply = reply_skey()
  if (msgType == b'fget'):
    reply = reply_who()
    print("REPLY: "+reply.decode('latin1'))       
  if (msgType == b'news'):
    news_cnt+=1
    if news_cnt == 1:
    	reply = cmd_news(7)
    if news_cnt == 2:
    	reply = cmd_news(8)    	
    print("REPLY: "+reply.decode('latin1'))       
  if (msgType == b'sele'):
    parse_data(data)
    p =  'INGAME=1\n'
    p += 'MYGAME=1\n'
    p += 'ASYNC=1\n'
    p += 'MESGS=0\n'
    p += 'ROOMS=0\n'
    p += 'STATS=0\n'
    p += 'USERS=0\n'
    p += 'USERSETS=0\n'
    p += 'PLATFORM=PS3\n'
    packet = create_packet('sele', '', p)
    return packet
  if ((msgType == b'auth')):
    authsent=authsent+1					
    replyTmp=msgType+pad
    parse_data(data)
    reply = reply_auth(data)
    if len(reply) > 1:
     oddByte=len(codecs.decode(reply+replyTmp,'latin1'))+1
     oddByte = codecs.decode('{0:x}'.format(int(oddByte)),'hex_codec')
     reply=replyTmp+oddByte+reply
     print("REPLY: "+reply.decode('latin1'))
  if (msgType == b'acct'):
    replyTmp=b'acct'+pad
    parse_data(data)
    reply = reply_acct(data)
    oddByte=len(codecs.decode(reply+replyTmp,'latin1'))+1
    oddByte = codecs.decode('{0:x}'.format(int(oddByte)),'hex_codec')
    reply=replyTmp+oddByte+reply
    print("REPLY: "+reply.decode('latin1'))
  if (msgType == b'pers'):
    parse_data(data)
    oddByte = codecs.decode('00','hex_codec')
    replyTmp=b'pers'+pad
    persStr="A=24.141.39.62"
    reply=persStr.encode('ascii')+x0A
    persStr='EX-telemetry=192.168.0.228,9983,enUS'
    reply=persStr.encode('ascii')+x0A
    persStr="LA=24.141.39.62"
    reply=persStr.encode('ascii')+x0A
    persStr="LOC=enUS"
    reply=persStr.encode('ascii')+x0A
    persStr="IDLE=10000"
    reply+=persStr.encode('ascii')+x0A
    persStr="MA="+clientMAC
    reply+=persStr.encode('ascii')+x0A
    if isinstance(clientNAME,str):
    	persStr="PERS="+clientNAME.lower()
    	reply+=persStr.encode('ascii')+x0A
    	persStr="NAME="+clientNAME.lower()
    else:
    	persStr="PERS="+clientNAME[0].lower()	
    	reply+=persStr.encode('ascii')+x0A
    	persStr="NAME="+clientNAME[0].lower()	
    reply+=persStr.encode('ascii')+x0A
    persStr="LAST="+time.strftime("%Y.%m.%d-%I:%M:%S",time.localtime())
    reply+=persStr.encode('ascii')+x0A
    persStr="PLAST="+time.strftime("%Y.%m.%d-%I:%M:%S",time.localtime())
    reply+=persStr.encode('ascii')+x0A
    persStr="SINCE="+time.strftime("%Y.%m.%d-%I:%M:%S",time.localtime())
    reply+=persStr.encode('ascii')+x0A
    persStr="PSINCE="+time.strftime("%Y.%m.%d-%I:%M:%S",time.localtime())
    reply+=persStr.encode('ascii')+x0A
    persStr="LKEY=3fcf27540c92935b0a66fd3b0000283c"        
    reply+=persStr.encode('ascii')+codecs.decode('0A00','hex_codec')
    oddByte=len(codecs.decode(replyTmp+reply,'latin1'))+1
    oddByte = codecs.decode('{0:x}'.format(int(oddByte)),'hex_codec')
    reply=replyTmp+oddByte+reply
    print("REPLY: "+reply.decode('latin1'))	
  if (msgType == b'sviw'):
    oddByte = codecs.decode('00','hex_codec')
    replyTmp=b'sviw'+pad         
    sviwStr="N=5"
    reply=sviwStr.encode('ascii')+x0A
    sviwStr="NAMES=0,3,4,5,6"
    reply+=sviwStr.encode('ascii')+x0A
    sviwStr="DESCS=1,1,1,1,1"
    reply+=sviwStr.encode('ascii')+x0A
    sviwStr="PARAMS=2,2,2,2,2"
    reply+=sviwStr.encode('ascii')+codecs.decode('0A00','hex_codec')
    oddByte=len(codecs.decode(reply,'latin1'))+12
    oddByte = codecs.decode('{0:x}'.format(int(oddByte)),'hex_codec')
    reply=replyTmp+oddByte+reply
    print("REPLY: "+reply.decode('latin1'))
  if (msgType == b'uatr'):
    time.sleep(1)
    reply = reply_who()
    print("REPLY: "+reply.decode('latin1'))
    time.sleep(1)
  if (msgType == b'usld'):
    parse_data(data)
    p =  'IMGATE=0\n'
    p += 'QMSG0=TEST0\n'
    p += 'QMSG1=TEST1\n'
    p += 'QMSG2=TEST2\n'
    p += 'QMSG3=TEST3\n'
    p += 'QMSG4=TEST4\n'
    p += 'QMSG5=TEST5\n'
    p += 'SPM_EA=0\n'
    p += 'SPM_PART=0\n'
    p += 'UID=$000000000b32588d\n'
    packet = create_packet('usld', '', p)
    return packet
    time.sleep(1)
  if (msgType == b'slst'):
    parse_data(data)
    p='COUNT=27'                                     
    p+='VIEW0=lobby,"Online Lobby Stats View\n'      
    p+='VIEW1=DLC,"DLC Lobby Stats View\n'           
    p+='VIEW2=RoadRules,"Road Rules\n'               
    p+='VIEW3=DayBikeRRs,"Day Bike Road Rules\n'     
    p+='VIEW4=NightBikeRR,"Night Bike Road Rules\n'  
    p+='VIEW5=PlayerStatS,"Player Stats Summary\n'   
    p+='VIEW6=LastEvent1,"Recent Event 1 Details\n'  
    p+='VIEW7=LastEvent2,"Recent Event 2 Details\n'  
    p+='VIEW8=LastEvent3,"Recent Event 3 Details\n'  
    p+='VIEW9=LastEvent4,"Recent Event 4 Details\n'  
    p+='VIEW10=LastEvent5,"Recent Event 5 Details\n' 
    p+='VIEW11=OfflineProg,"Offline Progression\n'   
    p+='VIEW12=Rival1,"Rival 1 information\n'        
    p+='VIEW13=Rival2,"Rival 2 information\n'        
    p+='VIEW14=Rival3,"Rival 3 information\n'        
    p+='VIEW15=Rival4,"Rival 4 information\n'        
    p+='VIEW16=Rival5,"Rival 5 information\n'        
    p+='VIEW17=Rival6,"Rival 6 information\n'        
    p+='VIEW18=Rival7,"Rival 7 information\n'        
    p+='VIEW19=Rival8,"Rival 8 information\n'        
    p+='VIEW20=Rival9,"Rival 9 information\n'        
    p+='VIEW21=Rival10,"Rival 10 information\n'      
    p+='VIEW22=DriverDetai,"Driver details\n'        
    p+='VIEW23=RiderDetail,"Rider details\n'         
    p+='VIEW24=IsldDetails,"Island details\n'        
    p+='VIEW25=Friends,"Friends List\n'              
    p+='VIEW26=PNetworkSta,"Paradise Network Stats\n'
    packet = create_packet('slst', '', p)
    return packet
  if (msgType == b'cate'):
    parse_data(data)
    reply = create_packet('cate', '', '')
  if (msgType == b'gqwk'):
    parse_data(data)
    reply = create_packet('gqwk', '', '')
  if (msgType == b'gpsc'):
    parse_data(data)
    reply = reply_mgm()
  if (msgType == b'cper'):
    parse_data(data)
    replyTmp=b'cper'+pad
    reply = reply_cper(data)
    oddByte=len(codecs.decode(reply,'latin1'))+12
    oddByte = codecs.decode('{0:x}'.format(int(oddByte)),'hex_codec')
    reply=replyTmp+oddByte+reply
    print("REPLY: "+reply.decode('latin1'))
    time.sleep(1)
  if (msgType == b'gsea'):
    replyTmp=b'gsea'+pad
    gseaStr="COUNT=0"         
    reply=gseaStr.encode('ascii')+codecs.decode('0A00','hex_codec')
    oddByte=len(codecs.decode(reply,'latin1'))+12
    oddByte = codecs.decode('{0:x}'.format(int(oddByte)),'hex_codec')
    reply=replyTmp+oddByte+reply
    print("REPLY: "+reply.decode('latin1'))
    time.sleep(1)
	#ping				
  if (msgType == b'~png'):
    ping_start=time.time()
    if (ping_cnt>=1):
     ping_cnt+=1
    else:
     ping_cnt=1          
    reply = reply_ping(data)
    time.sleep(2)

  return reply
       
def threaded_client(connection):
	global SKEYREPLY, SKEYSENT, z, ping_cnt, ping_start, curr_time, ping_time, ping_sent
	global pad,pad2,x00,x0A,oddByte,reply,msgType,msgSize,authsent,NO_DATA,news_cnt
	connection.settimeout(500)
	while True:        
		curr_time=time.time()
		try:
		 tmp = connection.recv(12)
		 NO_DATA=False
		except:
		 NO_DATA=True
		 time.sleep(0.5)
		 curr_time=time.time()            
		 #reply=b''
		 #if not NO_DATA==True:
		 #	print("! end of data ... let's wait for some...")
		 #	for x in range(0,60):
		 #		try:
		 #			tmp = connection.recv(12)
		 #		except:
		 #			time.sleep(0.2)
		msgType = tmp[:4]
		print("RECV: "+str(msgType))
		if tmp[10] == 0:
			msgSize=tmp[11]
			print("SIZE1: "+(str(msgSize)))
		else:
			msgSize = tmp[10]
			msgSize += tmp[11]
			msgSize = int(struct.unpack(">h",bytes(str(msgSize),'ascii'))[0])
			print("SIZE2: "+(str(msgSize)))		
		msgSize = msgSize - 12
		data = connection.recv(msgSize)
		print("SIZE3: "+(str(msgSize)))
		time.sleep(0.2)
		reply = build_reply(data)
		connection.sendall((reply))
		if (msgType == b'pers'):
			reply = reply_who()
			connection.sendall((reply))
		if (msgType == b'gpsc'):
			reply = reply_who()
			connection.sendall((reply))
while True:
		CLIENT, ADDRESS = GameSocket.accept()
		print('Player Connected from: ' + ADDRESS[0] + ':' + str(ADDRESS[1]))
		start_new_thread(threaded_client, (CLIENT, ))
		THREADCOUNT += 1
		print('Thread Number: ' + str(THREADCOUNT))
		CLIENT, ADDRESS = LISTENERSocket.accept()
		print('LISTENER Connected from: ' + ADDRESS[0] + ':' + str(ADDRESS[1]))
		start_new_thread(threaded_client, (CLIENT, ))
		THREADCOUNT += 1
		print('Thread Number: ' + str(THREADCOUNT))    
		CLIENT, ADDRESS = BuddySocket.accept()
		print('Buddy Connected from: ' + ADDRESS[0] + ':' + str(ADDRESS[1]))
		start_new_thread(threaded_client, (CLIENT, ))
		THREADCOUNT += 1
		print('Thread Number: ' + str(THREADCOUNT))