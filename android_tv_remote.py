from pynput import keyboard

def on_release(key):
    # print(key.char)
    if key.char == 'q' or key == keyboard.Key.esc:
        # Stop listener
        return False

if __name__ == "__main__":
    # # Collect events until released
    with keyboard.Listener(on_release=on_release) as listener:
        listener.join()
