def upload(request, client_connection, filename):

  #pega o conetúdo do body da mensagem
  content = request.split("\r\n\r\n", 1)[1]
  print("REQUEST", request, "\n\n\n\n\n\n")
  print("NOME DO ARQUIVO", filename, "\n\n\n\n\n\n")


  #try e except para caso o arquivo exista
  try:
    #abrir o arquivo, caso ele exista
    fin = open("htdocs" + filename, "r")
    #reescreve dentro do arquivo
    fin = open("htdocs" + filename, "w")
    fin.write(content)
    #fecho o arquivo
    fin.close()
    #envia a resposta
    response = "HTTP/1.1 200 OK\n\n" + content
  except FileNotFoundError:
    #caso o arquivo não exista, cria um e escreve o conteúdo
    fin = open("htdocs" + filename, "w")
    fin.write(content)
    #fecha o arquivo
    fin.close
    #envia a resposta
    response = "HTTP/1.1 201 CREATED\n\n" + content
  #envia a resposta HTTP
  client_connection.sendall(response.encode())

def put(request, client_connection):
  #analisa a solicitação HTTP
  headers = request.split("\n")
  #pega o nome do arquivo sendo solicitado
  filename = headers[0].split()[1]
  #pega o conetúdo do body da mensagem
  content = request.split("\n\n", 1)[1]
  #try e except para caso o arquivo exista
  try:
    #abrir o arquivo, caso ele exista
    fin = open("htdocs" + filename, "r")
    #reescreve dentro do arquivo
    fin = open("htdocs" + filename, "w")
    fin.write(content)
    #fecho o arquivo
    fin.close()
    #envia a resposta
    response = "HTTP/1.1 200 OK\n\n" + content
  except FileNotFoundError:
    #caso o arquivo não exista, cria um e escreve o conteúdo
    fin = open("htdocs" + filename, "w")
    fin.write(content)
    #fecha o arquivo
    fin.close
    #envia a resposta
    response = "HTTP/1.1 201 CREATED\n\n" + content
  #envia a resposta HTTP
  client_connection.sendall(response.encode())