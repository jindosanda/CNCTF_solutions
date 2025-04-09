# You can solve this challenge using dig:
# dig @ctf.computernetworking.usi.ch -p 31100 TXT flag.ctf.computernetworking.usi.ch

from dnslib import DNSRecord, QTYPE
import socket

host = "ctf.computernetworking.usi.ch" 
port = 31100

qname = "flag.ctf.computernetworking.usi.ch"
q = DNSRecord.question(qname, qtype="TXT")

# Send UDP query manually
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(2)
sock.sendto(q.pack(), (host, port))

data, _ = sock.recvfrom(1024)
response = DNSRecord.parse(data)

for rr in response.rr:
    if rr.rtype == QTYPE.TXT:
        print("🎉 Flag:", ''.join([txt.decode() for txt in rr.rdata.data]))
