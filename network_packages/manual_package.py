from copyreg import constructor
import socket
import time 

# s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
# s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

# ip_header  = b'\x45\x00\x00\x28'  # Version, IHL, Type of Service | Total Length
# ip_header += b'\xab\xcd\x00\x00'  # Identification | Flags, Fragment Offset
# ip_header += b'\x40\x06\xa6\xec'  # TTL, Protocol | Header Checksum
# ip_header += b'\x0a\x0a\x0a\x02'  # Source Address
# ip_header += b'\x0a\x0a\x0a\x01'  # Destination Address
# # ip_header += bytes([127,0,0,1])
# # ip_header += bytes([127,0,0,1])
# tcp_header  = b'\x30\x39\x00\x50' # Source Port | Destination Port
# tcp_header += b'\x00\x00\x00\x00' # Sequence Number
# tcp_header += b'\x00\x00\x00\x00' # Acknowledgement Number
# tcp_header += b'\x50\x02\x71\x10' # Data Offset, Reserved, Flags | Window Size
# tcp_header += b'\xe6\x32\x00\x00' # Checksum | Urgent Pointer
# print(ip_header)
# packet = ip_header + tcp_header
# s.sendto(packet, ('10.10.10.1', 0))

n_i = 0 
while(n_i < 1000):
    time.sleep(0.1)

    s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
    s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

    ip_header  = b'\x45\x00\x00\x28'  # Version, IHL, Type of Service | Total Length
    ip_header += b'\xab\xcd\x00\x00'  # Identification | Flags, Fragment Offset
    ip_header += b'\x40\x06\xa6\xec'  # TTL, Protocol | Header Checksum
    # ip_header += b'\x0a\x0a\x0a\x02'  # Source Address
    # ip_header += b'\x0a\x0a\x0a\x01'  # Destination Address
    ip_header +=bytes([127,0,0,1])
    ip_header +=bytes([127,0,0,1])
    tcp_header  = b'\x30\x39\x00\x50' # Source Port | Destination Port
    tcp_header += b'\x00\x00\x00\x00' # Sequence Number
    tcp_header += b'\x00\x00\x00\x00' # Acknowledgement Number
    tcp_header += b'\x50\x02\x71\x10' # Data Offset, Reserved, Flags | Window Size
    # if(n_i %2 == 0 ):
        # tcp_header += b'\xe6\x32\x00\x00' # Checksum | Urgent Pointer
    # else: 
        # tcp_header += b'\xe6\x32\x00\x01' # Checksum | Urgent Pointer
    # ip_header +=bytes([230,50,0,0])
    ip_header +=b'\xe6\x32\x00'
    ip_header +=bytes([n_i])

    packet = ip_header + tcp_header
    s.sendto(packet, ('127.0.0.1', 0))

    n_i+=1