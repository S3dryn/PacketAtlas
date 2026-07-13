from scapy.all import*

file = rdpcap("./smallFlows.pcap")
convoCount = 1
conversations = {}
# structure of this dict:
# conversations = { convoid: [{timestamp , ip, type , ..}], convoid: [{timestamp , ip, type , ..}], ....}


# sample packet 
# ###[ Ethernet ]###
#   dst       = ff:ff:ff:ff:ff:ff
#   src       = 40:61:86:9a:f1:f5
#   type      = IPv4
# ###[ IP ]###
#      version   = 4
#      ihl       = 5
#      tos       = 0x0
#      len       = 148
#      id        = 13784
#      flags     = 
#      frag      = 0
#      ttl       = 128
#      proto     = udp
#      chksum    = 0x7bae
#      src       = 192.168.3.131
#      dst       = 192.168.3.255
#      \options   \
# ###[ UDP ]###
#         sport     = 17500
#         dport     = 17500
#         len       = 128
#         chksum    = 0xf43f
# ###[ Raw ]###
#            load      = b'{"host_int": 20473467, "version": [1, 8], "displayname": "Trevor-PC", "port": 17500, "namespaces": [13068657, 13069042]}'

def makeConvo(insertdict,convoCount):
    conversations[convoCount] = {}
    conversations[convoCount]["index"] = 0
    conversations[convoCount]["state"] = "idle"
    conversations[convoCount]["info"] = []
    conversations[convoCount]["info"].append(insertdict)
    convoCount +=1




for packet in file:
    # To sort out ARP packets
    if packet.haslayer("IP"):
        # making the object that will be inserted
        insertdict = {}
        insertdict["time"] = packet.time
        insertdict['src_ip'] = packet["IP"].src
        insertdict['dst_ip'] = packet["IP"].dst
        
        if packet.haslayer("TCP"):
            insertdict["type"]  = "TCP"
        else:
            insertdict["type"]  = "UDP"
        
        # sorting the packet
        if len(conversations) != 0:
            match = False
            for val in conversations.values():
                #checking if a similar packet exists
                if ((val["info"][0]['src_ip'] == insertdict['src_ip'] and val["info"][0]['dst_ip'] == insertdict['dst_ip']) or (val["info"][0]['src_ip'] == insertdict['dst_ip'] and val["info"][0]['dst_ip'] == insertdict['src_ip'])) and val["info"][0]['type'] == insertdict["type"]:
                    val["info"].append(insertdict)
                    match = True
                    break
            
            if not match:
                makeConvo(insertdict, convoCount)
        else:
            makeConvo(insertdict, convoCount)
    
for cnv in conversations.values():
    print(cnv[0])

print(convoCount)
