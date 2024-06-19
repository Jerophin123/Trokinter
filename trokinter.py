import os
import subprocess
import sys
import threading
import time
import random
import tkinter as tk

def check_root():
    if os.geteuid() != 0:
        print("This script must be run as root.")
        sys.exit(1)

def install_tkinter():
    try:
        # Check if Tkinter is installed by importing it
        import tkinter
    except ImportError:
        print("Tkinter is not installed. Installing Tkinter...")
        try:
            # For Debian-based systems (e.g., Ubuntu)
            subprocess.check_call([sys.executable, "-m", "pip", "install", "tk"])
            print("Tkinter installed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Failed to install Tkinter: {e}")
            sys.exit(1)

def create_window(x, y):
    root = tk.Tk()
    root.title("Message Window")
    root.geometry(f"300x200+{x}+{y}")
    message = tk.Label(root, text="You System is being FUCKED UP")
    message.pack(pady=50)
    root.mainloop()

def execute_command():
    # Replace this command with any Linux command you want to execute
    command = "neofetch"
    subprocess.run(command, shell=True)

def create_windows_in_loop(limit=100, total_limit=500, delay=0.1):
    screen_width = 1920  # Assuming screen width
    screen_height = 1080  # Assuming screen height
    count = 0
    total_count = 0
    while True:
        try:
            x = random.randint(0, screen_width - 300)  # Random x position
            y = random.randint(0, screen_height - 200)  # Random y position
            threading.Thread(target=create_window, args=(x, y)).start()
            count += 1
            total_count += 1
            if count == limit:
                execute_command()
                count = 0
            if total_count == total_limit:
                break
            time.sleep(delay)
        except KeyboardInterrupt:
            print("Script interrupted by user.")
            break
        except Exception as e:
            print(f"An error occurred: {e}")
            break

if __name__ == "__main__":
    check_root()  # Ensure the script is run as root
    install_tkinter()  # Check and install Tkinter if necessary
    create_windows_in_loop(limit=100, total_limit=500, delay=0.1)  # Adjust the delay and total_limit as needed
