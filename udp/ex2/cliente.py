from tkinter import Tk
from tkinter.filedialog import askopenfilename
from threading import Thread 
import socket
import hashlib
import os
import time 

class ClientUdp():
    def __init__(self, ip):
        self.ip = ip
        self.port = 5000

    def getIp(self): 
        return self.ip 
    
    def getPort(self):
        return self.port

    def enviaArquivos(self, clientSocket):
        while 1:
            hashMd5 = hashlib.md5() # Gera hashMd5

            Tk().withdraw() # Isto torna oculto a janela principal
            path = askopenfilename() # Isto te permite selecionar um arquivo e retorna o path do arquivo
            print(path) 

            if(path == False): # Caso cancelar a seleção de arquivo
                break

            if(os.path.isfile(path) and os.path.exists(path)): # Verifica se o path é um arquivo e se ele existe
                tam = os.path.getsize(path) # Tamanho do arquivo
                nome = os.path.basename(path) # Obtem o nome base do arquivo
                clientSocket.sendto((str(tam) + "/" + nome).encode('utf-8'), addr)  # Envia o tamanho e nome do arquivo primeiramente

                with open(path, "rb") as arquivo:
                    for pedacoArquivo in iter(lambda: arquivo.read(1024), b""): # Lê arquivo de 1024 em 1024 Bytes
                        hashMd5.update(pedacoArquivo) # Atualiza hash md5
                        clientSocket.sendto(pedacoArquivo, addr) # Enviando arquivo
                        time.sleep(0.01) 
                
                clientSocket.sendto(hashMd5.hexdigest().encode('utf-8'), addr) # Enviando checksum(hash md5)

                # time.sleep(1)
                data = clientSocket.recvfrom(1024) # Recebe arquivos
                resposta = data[0].decode('utf-8')
                if(resposta == "0"):
                    print("Enviado com sucesso\n")
                else:
                    print("Erro com integridade do arquivo\n")

            else:
                break
    

clientUdp = ClientUdp("127.0.0.1")
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
addr = (clientUdp.getIp(), clientUdp.getPort())
print(addr)
clientUdp.enviaArquivos(clientSocket)
clientUdp.recebeArquivos(clientSocket)
clientSocket.close()


