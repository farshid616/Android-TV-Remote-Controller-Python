from pynput import keyboard
from pairing import PairingSocket
import sys

def on_release(key):
    # print(key.char)
    if key.char == 'q' or key == keyboard.Key.esc:
        # Stop listener
        return False

if __name__ == "__main__":
    # if argument for pairing exist, start to pair
    if len(sys.argv) > 1 and sys.argv[1] == "pairing":
        pairing_sock = PairingSocket("hmi", '192.168.0.144')
        pairing_sock.connect()
        pairing_sock.start_pairing()
        assert (pairing_sock.connected),"Connection unsuccessful!"
    # Receive input keys
    with keyboard.Listener(on_release=on_release) as listener:
        listener.join()
