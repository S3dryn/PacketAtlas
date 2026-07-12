import pygame
import sys
import random
import math
pygame.init()

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

running = True
xcoords = 300
ycoords = 400


conversations = {
    "conv_001":{ "index": 0,
                "state":"idle",
          "info": [
        {
            "timestamp": 0.000,
            "src_ip": "192.168.1.10",
            "dst_ip": "142.250.183.78",
            "protocol": "TCP",
            "src_port": 52341,
            "dst_port": 443,
            "flags": "SYN",
            "length": 60,
        },
        {
            "timestamp": 0.032,
            "src_ip": "142.250.183.78",
            "dst_ip": "192.168.1.10",
            "protocol": "TCP",
            "src_port": 443,
            "dst_port": 52341,
            "flags": "SYN,ACK",
            "length": 60,
        },
        {
            "timestamp": 0.048,
            "src_ip": "192.168.1.10",
            "dst_ip": "142.250.183.78",
            "protocol": "TCP",
            "src_port": 52341,
            "dst_port": 443,
            "flags": "ACK",
            "length": 52,
        },
        {
            "timestamp": 0.081,
            "src_ip": "192.168.1.10",
            "dst_ip": "142.250.183.78",
            "protocol": "HTTP",
            "method": "GET",
            "length": 512,
        },
        {
            "timestamp": 0.150,
            "src_ip": "142.250.183.78",
            "dst_ip": "192.168.1.10",
            "protocol": "HTTP",
            "status": 200,
            "length": 1384,
        },
    ]},

    "conv_002": { "index": 0,
                 "state":"idle",
          "info":[
        {
            "timestamp": 0.400,
            "src_ip": "192.168.1.10",
            "dst_ip": "8.8.8.8",
            "protocol": "DNS",
            "query": "www.example.com",
            "length": 74,
        },
        {
            "timestamp": 0.423,
            "src_ip": "8.8.8.8",
            "dst_ip": "192.168.1.10",
            "protocol": "DNS",
            "answer": "93.184.216.34",
            "length": 90,
        },
    ]},

    "conv_003": { "index": 0,
                 "state":"idle",
          "info":[
        {
            "timestamp": 1.015,
            "src_ip": "192.168.1.10",
            "dst_ip": "192.168.1.1",
            "protocol": "ICMP",
            "type": "Echo Request",
            "length": 64,
        },
        {
            "timestamp": 1.028,
            "src_ip": "192.168.1.1",
            "dst_ip": "192.168.1.10",
            "protocol": "ICMP",
            "type": "Echo Reply",
            "length": 64,
        },
    ]},
}



class Packet:
      def __init__(self,x,y,speed,info,width,length,state,convo,color):
            self.x = x
            self.y = y
            self.width = width
            self.length = length
            self.speed = speed
            self.info = info
            self.state = state
            self.convo = convo
            self.color = color
      def update(self,dt,trgtx,trgty):

            t = min(self.speed * dt, 1.0)
            
            self.x = pygame.math.lerp(self.x, trgtx, t)
            self.y = pygame.math.lerp(self.y, trgty, t)
            distance = math.hypot(trgtx - self.x, trgty - self.y)
            if distance < 5.0:
                  self.state = "done"

      def draw(self):
            Rect = pygame.Rect(self.x,self.y,self.width,self.length)
            pygame.draw.rect(screen,self.color,Rect)

class Machine:
      def __init__(self,x,y,speed,info,width,length):
            self.x = x
            self.y = y
            self.width = width
            self.length = length
            self.speed = speed
            self.info = info
      def update(self,keys):
            if keys[pygame.K_w]:
                  self.y -= self.speed
            
            if keys[pygame.K_d]:
                  self.x += self.speed
            
            if keys[pygame.K_s]:
                  self.y += self.speed
            if keys[pygame.K_a]:
                  self.x -= self.speed

      def draw(self):
            Rect = pygame.Rect(self.x,self.y,self.width,self.length)
            pygame.draw.rect(screen,(7,3,252),Rect)

ips = set()
machines = {}

for convo in conversations.values():
      src_ip = convo["info"][0]["src_ip"]
      dst_ip = convo["info"][0]["dst_ip"]
      ips.add(src_ip)
      ips.add(dst_ip)


 # getting points on a circle for the arrangement
n = len(ips)
stepang = (2 *math.pi)/n 
center = (SCREEN_WIDTH/2,SCREEN_HEIGHT/2)
radius = 150
count = 0
angles = []
points = []
for i in range(n):
      angles.append(count)
      count += stepang

for angle in angles:
      point = {
            "x": center[0] + radius* math.cos(angle),
            "y": center[1] + radius * math.sin(angle)
      }
      points.append(point)

pointsIndex = 0




for ip in ips:
      
      machine = Machine(points[pointsIndex]["x"],points[pointsIndex]["y"],0,ip,30,30)
      machines[ip] = machine
      pointsIndex +=1


def drawMachines():

      for machine in machines.values():
            machine.draw()


dt = 0
activePackets = []


 #  packet creation 
def CheckStateConv():
      for key,convo in conversations.items():
            if convo["state"] == "idle":
                  items = len(convo["info"])
                  color = (random.randrange(0,255),random.randrange(0,255),random.randrange(0,255))
                  packetInfo = convo["info"][convo["index"]]
                  packetx = machines[packetInfo["src_ip"]].x + random.randrange(5,10)
                  packety = machines[packetInfo["src_ip"]].y + random.randrange(5,10)
                  packet = Packet(packetx,packety,1,packetInfo,20,20,"running",key,color)
                  activePackets.append(packet)
                  convo["state"] = "running"

                  if convo["index"] +1 >= items:
                        convo["state"] = "done"
                  else:
                        convo["index"] +=1
# packet updating
def UpdatePackets(dt):
      for packet in activePackets:
            trgtx = machines[packet.info["dst_ip"]].x
            trgty = machines[packet.info["dst_ip"]].y
            packet.update(dt,trgtx,trgty)

#packet end
def KillPackets():
      for packet in activePackets:
            if packet.state == "done":
                  convo = packet.convo
                  length = len(conversations[convo]["info"])
                  index = conversations[convo]["index"]
                  if conversations[convo]["state"] == "done":
                        pass
                  else:
                        conversations[convo]["state"] = "idle"

                  activePackets.remove(packet)
            





while running:

      for event in pygame.event.get():
                  if event.type == pygame.QUIT:
                        running = False


      keys = pygame.key.get_pressed()
      
      
      KillPackets()
      CheckStateConv()
      UpdatePackets(dt)
      


      screen.fill((0,0,0))
      for packet in activePackets:
            packet.draw()
      drawMachines()
      pygame.display.flip()
      dt = clock.tick(60)/1000

pygame.quit()
sys.exit()

    