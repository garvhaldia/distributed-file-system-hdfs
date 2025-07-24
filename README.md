# Secure File Storage System
###### A client-server based file storage system implemented in Python that allows users to securely store, retrieve, and manage their files. The system features user authentication, directory-based storage, SSL/TLS encryption, and supports various file operations.
### Features
###### * User authentication
###### * SSL/TLS encrypted communication
###### * Secure file upload and download
###### * File preview functionality
###### * File management operations (list, delete, view)
###### * Directory-based storage structure
###### * Chunk-based file transfer for handling large files
###### * Multi-threaded server supporting multiple concurrent connections
###### * Self-signed SSL certificate for secure authentication

### Prerequisites

###### * Python 3.x
###### * Basic understanding of terminal/command line operations

### Installation

###### * Clone or download the repository to your local machine
###### * Ensure you have Python 3.x installed
###### * Use authentication file named id_passwd.txt in the server directory

### Configuration
#### Server Configuration
##### The server uses the following default settings in server.py:
```python
SERVER_IP = '127.0.0.1'
SERVER_PORT = 9001
AUTH_FILE = "id_passwd.txt"
STORAGE_ROOT = os.path.join(os.getcwd(), "server_storage")
```
#### Client Configuration
##### The client uses the following default settings in client.py:
```python
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 9001
```
#### Authentication Setup
##### Create an id_passwd.txt file with the following format:
```python
username:password
```
##### Each line should contain one user credential pair, with username and password separated by a colon.
Example:
```python
user1:pass1
user2:pass2
```
### Usage
#### Starting the Server:

##### Open a terminal in the server directory
##### Run the server:
```python
 python3 server.py
```
##### The server will create a server_storage directory automatically if it doesn't exist.
#### Running the Client
##### Open a new terminal in the client directory
##### Run the client:
```python
 python3 client.py
```

#### After authentication, users can perform the following operations:

###### Upload File: Upload a file to the server
###### Download File: Download a file from the server
###### View File: Preview file contents till 1024 bytes
###### Delete File: Remove a file from the server
###### List Files: View all stored files
###### Exit: Close the connection

### Security Features

###### * Password-based authentication
###### * User-specific storage directories
###### * Proper file permissions (700 for directories, 600 for files)
###### * Secure file transfer using chunks
###### * Input validation and error handling
#### The server creates a hierarchical storage structure:
##### Storage Structure
```python

server_storage/
└── u/
    └── username/
        └── user_files
```
### Error Handling
#### The system includes comprehensive error handling for:
###### * Connection issues
###### * Authentication failures
###### * File operation errors
###### * Invalid commands
###### * Network interruptions

### Technical Details
##### Chunk Sizes

###### * File transfer chunk size: 1024 bytes
###### * File preview size: 1024 bytes
###### * Buffer size: 4096 bytes

### Network Protocol

###### * TCP/IP based communication
###### * Text-based command protocol
###### * Binary file transfer support

### Limitations

###### * Local network usage only (localhost)
###### * Plain text password storage (consider implementing encryption)
###### * Basic file preview functionality
###### * No file compression
