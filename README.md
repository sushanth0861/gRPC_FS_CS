This project demonstrates Remote Procedure Call (RPC) using gRPC for file synchronization and computation services between a client and server.

## Client

The client folder contains the following components:

- **computation_client.py**: Client code for computation services.
- **file_client.py**: Client code for file synchronization services.
- **requirements_client.txt**: List of dependencies required for the client.
- **services.proto**: Protobuf definition for gRPC services.
- **sync_folder/**: Directory being synchronized with the server.

For client setup and installation instructions, refer to the [Client README](./Client/README.md).

## Server

The server folder contains the following components:

- **computationserver.py**: Server code for computation services.
- **fileserver.py**: Server code for file services.
- **requirements_server.txt**: List of dependencies required for the server.
- **services.proto**: Protobuf definition for gRPC services.
- **server_files/**: Directory being synchronized with the clients.

For server setup and installation instructions, refer to the [Server README](./Server/README.md).