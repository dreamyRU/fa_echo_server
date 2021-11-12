import logging
from random import randint
import socket
from storage import Database


class Server:
    def __init__(self, database, host, port, logfile):
        logging.basicConfig(filename=logfile,  level=logging.INFO,
        format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %H:%M:%S')
        self.sock = socket.socket()
        while True:
            try:
                self.sock.bind((host, port))
                break
            except OSError:
                port = randint(2000, 8000)

        logging.info("Запуск сервера {}:{}".format(host, port))
        self.sock.listen(1)
        logging.info("Начало прослушивания порта {}".format(port))

        self.db = Database(database)
    
    def authentication(self):
        name = self.db.checkIP(self.addr)
        if name != None:
            logging.info("Aутентификация клиента {}".format(self.addr))
            self.conn.send("\n> Enter your password:".encode())
            for i in range(3):
                password = self.conn.recv(1024).decode()
                if self.db.login(name, password):
                    logging.info("Аутентификация клиента {} прошла успешно".format(self.addr))
                    self.conn.send("> Hello, {}".format(name).encode())
                    break
                elif i == 2:
                    logging.info("Исчерпан лимит попыток ввода пароля. Отключение клиента {}".format(self.addr))
                    self.conn.send("_error_".encode()) 
                    return False
                else:
                    self.conn.send(("> Incorrect password, you have {} more chances."
                    .format(2-i) + "\n> Enter your password:").encode())
        else:
            logging.info("Регистрация клиента {}".format(self.addr))
            self.conn.send("> Hello, enter your name:".encode())
            nameInput = self.conn.recv(1024).decode()

            self.conn.send("> Create your password:".encode())
            password = self.conn.recv(1024).decode()

            self.db.createUser(self.addr, nameInput, password)
            self.conn.send("> Welcome, {}".format(nameInput).encode())
            
        return True


    def connect(self):
        self.conn, self.addr = self.sock.accept()
        self.addr = "{}:{}".format(self.addr[0], self.addr[1])
        logging.info("Поключение клиента с адреса {}".format(self.addr))

        if not self.authentication():
            self.conn.close()
            return

        while True:
            data = self.conn.recv(1024).decode()
            logging.info("Прием данных от клиента {}: {}".format(self.addr, data))

            if data == "exit":
                logging.info("Отключение клиента {}".format(self.addr))
                self.conn.close()
                return
            
            logging.info("Отправка данных клиенту {}: {}".format(self.addr, data.upper()))
            try:
                self.conn.send(("> " + data.upper()).encode())
            except BrokenPipeError:
                logging.info("Разрыв соединения с клиентом {}".format(self.addr))
                self.conn.close()
                return
    

if __name__ == "__main__":
    server = Server(
        database='./storage.db', 
        host='localhost', 
        port=9080,
        logfile="./Logs/server.log")
    
    while True:
        server.connect()