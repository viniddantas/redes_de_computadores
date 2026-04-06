import socket
import os
import json

ARQUIVO_BANCO = "banco_de_carros.json"

def carregar_banco():
    if os.path.exists(ARQUIVO_BANCO):
        fin = open(ARQUIVO_BANCO, "r", encoding="utf-8")
        data = json.load(fin)
        fin.close()
        return data
    else:
        return {}

def salvar_banco(dados):
    fin = open(ARQUIVO_BANCO, "w", encoding="utf-8")
    data = json.dump(dados, fin, indent=4, ensure_ascii=False)
    fin.close()

banco_de_carros = carregar_banco()

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
    try:
        if filename == "/index.html":
            
            print("\n=====Gerando index.html=====\n")
            car_html = ""

            #Gerando o card de cada carro na página inicial
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
            #Gera uma página modelo para cada veículo
            
            print("\n=====Gerando veiculo.html=====\n")
            car_name = filename.split("=")[1]
            if car_name in banco_de_carros:
                car_data = banco_de_carros[car_name]

                fin = open("htdocs/veiculo.html", "r")

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
        elif 'administracao.html' in filename:
            print("\n=====Gerando administracao.html=====\n")
            html_admin_car = ""

            for car, details in banco_de_carros.items():
                html_admin_car += f"""
                <div class="item-carro">
                    <span class="nome-carro-admin">{details['nome']}</span>
                    <button class="btn-deletar" onclick="deletarCarro('{car}')">Excluir</button>
                </div>
                """
            fin = open("htdocs/administracao.html", "r")

            content = fin.read()
            content = content.replace("{{LISTA_DE_CARROS_ADMIN}}", html_admin_car)
            fin.close()
            
            response = "HTTP/1.1 200 OK\n\n" + content
            client_connection.sendall(response.encode('utf-8'))

        #tratamento de imagem
        elif filename.endswith(".jpg") or filename.endswith(".png"):
            fin = open("htdocs" + filename, "rb")
            content_bytes = fin.read()
            fin.close() 
            header = "HTTP/1.1 200 OK\r\n\r\n"
            client_connection.sendall(header.encode('utf-8') + content_bytes)

        #Tratamento de paginas genericas
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
    except Exception as e:
        print(f"Erro ao processar GET: {e}")
        response = "HTTP/1.1 500 Internal Server Error\r\n\r\n<h1>500 Internal Server Error</h1>"
        client_connection.sendall(response.encode('utf-8'))
        
def post(request, client_connection):
    try:
        parts = request.split("\r\n\r\n", 1)
        header = parts[0]

        if len(parts) > 1:
            body = parts[1]
        else: 
            print("======== Erro inesperado (body está vazio) ==========")

        request_type = header.split("\r\n")[0].split()[1]

        filename = request_type

        if "." in filename:
            filename = request_type.replace("/", "")
        else:
            filename = request_type.replace("/", "") + ".txt"

        print("FILENAME", filename)

        fin = open(filename, "a", encoding="utf-8")
        fin.write(body + "\n")
        fin.close()

        # with open(filename, "a", encoding="utf-8") as f:
        #     f.write(body + "\n")
        
        if 'login' in request_type:
            if len(parts) > 0 and len(body) > 1:
                usuario = body.split("&")[0].split("=")[1]
                senha = body.split("&")[1].split("=")[1]
                print("Usuario: ", usuario)
                print("Senha: ", senha)
                if usuario == "admin" and senha == "admin":
                    print("\n=====Login APROVADO. Redirecionando...=====\n")
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
            else:
                print("Post recebido nao contem usuario e senha")
        elif 'adicionar-veiculo' in request_type:
            print("ADICIONANDO VEICULO")
            dados = {}
            for par in body.split("&"):
                key, value = par.split("=", 1)
                
                formated_value = value.replace("+", " ").replace("%2F", "/").replace("%3A", ":").replace("%24","$")

                dados[key] = formated_value

            new_key = dados['chave']

            banco_de_carros[new_key] = {
                "nome": dados['nome'],
                "imagem": dados['imagem'],
                "preco": dados['preco'],
                "ano": dados['ano'],
                "cavalos": dados['cavalos'],
                "cilindros": dados['cilindros'],
                "descricao": dados['descricao']
            }

            salvar_banco(banco_de_carros)
            
            print(f"Sucesso! O carro {new_key} foi adicionado no banco.")

            response = "HTTP/1.1 302 Found\r\nLocation: /administracao.html\r\n\r\n"
            client_connection.sendall(response.encode('utf-8'))
        elif 'contato' in request_type:
            print("\n--- FORMULÁRIO DE CONTATO RECEBIDO ---")
            
            if body:
                print(f"Mensagem bruta recebida: {body}")

            response = "HTTP/1.1 302 Found\r\nLocation: /\r\n\r\n"
            client_connection.sendall(response.encode('utf-8'))
    except Exception as e:
        print(f"Erro crítico no POST: {e}") # Adicione isto
        response = "HTTP/1.1 500 Internal Server Error\r\n\r\n<h1>Erro ao processar o forms</h1>"
        client_connection.sendall(response.encode('utf-8'))

