import socket

# Nosso banco de dados simulado
banco_de_carros = {
    "ferrari": {
        "nome": "Ferrari 458 Italia",
        "imagem": "/img/ferrari.jpg",
        "preco": "R$ 2.000.000",
        "descricao": "Ferrari 458 Italia 4.5 V8 32V Gasolina F1-DCT - Vermelho - 2011",
        "cavalos": "570 CV",
        "cilindros": "V8",
    },
    "porsche": {
        "nome": "Porsche 911 Carrera S",
        "imagem": "/img/porsche.jpg",
        "preco": "R$ 1.100.000",
        "descricao": "Porsche 911 Carrera S 3.0 24V H6 Gasolina PDK - Prata - 2024",
        "cavalos": "450 CV",
        "cilindros": "H6 (Boxer)",
    },
    "uno": {
        "nome": "Fiat Uno Mille Way",
        "imagem": "/img/uno.jpg",
        "preco": "R$ 30.000",
        "descricao": "Fiat Uno Mille Way Economy 1.0 Fire Flex Manual - Branco - 2013",
        "cavalos": "66 CV",
        "cilindros": "L4",
    },
    "mercedes": {
        "nome": "Mercedes-Benz 300 SL",
        "imagem": "/img/mercedes.jpg",
        "preco": "R$ 15.000.000",
        "descricao": "Mercedes-Benz 300 SL Gullwing 3.0 L6 Gasolina Manual - Prata - 1955",
        "cavalos": "215 CV",
        "cilindros": "L6",
    },
    "lamborghini": {
        "nome": "Lamborghini Aventador",
        "imagem": "/img/aventador.jpg",
        "preco": "R$ 4.500.000",
        "descricao": "Lamborghini Aventador LP 700-4 6.5 V12 Gasolina ISR - Laranja - 2018",
        "cavalos": "700 CV",
        "cilindros": "V12",
    },
    "nissan": {
        "nome": "Nissan Skyline GT-R R34",
        "imagem": "/img/skyline.jpg",
        "preco": "R$ 1.200.000",
        "descricao": "Nissan Skyline GT-R V-Spec II 2.6 L6 Biturbo Manual - Azul - 2002",
        "cavalos": "280 CV",
        "cilindros": "L6",
    },
    "chevrolet": {
        "nome": "Chevrolet Corvette C8",
        "imagem": "/img/corvette.jpg",
        "preco": "R$ 1.300.000",
        "descricao": "Chevrolet Corvette Stingray 6.2 V8 Gasolina Dual-Clutch - Amarelo - 2023",
        "cavalos": "495 CV",
        "cilindros": "V8",
    }
}



#definindo o endereço IP do host
SERVER_HOST = ""
#definindo o número da porta em que o servidor irá escutar pelas requisições HTTP
SERVER_PORT = 8080

#vamos criar o socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#vamos setar a opção de reutilizar sockets já abertos
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

#atrela o socket ao endereço da máquina e ao número de porta definido
server_socket.bind((SERVER_HOST, SERVER_PORT))

#coloca o socket para escutar por conexões
server_socket.listen(1)

#mensagem inicial do servidor
print("Servidor em execução...")
print("Escutando por conexões na porta %s" % SERVER_PORT)

#cria o while que irá receber as conexões
while True:
    #espera por conexões
    #client_connection: o socket que será criado para trocar dados com o cliente de forma dedicada
    #client_address: tupla (IP do cliente, Porta do cliente)
    client_connection, client_address = server_socket.accept()

    #pega a solicitação do cliente
    request = client_connection.recv(1024).decode('utf-8')
    #verifica se a request possui algum conteúdo (pois alguns navegadores ficam periodicamente enviando alguma string vazia)
    if request:
        #imprime a solicitação do cliente
        # print("INICIO Request:", request, "FIM REQUEST")

        #analisa a solicitação HTTP
        headers = request.split("\n")
        method = headers[0].split()[0]
        print(method)
        if method == 'GET':
            # pega o nome do arquivo sendo solicitado
            filename = headers[0].split()[1]
            print("\nFilename = ", filename, "\n")
            #verifica qual arquivo está sendo solicitado e envia a resposta para o cliente
            if filename == "/":
                filename = "/index.html"

            #try e except para tratamento de erro quando um arquivo solicitado não existir
            try:
                print("htdocs" + filename)
                #abrir o arquivo e enviar para o cliente
                fin = open("htdocs" + filename)
                #leio o conteúdo do arquivo para uma variável
                content = fin.read()
                #fecho o arquivo
                fin.close()
                #envia a resposta
                response = "HTTP/1.1 200 OK\n\n" + content
            except FileNotFoundError:
                #caso o arquivo solicitado não exista no servidor, gera uma resposta de erro
                response = "HTTP/1.1 404 NOT FOUND\n\n<h1>ERROR 404!<br>File Not Found!</h1>"
            #envia a resposta HTTP
            client_connection.sendall(response.encode())
        elif method == 'POST':
            try:
                dados = headers[0].split()[1]
                print(dados)
            except FileNotFoundError:
                response = "HTTP/1.1 404 NOT FOUND\n\n<h1>ERROR 404!<br>File Not Found!</h1>"
        else:
            client_connection.close()

server_socket.close()
