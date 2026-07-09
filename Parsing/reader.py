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



for packet in file:
    # To sort out ARP packets
    if packet.haslayer("IP"):
        # making the object that will be inserted
        insertdict = {}
        insertdict["time"] = packet.time
        insertdict['srcip'] = packet["IP"].src
        insertdict['dstip'] = packet["IP"].dst
        if packet.haslayer("TCP"):
            insertdict["type"]  = "TCP"
        else:
            insertdict["type"]  = "UDP"
        # sorting the packet
        if len(conversations) != 0:
            match = False
            for val in conversations.values():
                #checking if a similar packet exists
                if ((val[0]['srcip'] == insertdict['srcip'] and val[0]['dstip'] == insertdict['dstip']) or (val[0]['srcip'] == insertdict['dstip'] and val[0]['dstip'] == insertdict['srcip'])) and val[0]['type'] == insertdict["type"]:
                    val.append(insertdict)
                    match = True
                    break
            
            if not match:
                conversations[convoCount] = []
                conversations[convoCount].append(insertdict)
                convoCount += 1
        else:
            conversations[convoCount] = []
            conversations[convoCount].append(insertdict)
            convoCount += 1
    
for cnv in conversations.values():
    print(cnv[0])

print(convoCount)
