import socket, ssl
from OpenSSL.crypto import load_certificate
from OpenSSL.crypto import FILETYPE_PEM
from asn1crypto.x509 import Certificate
import hashlib
from json_handler import *


class PairingSocket:
    '''
    This class designed to pair a client to a android TV
    '''

    def __init__(self, client_name, host_address, port=6467, sock=None):
        if sock is None:
            self.sock = socket.socket(
                socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock
        self.host = host_address
        self.client_name = client_name
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

    def start_pairing(self) :
        """
        This function will start the pairing process by sending a pairing req message,
        and starting to receive.
        """
        message = create_paring_request_message(self.client_name)
        self.send_message(message)
        self.receive_message()

    def parse_message(self, raw_message):
        """
        This function will receive raw message, decode the message,
        and create response message related to received message type.
        :param raw_message: raw received message
        :return: null at the end of the pairing or when some error occur
        """
        message = ""
        # ignore messages with less than 5 bytes (packet size messages)
        if len(raw_message) > 4 :
            message_status, message_type = parse_json_message(raw_message)
            if message_status == 200 :
                if message_type == 11:
                    # crating option message
                    message = create_option_message()

                elif message_type == 20:
                    # creating configuration message
                    message = create_configuration_mesaage()

                elif message_type == 31:
                    # Creating secret message: a sha-256 hash of client certificate modulus + client certificate exponent +
                    # server modulus + server exponent + two last digit of pairing key coded to base64
                    input_code = input("enter the code: ")
                    # bin_inp = chr(int(inp[-2:], 16))
                    with open("cert.pem", 'rb') as fp:
                        cert = load_certificate(FILETYPE_PEM, fp.read())
                    client_modulus = cert.get_pubkey().to_cryptography_key().public_numbers().n
                    client_exponent = cert.get_pubkey().to_cryptography_key().public_numbers().e
                    # all items in hex format
                    client_mod = '{:X}'.format(client_modulus)
                    client_exp = "010001"
                    server_cert = Certificate.load(self.ssl_sock.getpeercert(True))
                    server_mod = '{:X}'.format(server_cert.public_key.native["public_key"]["modulus"])
                    server_exp = "010001"
                    h = hashlib.sha256()
                    h.update(bytes.fromhex(client_mod))
                    h.update(bytes.fromhex(client_exp))
                    h.update(bytes.fromhex(server_mod))
                    h.update(bytes.fromhex(server_exp))
                    h.update(bytes.fromhex(input_code[-2:]))
                    hash_result = h.digest()
                    message = create_secret_message(hash_result)

                elif message_type == 41:
                    # Pairing finished successfully
                    self.connected = True
                    self.disconnect()
                    return
            else :
                self.disconnect()
                return
        else :
            self.receive_message()
            return

        self.send_message(message)
        self.receive_message()

    def send_message(self, msg):
        """
        This function will receive message and will send the message size,
        and the message body to server.
        :param message: created message
        """
        self.ssl_sock.send((len(msg)).to_bytes(4, byteorder='big'))
        self.ssl_sock.send(msg.encode())

    def receive_message(self):
        """
        This function will receive messages from server and pass it to
        message parser function.
        """
        data = self.ssl_sock.recv(1024)
        self.parse_message(data)