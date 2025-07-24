#!/usr/bin/env python3
import socket
import ssl
import os

# Define server address and port
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 9001

# SSL/TLS Configuration
SSL_CERTFILE = os.path.join('ssl_certs', 'server.crt')
BUFFER_SIZE = 4096
CHUNK_SIZE = 1024  # Size of each file chunk

class Client:
    def __init__(self):
        self.username = None
        self.password = None
        
        # Create basic socket
        base_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Create SSL context
        context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        # If using a self-signed certificate, disable hostname checking
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        
        # Wrap the socket with SSL
        self.client_socket = context.wrap_socket(base_socket, server_hostname=SERVER_HOST)

    def connect_to_server(self):
        try:
            self.client_socket.connect((SERVER_HOST, SERVER_PORT))
            print("Securely connected to the server.")
            return True
        except socket.error as e:
            print(f"Error connecting to server: {e}")
            return False

    def receive_message(self):
        try:
            return self.client_socket.recv(BUFFER_SIZE).decode()
        except Exception as e:
            print(f"Error receiving message: {e}")
            return None

    def send_message(self, message):
        try:
            self.client_socket.send(message.encode())
        except Exception as e:
            print(f"Error sending message: {e}")

    def authenticate(self):
        try:
            prompt = self.receive_message()
            print(prompt, end='')
            self.username = input()
            self.send_message(self.username)

            prompt = self.receive_message()
            print(prompt, end='')
            self.password = input()
            self.send_message(self.password)

            response = self.receive_message()
            print(response)
            return "Authentication Successful" in response

        except Exception as e:
            print(f"Authentication error: {e}")
            return False

    def upload_file(self, filename):
        try:
            if not os.path.exists(filename):
                print(f"Error: File '{filename}' not found.")
                return

            with open(filename, 'rb') as file:
                while True:
                    chunk = file.read(CHUNK_SIZE)
                    if not chunk:
                        self.client_socket.send(b"EOF")
                        break

                    self.client_socket.send(chunk)

                    response = self.receive_message()
                    if response != "ACK":
                        print(f"Error uploading chunk: {response}")
                        file.seek(-len(chunk), 1)
                        continue

            response = self.receive_message()
            print(response)
        except Exception as e:
            print(f"Upload error: {e}")

    def download_file(self, filename):
        try:
            # Hardcode the download path to the Downloads directory
            download_dir = os.path.join(os.path.expanduser("~"), "Downloads")
            os.makedirs(download_dir, exist_ok=True)  # Ensure the directory exists
            
            save_path = os.path.join(download_dir, filename)
            with open(save_path, 'wb') as file:
                while True:
                    chunk = self.client_socket.recv(CHUNK_SIZE)
                    if chunk == b"EOF" or not chunk:
                        break
                    if b"File not found" in chunk:
                        print("File not found on server")
                        return
                    file.write(chunk)

            print(f"File '{filename}' downloaded successfully to {save_path}.")
        except Exception as e:
            print(f"Download error: {e}")

    def view_file(self, filename):
        try:
            preview = self.receive_message()
            if preview:
                print("\nFile Preview:")
                print("-" * 50)
                print(preview)
                print("-" * 50)
        except Exception as e:
            print(f"Error viewing file: {e}")

    def delete_file(self, filename):
        try:
            response = self.receive_message()
            print(response)
        except Exception as e:
            print(f"Error deleting file: {e}")

    def list_files(self):
        try:
            file_list = self.receive_message()
            if file_list:
                print("\nFiles in your directory:")
                print("-" * 50)
                print(file_list)
                print("-" * 50)
        except Exception as e:
            print(f"Error listing files: {e}")

    def display_menu(self):
        print("\nSelect an action:")
        print("1) Upload File")
        print("2) Download File")
        print("3) View File")
        print("4) Delete File")
        print("5) List Files")
        print("6) Exit")

    def handle_server_interaction(self):
        while True:
            self.display_menu()
            try:
                option = input("Choose an option: ")

                commands = {
                    "1": "upload",
                    "2": "download",
                    "3": "view",
                    "4": "delete",
                    "5": "list",
                    "6": "quit"
                }

                if option in commands:
                    command = commands[option]
                    self.send_message(command)

                    if command == "quit":
                        print("Exiting...")
                        break

                    if command in ["upload", "download", "view", "delete"]:
                        filename = input("Enter filename: ")
                        self.send_message(filename)

                        if command == "upload":
                            self.upload_file(filename)
                        elif command == "download":
                            self.download_file(filename)
                        elif command == "view":
                            self.view_file(filename)
                        else:  # delete
                            self.delete_file(filename)
                    elif command == "list":
                        self.list_files()
                else:
                    print("Invalid option. Please try again.")
            except Exception as e:
                print(f"Error in server interaction: {e}")
                break

    def close(self):
        try:
            self.client_socket.close()
            print("\nConnection closed.")
        except Exception as e:
            print(f"Error closing connection: {e}")

def main():
    client = Client()

    if not client.connect_to_server():
        return

    try:
        if client.authenticate():
            client.handle_server_interaction()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    main()
