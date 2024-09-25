
# Server Setup

This guide will help you set up the server environment, install the necessary dependencies, and generate the required gRPC code from the `services.proto` file.

## Folder Structure

The project directory is organized as follows:
- **Server/**:
  - **computationserver.py**: Contains the server code for computation services.
  - **fileserver.py**: Contains the server code for file services.
  - **requirements_server.txt**: Lists the dependencies required for the server.
  - **services.proto**: Defines the gRPC services and messages.
  - **server_files/**: The directory being synchronized with the client.

## Prerequisites

Ensure you have the following installed:
- Python 3.6+
- `pip` (Python package installer)

## Setup Instructions

### 1. Create a Virtual Environment

First, create a virtual environment named `dsp1_server_venv`:

```bash
python -m venv dsp1_server_venv
```

### 2. Activate the Virtual Environment
Activate the virtual environment. On Windows, use:

```bash
.\dsp1_server_venv\Scripts\activate
```
On macOS and Linux, use:

```bash
source dsp1_server_venv/bin/activate
```

### 3. Install Dependencies
Install the required dependencies from the requirements_server.txt file:

```bash
pip install -r requirements_server.txt
```

### 4. Generate gRPC Code
Generate the gRPC code from the services.proto file using the grpc_tools.protoc command:

```bash
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. services.proto
```

### 5. Start the Server

```bash
python computationserver.py
python fileserver.py
```