def delete(request, client_connection):
    try:
        #obtem o nome do carro
        car_name = request.split()[1].split("=")[1]

        #verifica se o carro está contido na base de dados 
        if car_name in banco_de_carros:
            print(f"Apagando {car_name} da base de dados")
            del banco_de_carros[car_name]
            salvar_banco(banco_de_carros)
            response = "HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\nRemovido com sucesso!"
            client_connection.sendall(response.encode('utf-8'))
        else:
            response = "HTTP/1.1 400 Bad Request\r\n\r\nRota invalida."
            client_connection.sendall(response.encode('utf-8'))
        print("\n", response, sep="")
    except Exception as e:
        print(f"Erro ao processar DELETE: {e}")
        erro_500 = "HTTP/1.1 500 Internal Server Error\r\n\r\nErro interno no servidor."
        client_connection.sendall(erro_500.encode('utf-8'))

def request_receive(client_connection):
    request = b""
    try:
        #Ler o cabeçalho (b"\r\n\r\n" significa o fim do cabeçalho)
        while b"\r\n\r\n" not in request:
            request_part = client_connection.recv(1024)
            if not request_part:
                break
            request += request_part

        #Verificação de seguraça caso o cliente feche a conexão
        if not request or b"\r\n\r\n" not in request:
            return ""

        parts = request.split(b"\r\n\r\n", 1)
        header = parts[0]

        if len(parts) > 1:
            body = parts[1]
        else: 
            body = b""

        #Conversão do header para string
        header_str = header.decode('utf-8', errors='ignore')

        #Loop para obter o conteng-length
        body_lenght = 0
        for linha in header_str.split("\r\n"):
            if linha.lower().startswith("content-length:"):
                try:
                    body_lenght = int(linha.split(":")[1].strip())
                except ValueError:
                    body_lenght = 0
                break

        #Loop para obter o body sabendo o valor do conteng-length
        while len(body) < body_lenght:
            request_part = client_connection.recv(1024)
            if not request_part:
                break
            body += request_part

        #Retorno
        complete_request = header + b"\r\n\r\n" + body
        return complete_request.decode('utf-8', errors='ignore')
    except Exception as e:
        print(f"Erro ao processar request: {e}")
        response = "HTTP/1.1 500 Internal Server Error\r\n\r\n<h1>500 Internal Server Error</h1>"
        client_connection.sendall(response.encode('utf-8'))
        

#cria o while que irá receber as conexões
while True:
    #client_connection: o socket que será criado para trocar dados com o cliente de forma dedicada
    #client_address: tupla (IP do cliente, Porta do cliente)
    client_connection, client_address = server_socket.accept()

    #pega a solicitação do cliente
    request = request_receive(client_connection)
    
    #verifica se a request possui algum conteúdo (pois alguns navegadores ficam periodicamente enviando alguma string vazia)
    if request:
        # print(request.split("\r\n")[0], sep="")
        headers = request.split()
        method = request.split()[0]
        # print("Headers", headers)
        # print(headers[0].split()[1])
        if method == 'GET':
            get(headers, client_connection)
        elif method == 'POST' and headers[1] == "/Upload.html":
            start = request.find('filename="') + len('filename="')
            end = request.find('"', start)

            print("\nStart/n", start)
            print("\nEndn", end)
            
            upload(request, client_connection, request[start:end])
        elif method == 'POST':
            post(request, client_connection)
        elif method == "DELETE":
            delete(request, client_connection)
        
        client_connection.close()

server_socket.close()
