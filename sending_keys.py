import socket, ssl
import OpenSSL
from OpenSSL.crypto import load_certificate
from OpenSSL.crypto import FILETYPE_PEM
from asn1crypto.x509 import Certificate


class SendingKeySocket:
    '''
    This class designed to send controlling commands to a android TV
    '''

    def __init__(self, server_name, host_address, port=6466, sock=None):
        if sock is None:
            self.sock = socket.socket(
                socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock
        self.host = host_address
        self.server_name = server_name
        self.port = port
        self.connected = False

    def connect(self):
        """
        This function will create a socket to given ip and port,
        with generated certificate and public key
        """
        self.ssl_sock = ssl.wrap_socket(self.sock,
                            keyfile="key.pem",
                            certfile="cert.pem",
                            do_handshake_on_connect=True)
        self.ssl_sock.connect((self.host, self.port))
    
    def disconnect(self):
        """
        This function will disconnect the socket
        """
        self.ssl_sock.close()

    # TODO: Implement parser function
    def parse_message(self, raw_message):
        """
        This function will receive raw message, decode the message.
        :param raw_message: raw received message
        :return: 
        """
        pass

    def send_message(self, msg):
        """
        This function will receive message bytes as a param and will send the message size,
        and the message body to server.
        :param msg: created message in bytes
        """
        self.ssl_sock.send(msg)

    def receive_message(self):
        """
        This function will receive messages from server and pass it to
        message parser function.
        """
        data = self.ssl_sock.recv(1024)
        self.parse_message(data)

    def create_configuration_mesaage(self, server_name):
        """
        This function will receive server name and create the configuration message.
        :param server_name: string of the server name
        :return: string of the created configuration message
        """
        # adding the size, 1, message type 0 and seperaor 0
        message = [1,0,0]
        # adding payload size
        message.append(17+len(server_name))
        # adding two 1 as a 4 byte, one 32, one 3 and six 0 
        message += [0,0,0,1,0,0,0,1,32,3,0,0,0,0,0,0]
        # adding size of the server name
        message.append(len(server_name))
        # adding server name characters as asci 
        for item in server_name:
            message.append(ord(item))
        return message
    
    def send_key_command(self, command_code):
        """
        This function will receive command code, create and send command message to server.
        :param server_name: integer of command code
        """
        self.send_message(bytes(self.create_configuration_mesaage(self.server_name)))
        # creating message
        message = [1,2,0,16,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        # adding key code to the mesage
        message.append(command_code)
        # sending key command with press flag
        self.send_message(bytes(message))
        # change counter to 1
        message[11] = 1
        # change press flag to release
        message[15] = 1
        # sending key command with release flag
        self.send_message(bytes(message))
 
    # TODO: complete launch app function.
    def send_lunch_app_command(self, app_name):
        """
        This function will receive android application name, create and send app launch command.
        :param app_name: string of the application package name
        """
        # currently just launch netflix
        self.send_message(bytes(self.create_configuration_mesaage(self.server_name)))
        # creating message
        message = [1,16,0]
        # adding key code to the mesage
        name = "intent:#Intent;component=com.netflix.ninja/.MainActivity;end"
        message.append(len(name))
        for item in name:
            message.append(ord(item))
        # sending key command with release flag
        self.send_message(bytes(message))
        