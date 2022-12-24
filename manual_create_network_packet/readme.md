# the packet blueprint 


|      0000|      0000|      0000|      0000|      0000|      0000|      0000|      0000|
|       ---|       ---|       ---|       ---|       ---|       ---|       ---|       ---|
|<a>Version|<a>IHL    |<a>Type  -|of service|<a>Tot   -|al       -|len      -|ngth      |
|<a>Identi-|fication  |          |          |<a>Flags  |<a>Frag  -|ment  off-|set       |
|T_ime to -|live      |P_roto   -|col       |H_ead    -|er       -|check    -|sum      -|
|<a>S     -|our      -|ce       -|Ad       -|dr       -|e        -|s        -|s         |
|<a>Dest  -|ina      -|tio      -|Ad       -|dr       -|e        -|s        -|s         |
|<a>Sou   -|ce       -|po       -|rt        |<a>Desti -|nation   -|po       -|rt        |
|<a>Se    -|quen     -|ce       -|nu       -|m        -|b        -|e        -|r         |
|<a>Ackno -|wledge   -|ment     -|nu       -|m        -|b        -|e        -|r         |
|<a>Dtaoffs|<a>x      |<a>xxxx   |<a>xxxx   |<a>Win   -|dow      -|si       -|ze        |
|<a>che   -|ck       -|su       -|m         |<a>Ur    -|gent     -|poin     -|ter       |

## IP internet protocol
- connectionless 
    - datacorruption may occur
    - package loss   may occur
- packages also called datagram
- ipv4 version exists
- ipv6 version exists

format is 

|version         |IHL             |type of service |total length    |
|identification                   |flags   |fragment offset         |
|Time to live    |Protocol        |Header Checksum                  |
|Source address                                                     |
|Destination address                                                |
|Otions variable + padding                                          |
|Data variable                                                      |

### version (4 bits)

indicates the version (IPv4 or IPv6)

### IHL (4 bits)

IP header length in 32bit words

min val: 5 words

max val: 15 words => 32bits * 15 = 480bits == 60bytes

### type of service(8 bits)
also "differentiated services" 

used for quality of service 

first 6 bits are DSCP (differentiated services code point)

the last 2 bits are the ENC (explicit congestion notification)

used to notify the receiver in case of network congestion

### total length(16 bits)
in bytes

max is (2^16-1) = 65 535 Bytes ! so 65 kilobytes

### identification (16 bits)

all fragments of a packet have the same identification number 

### flags (3 bits)
0 0 0 
    ^ MF(more fragments)

  ^ DF (Dont fragment)

^ bit not used

#### DF dont fragment
tells the router to not fragment the packet

#### MF more fragments 
indicates that more fragments are about to come 

all (!but the last!) fragments have this bit set

### fragment offset (8 bits)
the index of the current fragment in all of the fragments

### time to live (8 bits)
a number which is decreased by every router  on the packages way

when it hits zero the router will discard the package and send a ICMP error message to the sender

### Protocol (8 bits)
next level protocl 

for example 
tcp: value 6
udp: value 17

### header checksum (16 bits)
checksum on the header only

### source address (32 bits)
source ip address

### destination address (32 bits)
destination ip addressa

### options (variable bits)
optional , in case used it must be padded to match a multiple of 32 bits

### data (variable bits)
payload of the data, the data is not part of the header and therefore not included in the header checksum

