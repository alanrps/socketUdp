import socket
import hashlib

class ServerUdp():
    def __init__(self, ip):
        self.ip = ip
        self.port = 5000

    def getIp(self):
        return self.ip
    
    def getPort(self):
        return self.port

    def recebeArquivos(self, serverSocket):
        while 1:
            arquivo = b'' # Cria arquivo
            idPacote = 0 # Controle de identificação de pacotes
            quantidadePacotes = 0 # Controla a quantidade de pacotes

            hashMd5 = hashlib.md5() # Gera hashMd5
            while 1:
              data, addr = serverSocket.recvfrom(1024)  #Recebe o arquivo

              if(idPacote == 0):
                  nome = data.decode('utf-8').split('/')[1] # Separa o nome por "/" e converte de Byte para string
                  quantidadePacotes = round(int(data.decode('utf-8').split('/')[0]) / 1024 + 2 + 0.5) # Separa a quantidade de pacotes por "/" e converte de Byte para inteiro

              elif(idPacote == quantidadePacotes -1): # Verifica se o pacote é o ultimo
                  md5 = data.decode('utf-8')  
                  break

              else:
                  arquivo += data # Faz a concatenação dos pacotes
                  hashMd5.update(data) # Atualiza hashMd5
              
              idPacote += 1
              pass

            if(hashMd5.hexdigest() == md5):
              print("Arquivo salvo")
              status = "0"
              serverSocket.sendto(status.encode('utf-8'), addr)

              with open('arquivos/' + nome, 'wb') as pedacoArquivo: # Salva os arquivos pasta 'arquivos'
                pedacoArquivo.write(arquivo)

            else:
              print("Erro integridade")
              status = "1"
              serverSocket.sendto(status.encode('utf-8'), addr)  # Envia status de recebimento do arquivo



serverUdp = ServerUdp("127.0.0.1")
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
addr = (serverUdp.getIp(), serverUdp.getPort())
print(addr)
serverSocket.bind(addr)
serverUdp.recebeArquivos(serverSocket)
