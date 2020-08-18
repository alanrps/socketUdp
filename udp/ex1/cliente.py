import threading
import socket
import hashlib
import os
import time 
import sys
from random import randint

class ClientUdp():
    def __init__(self,ipEnvio, portEnvio, ipRecebimento, portRecebimento):
        self.ipEnvio = ipEnvio
        self.portEnvio = portEnvio
        self.ipRecebimento = ipRecebimento
        self.portRecebimento = portRecebimento

    def getIpEnvio(self):
        return self.ipEnvio
    
    def getPortEnvio(self):
        return self.portEnvio
    
    def getIpRecebimento(self):
        return self.ipRecebimento

    def getPortRecebimento(self):
        return self.portRecebimento

    def enviaMensagem(self, clientSocket, clientUdp):
      addr = (clientUdp.getIpEnvio(), clientUdp.getPortEnvio())
      while 1:
        mensagem = input("Digite sua mensagem\n")
        if(len(mensagem.encode('utf-8')) > 255):
          print("Erro, Mensagem maior que s255 bytes")
        else:
          mensagem = (str(len(apelido)) + '/' + apelido + '/' + str(len(mensagem)) + '/' + mensagem)
          clientSocket.sendto(mensagem.encode('utf-8'), addr)


    def recebeMensagem(self, clientSocket, clientUdp):
      addr = (clientUdp.getIpRecebimento(),clientUdp.getPortRecebimento())
      clientSocket.bind(addr)

      while 1:
        data, addr = clientSocket.recvfrom(1024)
        mensagem = data.decode('utf-8').split('/')
        print (mensagem[1] +"#" + mensagem[-1])

global apelido
ipEnvio = sys.argv[1]
portEnvio = int(sys.argv[2])
ipRecebimento = sys.argv[3]
portRecebimento = int(sys.argv[4])

clientUdp = ClientUdp(ipEnvio,portEnvio,ipRecebimento,portRecebimento)
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while 1:
  apelido = input("Defina seu apelido:")
  if (len(apelido.encode('utf-8')) <= 255): 
    break

    print("Erro, apelido muito grande")
    pass

try:
  threadEnviaMensagem = threading.Thread(target=clientUdp.enviaMensagem, args=(clientSocket,clientUdp ))
  threadRecebeMensagem = threading.Thread(target=clientUdp.recebeMensagem, args=(clientSocket,clientUdp ))
  
  threadEnviaMensagem.start()
  threadRecebeMensagem.start()

except ValueError:
  print(ValueError)
  print("Erro ao criar thread!")

# clientSocket.close()





