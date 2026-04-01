def post():
    request = 'POST /login HTTP/1.1\r\nHost: localhost:8080\r\nConnection: keep-alive\r\nContent-Length: 36\r\nContent-Type: application/x-www-form-urlencoded\r\nUser-Agent: Mozilla/5.0...\r\nAccept: text/html...\r\n\r\nemail=admin%40mastercar.com&senha=1234'
    partes = request.split("\r\n\r\n")

    print(partes[1])

post()