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
        "ano": "1995",
        "descricao": "Fiat Uno Mille Way Economy 1.0 Fire Flex Manual - Branco - 2013",
        "cavalos": "2000 CV",
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
    filename = headers[1]

    if filename == "/":
        filename = "/index.html"

    print("\nFilename = ", filename, "\n")

    #try e except para tratamento de erro quando um arquivo solicitado não existir
    try:
        print("htdocs" + filename)
        if filename == "/index.html":
            car_html = ""

            for car, details in banco_de_carros.items():
                car_html += f"""
                    <li class="car-card">
                        <div class="car-image">
                            <img src="{details["imagem"]}" alt="{details["nome"]}">
                        </div>
                
                        <div class="car-content">
                            <div class="car-header">
                                <p class="car-model">{details["nome"]}</p>
                            </div>
                
                            <p class="car-description">
                                {details["descricao"]}
                            </p>
                
                            <div class="car-details">
                                <p class="detail-item">
                                    {details["ano"]}
                                </p>
                                <p class="detail-item">
                                    {details["cavalos"]}
                                </p>
                                <p class="detail-item">
                                    {details["cilindros"]}
                                </p>
                            </div>
                        </div>
                
                        <div class="car-footer">
                            <div class="car-price">
                                <p class="currency">R$</p>
                                <p class="value">{details["preco"]}</p>
                            </div>
                            <a href="./veiculo.html?carro={car}" class="btn-ver-mais" style="text-decoration:none; text-align:center;">Ver mais</a>
                        </div>
                    </li>
                """
            fin = open("htdocs/index.html", "r")
            content = fin.read()
            fin.close()

            content = content.replace("{{LISTA_DE_CARROS}}", car_html)
            response = "HTTP/1.1 200 OK\r\n\r\n" + content
            client_connection.sendall(response.encode('utf-8'))
        elif 'veiculo.html?' in filename:
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
            
            #tratamento de imagem
        elif filename.endswith(".jpg") or filename.endswith(".png"):
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
    
def post(request, client_connection):
    # request = 'POST /login HTTP/1.1\r\nHost: localhost:8080\r\nConnection: keep-alive\r\nContent-Length: 36\r\nContent-Type: application/x-www-form-urlencoded\r\nUser-Agent: Mozilla/5.0...\r\nAccept: text/html...\r\n\r\nemail=admin%40mastercar.com&senha=1234'c
    partes = request.split("\r\n\r\n", 1)

    print(partes[1])
    if len(partes) > 0 and len(partes[1]) > 1:

        try:
            usuario = partes[1].split("&")[0].split("=")[1]
            senha = partes[1].split("&")[1].split("=")[1]
            if usuario == "admin" and senha == "admin":
                print("Login APROVADO. Redirecionando...")
                response = "HTTP/1.1 302 Found\r\nLocation: /administracao.html\r\n\r\n"
                client_connection.sendall(response.encode('utf-8'))
            else:
                html_erro = """
                <!DOCTYPE html>
                <html lang='pt-br'>
                <head><meta charset='UTF-8'><title>Erro de Login - MasterCar</title></head>
                <body style='font-family: Arial; text-align: center; padding: 50px; background-color: #f4f4f4;'>
                    <div style='background: white; padding: 40px; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); display: inline-block;'>
                        <h1 style='color: #d9534f; margin-top: 0;'>Acesso Negado</h1>
                        <p style='font-size: 18px; color: #333;'>Usuário ou senha incorretos.</p>
                        <br>
                        <a href='/login.html' style='background: #555; color: white; padding: 12px 24px; text-decoration: none; border-radius: 4px; font-weight: bold;'>Tentar Novamente</a>
                    </div>
                </body>
                </html>
                """
                response = "HTTP/1.1 401 Unauthorized\r\nContent-Type: text/html; charset=utf-8\r\n\r\n" + html_erro
                client_connection.sendall(response.encode('utf-8'))
        except Exception as e:
            erro_500 = "HTTP/1.1 500 Internal Server Error\r\n\r\n<h1>Erro ao processar o forms</h1>"
            client_connection.sendall(erro_500.encode('utf-8'))
    else:
        print("Post recebido nao contem usuario e senha")

    
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
        elif method == 'POST':
            post(request, client_connection)    
        
        client_connection.close()

server_socket.close()
