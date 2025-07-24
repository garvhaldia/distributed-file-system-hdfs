#!/usr/bin/env python3
import socket
import ssl
import threading
import os
import signal
import sys

# Define the server IP and port
SERVER_IP = '127.0.0.1'
SERVER_PORT = 9001

# SSL/TLS Configuration
SSL_CERTFILE = os.path.join('ssl_certs', 'server.crt')
SSL_KEYFILE = os.path.join('ssl_certs', 'server.key')

# Authentication file
AUTH_FILE = "id_passwd.txt"
# Use a directory in the current working directory instead of root
STORAGE_ROOT = os.path.join(os.getcwd(), "server_storage")

CHUNK_SIZE = 1024  # Size of each file chunk
PREVIEW_SIZE = 1024  # Size of file preview in bytes

def authenticate(username, password):
    try:
        with open(AUTH_FILE, "r") as file:
            for line in file:
                file_username, file_password = line.strip().split(':')
                if username == file_username and password == file_password:
                    return True
        return False
    except FileNotFoundError:
        print(f"Error: Authentication file '{AUTH_FILE}' not found.")
        return False
    except Exception as e:
        print(f"Authentication error: {e}")
        return False

def signal_handler(sig, frame):
    print("\nShutting down the server gracefully...")
    server_socket.close()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def send_message(conn, message):
    try:
        conn.send(message.encode())
    except Exception as e:
        print(f"Error sending message: {e}")

def receive_message(conn):
    try:
        return conn.recv(4096).decode().strip()
    except Exception as e:
        print(f"Error receiving message: {e}")
        return None

def get_user_directory(username):
    os.makedirs(STORAGE_ROOT, exist_ok=True)
    user_dir = os.path.join(STORAGE_ROOT, username[0], username)
    os.makedirs(user_dir, exist_ok=True)
    os.chmod(user_dir, 0o700)
    return user_dir

def upload_file(username, filename, conn):
    try:
        user_dir = get_user_directory(username)
        file_path = os.path.join(user_dir, filename)

        with open(file_path, "wb") as file:
            while True:
                data = conn.recv(CHUNK_SIZE)
                if data == b"EOF":
                    break
                file.write(data)
                send_message(conn, "ACK")
        
        os.chmod(file_path, 0o600)
        send_message(conn, f"File '{filename}' uploaded successfully.")
    except Exception as e:
        send_message(conn, f"Error uploading file: {str(e)}")

def download_file(username, filename, conn):
    try:
        user_dir = get_user_directory(username)
        file_path = os.path.join(user_dir, filename)

        if os.path.exists(file_path):
            with open(file_path, 'rb') as file:
                while chunk := file.read(CHUNK_SIZE):
                    conn.send(chunk)
            conn.send(b"EOF")  # Ensure EOF is sent after the file is sent
        else:
            send_message(conn, "File not found")
    except Exception as e:
        send_message(conn, f"Error downloading file: {str(e)}")

def view_file(username, filename, conn):
    try:
        user_dir = get_user_directory(username)
        file_path = os.path.join(user_dir, filename)

        if os.path.exists(file_path):
            with open(file_path, 'rb') as file:
                preview_data = file.read(PREVIEW_SIZE)
                try:
                    preview_text = preview_data.decode('utf-8')
                except UnicodeDecodeError:
                    preview_text = "[Binary file preview]\n" + \
                                   ' '.join(f'{byte:02x}' for byte in preview_data[:100]) + \
                                   "\n[Preview truncated...]"
                
                file_size = os.path.getsize(file_path)
                preview_text = f"File size: {file_size} bytes\nPreview of first {PREVIEW_SIZE} bytes:\n\n{preview_text}"
                send_message(conn, preview_text)
        else:
            send_message(conn, "File not found")
    except Exception as e:
        send_message(conn, f"Error viewing file: {str(e)}")

def delete_file(username, filename, conn):
    try:
        user_dir = get_user_directory(username)
        file_path = os.path.join(user_dir, filename)

        if os.path.exists(file_path):
            os.remove(file_path)
            send_message(conn, f"File '{filename}' deleted successfully.")
        else:
            send_message(conn, "File not found")
    except Exception as e:
        send_message(conn, f"Error deleting file: {str(e)}")

def list_files(username, conn):
    try:
        user_dir = get_user_directory(username)
        if os.path.exists(user_dir):
            files = os.listdir(user_dir)
            send_message(conn, '\n'.join(files) if files else "No files found")
        else:
            send_message(conn, "No files found")
    except Exception as e:
        send_message(conn, f"Error listing files: {str(e)}")

def client_handler(conn):
    try:
        send_message(conn, "Username: ")
        username = receive_message(conn)
        
        send_message(conn, "Password: ")
        password = receive_message(conn)
        
        print(f"Attempting authentication for user: {username}")
        
        if not authenticate(username, password):
            print(f"Authentication failed for user: {username}")
            send_message(conn, "Authentication Failed")
            return

        print(f"Authentication successful for user: {username}")
        send_message(conn, "Authentication Successful\n")

        while True:
            try:
                action = receive_message(conn)
                
                if not action:
                    break

                print(f"User {username} requested action: {action}")

                if action == "upload":
                    filename = receive_message(conn)
                    upload_file(username, filename, conn)

                elif action == "download":
                    filename = receive_message(conn)
                    download_file(username, filename, conn)

                elif action == "view":
                    filename = receive_message(conn)
                    view_file(username, filename, conn)

                elif action == "delete":
                    filename = receive_message(conn)
                    delete_file(username, filename, conn)

                elif action == "list":
                    list_files(username, conn)

                elif action == "quit":
                    print(f"User {username} disconnected")
                    break

                else:
                    send_message(conn, "Invalid action")

            except Exception as e:
                print(f"Error handling request for {username}: {e}")
                send_message(conn, f"Error: {str(e)}")

    except Exception as e:
        print(f"Error handling client: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    try:
        os.makedirs(STORAGE_ROOT, exist_ok=True)
        os.chmod(STORAGE_ROOT, 0o755)

        # Create SSL context
        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        context.load_cert_chain(certfile=SSL_CERTFILE, keyfile=SSL_KEYFILE)

        # Create server socket
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((SERVER_IP, SERVER_PORT))
        server_socket.listen(5)

        # Wrap the server socket with SSL
        secure_server_socket = context.wrap_socket(server_socket, server_side=True)

        print(f"Secure server listening on {SERVER_IP}:{SERVER_PORT}")
        print(f"Authentication file: {AUTH_FILE}")
        print(f"Storage root: {STORAGE_ROOT}")
        print(f"SSL Certificate: {SSL_CERTFILE}")

        while True:
            client_conn, client_addr = secure_server_socket.accept()
            print(f"New secure connection from {client_addr}")
            threading.Thread(target=client_handler, args=(client_conn,)).start()

    except Exception as e:
        print(f"Server error: {e}")
    finally:
        server_socket.close()
