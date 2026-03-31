import socket

banco_de_carros = {
    "ferrari": {
        "nome": "Ferrari 458 Italia",
        "imagem": "/img/ferrari.jpg",
        "preco": "R$ 2.000.000",
        "ano": "2020",
        "descricao": "Ferrari 458 Italia 4.5 V8 32V Gasolina F1-DCT - Vermelho - 2011",
        "cavalos": "570 CV",
        "cilindros": "V8",
    },
    "porsche": {
        "nome": "Porsche 911 Carrera S",
        "imagem": "/img/porsche.jpg",
        "preco": "R$ 1.100.000",
        "ano": "2020",
        "descricao": "Porsche 911 Carrera S 3.0 24V H6 Gasolina PDK - Prata - 2024",
        "cavalos": "450 CV",
        "cilindros": "H6 (Boxer)",
    },
    "uno": {
        "nome": "Fiat Uno Mille Way",
        "imagem": "/img/uno.jpg",
        "preco": "R$ 30.000",
        "ano": "2020",
        "descricao": "Fiat Uno Mille Way Economy 1.0 Fire Flex Manual - Branco - 2013",
        "cavalos": "66 CV",
        "cilindros": "L4",
    },
    "mercedes": {
        "nome": "Mercedes-Benz 300 SL",
        "imagem": "/img/mercedes.jpg",
        "preco": "R$ 15.000.000",
        "ano": "2020",
        "descricao": "Mercedes-Benz 300 SL Gullwing 3.0 L6 Gasolina Manual - Prata - 1955",
        "cavalos": "215 CV",
        "cilindros": "L6",
    },
    "lamborghini": {
        "nome": "Lamborghini Aventador",
        "imagem": "/img/lamborghini.jpg",
        "preco": "R$ 4.500.000",
        "ano": "2020",
        "descricao": "Lamborghini Aventador LP 700-4 6.5 V12 Gasolina ISR - Laranja - 2018",
        "cavalos": "700 CV",
        "cilindros": "V12",
    },
    "nissan": {
        "nome": "Nissan Skyline GT-R R34",
        "imagem": "/img/nissan.jpg",
        "preco": "R$ 1.200.000",
        "ano": "2020",
        "descricao": "Nissan Skyline GT-R V-Spec II 2.6 L6 Biturbo Manual - Azul - 2002",
        "cavalos": "280 CV",
        "cilindros": "L6",
    },
    "chevrolet": {
        "nome": "Chevrolet Corvette C8",
        "imagem": "/img/chevrolet.jpg",
        "preco": "R$ 1.300.000",
        "ano": "2020",
        "descricao": "Chevrolet Corvette Stingray 6.2 V8 Gasolina Dual-Clutch - Amarelo - 2023",
        "cavalos": "495 CV",
        "cilindros": "V8",
    }
}

#definindo o endereço IP do host
SERVER_HOST = ""
#definindo o número da porta em que o servidor irá escutar pelas requisições HTTP
SERVER_PORT = 8080

#criando socket
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



def get(headers, client_connection):
    # print("\nHeaders\n\n\n", headers)
    filename = headers[1]

    if filename == "/":
        filename = "/index.html"

    print("\nFilename = ", filename, "\n")

    #try e except para tratamento de erro quando um arquivo solicitado não existir
    try:
        # print("htdocs" + filename)

        if 'veiculos.html?' in filename:
            car_name = filename.split("=")[1]
            if car_name in banco_de_carros:
                car_data = banco_de_carros[car_name]

                fin = open("htdocs/veiculo.html", "r")
                #leio o conteúdo do arquivo para uma variável
                content = fin.read()
                content = content.replace("{{NOME}}", car_data["nome"])
                content = content.replace("{{IMAGEM}}", car_data["imagem"])
                content = content.replace("{{PRECO}}", car_data["preco"])
                content = content.replace("{{ANO}}", car_data["ano"])
                content = content.replace("{{CILINDROS}}", car_data["cilindros"])
                content = content.replace("{{CAVALOS}}", car_data["cavalos"])
                content = content.replace("{{DESCRICAO}}", car_data["descricao"])

                fin.close()
                response = "HTTP/1.1 200 OK\n\n" + content
                client_connection.sendall(response.encode('utf-8'))
            else:
                response = "HTTP/1.1 404 NOT FOUND\r\n\r\n<h1>ERROR 404!<br>Veículo não encontrado.</h1>"
                client_connection.sendall(response.encode('utf-8'))
        else:
            #Tratamento de imagens
            if filename.endswith(".jpg") or filename.endswith(".png"):
                fin = open("htdocs" + filename, "rb")
                content_bytes = fin.read()
                fin.close()
                
                header = "HTTP/1.1 200 OK\r\n\r\n"
                client_connection.sendall(header.encode('utf-8') + content_bytes)

            #Tratamento de paginas padrão
            else:
                fin = open("htdocs" + filename)
                content = fin.read()
                fin.close()
                response = "HTTP/1.1 200 OK\n\n" + content
                client_connection.sendall(response.encode())
    except FileNotFoundError:
        #caso o arquivo solicitado não exista no servidor, gera uma resposta de erro
        response = "HTTP/1.1 404 NOT FOUND\n\n<h1>ERROR 404!<br>File Not Found!</h1>"
        client_connection.sendall(response.encode('utf-8'))
    

    
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
        headers = request.split()
        method = headers[0]
        if method == 'GET':
            get(headers, client_connection)
        # elif method == 'POST':
        #     try:
        #         dados = headers[0].split()[1]
        #         print(dados)
        #     except FileNotFoundError:
        #         response = "HTTP/1.1 404 NOT FOUND\n\n<h1>ERROR 404!<br>File Not Found!</h1>"
        
        client_connection.close()

server_socket.close()



# EXEMPLO DE REQUEST DO NAVEGADOR

# ['GET / HTTP/1.1\r', 'Host: localhost:8080\r', 'Connection: keep-alive\r', 'Cache-Control: max-age=0\r',
#   'sec-ch-ua: "Google Chrome";v="143", "Chromium";v="143", "Not A(Brand";v="24"\r', 'sec-ch-ua-mobile: ?0\r', 
#   'sec-ch-ua-platform: "Linux"\r', 'Upgrade-Insecure-Requests: 1\r', 
#   'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36\r', 
#   'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7\r',
#   'Sec-Fetch-Site: none\r', 'Sec-Fetch-Mode: navigate\r', 'Sec-Fetch-User: ?1\r', 'Sec-Fetch-Dest: document\r',
#   'Accept-Encoding: gzip, deflate, br, zstd\r',
#     'Accept-Language: pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7\r', '\r', '']