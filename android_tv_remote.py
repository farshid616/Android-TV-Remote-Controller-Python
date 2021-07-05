from pynput import keyboard
from pairing import PairingSocket
from sending_keys import SendingKeySocket
from key_codes import *
import sys


# Set your server name, server ip and client name here
SERVER_IP = '192.168.0.144'
SERVER_NAME = "Mi Box"
CLIENT_NAME = "hmi"

def print_guide():
    print('''
    You can controll you device with this keys:
                w = up                      u = volume up

    a = left    o = ok      d = right       j = volume down

                s = down

    b = back    h = home    n = netflix     q = exit
    ''')

def on_release(key):
    print_guide()
    if key.char == 'q' or key == keyboard.Key.esc:
        # Stop listener
        sending_key_socket.disconnect()
        return False
    elif key.char == 'h' :
        sending_key_socket.send_key_command(KEYCODE_HOME)
    elif key.char == 'b' :
        sending_key_socket.send_key_command(KEYCODE_BACK)
    elif key.char == 'w' :
        sending_key_socket.send_key_command(KEYCODE_DPAD_UP)
    elif key.char == 's' :
        sending_key_socket.send_key_command(KEYCODE_DPAD_DOWN)
    elif key.char == 'a' :
        sending_key_socket.send_key_command(KEYCODE_DPAD_LEFT)   
    elif key.char == 'd' :
        sending_key_socket.send_key_command(KEYCODE_DPAD_RIGHT)
    elif key.char == 'o' :
        sending_key_socket.send_key_command(KEYCODE_DPAD_CENTER)
    elif key.char == 'u' :
        sending_key_socket.send_key_command(KEYCODE_VOLUME_UP)
    elif key.char == 'j' :
        sending_key_socket.send_key_command(KEYCODE_VOLUME_DOWN)
    elif key.char == 'n' :
        sending_key_socket.send_lunch_app_command("netflix")


if __name__ == "__main__":
    # if argument for pairing exist, start to pair
    if len(sys.argv) > 1 and sys.argv[1] == "pairing":
        pairing_sock = PairingSocket(CLIENT_NAME, SERVER_IP)
        pairing_sock.connect()
        pairing_sock.start_pairing()
        assert (pairing_sock.connected),"Connection unsuccessful!"
    
    sending_key_socket = SendingKeySocket(SERVER_NAME, SERVER_IP)
    sending_key_socket.connect()
    print_guide()
    # Receive input keys
    with keyboard.Listener(on_release=on_release) as listener:
        listener.join()
