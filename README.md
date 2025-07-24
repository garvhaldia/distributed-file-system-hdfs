# Mini-HDFS: Simplified Distributed File System

###### A Python implementation of a simplified HDFS (Hadoop Distributed File System) that replicates core distributed storage concepts. Th### Limitations (Compared to Full HDFS)

###### \* Single-node deployment (no distributed DataNodes)

###### \* No replication factor implementation

###### \* Local network usage only (localhost)

###### \* Plain text password storage (consider implementing Kerberos-like auth)

###### \* Basic file preview functionality

###### \* No file compression or deduplication

###### \* Simplified block management (no block splitting/merging)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Author

**Garv Haldia** - [GitHub Profile](https://github.com/garvhaldia)r file system provides secure storage, retrieval, and management of files with features inspired by HDFS architecture including user authentication, hierarchical storage, SSL/TLS encryption, and chunk-based file operations.

### Features (HDFS-Inspired)

###### \* User authentication and access control

###### \* SSL/TLS encrypted communication (enhanced security over standard HDFS)

###### \* Hierarchical namespace similar to HDFS directory structure

###### \* Chunk-based file storage and transfer (block-level operations)

###### \* Secure file upload, download, and management operations

###### \* File preview functionality (metadata inspection)

###### \* Multi-threaded server supporting concurrent client connections

###### \* Distributed storage concepts with centralized metadata management

###### \* Self-signed SSL certificate for secure authentication

### Prerequisites

###### \* Python 3.x

###### \* Basic understanding of terminal/command line operations

### Installation

###### \* Clone or download the repository to your local machine

###### \* Ensure you have Python 3.x installed

###### \* Use authentication file named id_passwd.txt in the server directory

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

###### \* Password-based authentication

###### \* User-specific storage directories

###### \* Proper file permissions (700 for directories, 600 for files)

###### \* Secure file transfer using chunks

###### \* Input validation and error handling

#### The server creates a hierarchical storage structure similar to HDFS:

##### Storage Structure (HDFS-style)

```python

server_storage/
└── u/
    └── username/
        └── user_files  # Block storage area
```

### HDFS Concepts Implemented

#### This project replicates key HDFS concepts:

###### \* **Namespace Management**: Hierarchical file organization

###### \* **Block Storage**: Chunk-based file handling (1024-byte blocks)

###### \* **Client-Server Architecture**: Centralized metadata and storage management

###### \* **Concurrent Access**: Multi-threaded server for multiple clients

###### \* **Security**: Enhanced with SSL/TLS (beyond standard HDFS)

###### \* **File Operations**: Standard HDFS-like operations (put, get, ls, rm)

### Error Handling

#### The system includes comprehensive error handling for:

###### \* Connection issues

###### \* Authentication failures

###### \* File operation errors

###### \* Invalid commands

###### \* Network interruptions

### Technical Details (HDFS-Inspired)

##### Block/Chunk Sizes (Similar to HDFS blocks)

###### \* File transfer chunk size: 1024 bytes (simplified HDFS block)

###### \* File preview size: 1024 bytes (metadata inspection)

###### \* Buffer size: 4096 bytes

### Network Protocol

###### \* TCP/IP based communication (NameNode-DataNode style)

###### \* Text-based command protocol (HDFS client commands)

###### \* Binary file transfer support (block transfer)

### Limitations (Compared to Full HDFS)

###### \* Single-node deployment (no distributed DataNodes)

###### \* No replication factor implementation

###### \* Local network usage only (localhost)

###### \* Plain text password storage (consider implementing Kerberos-like auth)

###### \* Basic file preview functionality

###### \* No file compression or deduplication

###### \* Simplified block management (no block splitting/merging)
