from dnslib.server import DNSServer, BaseResolver, DNSLogger
from dnslib import RR, QTYPE, TXT

class FlagResolver(BaseResolver):
    def resolve(self, request, handler):
        reply = request.reply()
        qname = request.q.qname
        qtype = request.q.qtype
        if qtype == QTYPE.TXT and str(qname).lower() == "flag.ctf.computernetworking.usi.ch.":
            reply.add_answer(RR(qname, QTYPE.TXT, ttl=60, rdata=TXT("CTF{dns_txt_records_are_fun}")))
        return reply

if __name__ == "__main__":
    resolver = FlagResolver()
    server = DNSServer(resolver, port=31100, address="0.0.0.0", logger=DNSLogger(log="", prefix=""))
    print("[+] DNS Server running on port 31100")
    server.start()
