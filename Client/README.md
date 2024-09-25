# Client Setup

This guide will help you set up the client environment, install the necessary dependencies, and generate the required gRPC code from the `services.proto` file.
## Folder Structure

The project directory is organized as follows:
- **Client/**:
  - **computation_client.py**: Contains the client code for computation services.
  - **file_client.py**: Contains the client code for file synchronization services.
  - **requirements_client.txt**: Lists the dependencies required for the client.
  - **services.proto**: Defines the gRPC services and messages.
  - **sync_folder/**: The directory being synchronized with the server.
## Prerequisites

Ensure you have the following installed:
- Python 3.6+
- `pip` (Python package installer)

## Setup Instructions

### 1. Create a Virtual Environment

First, create a virtual environment named `dsp1_client_venv`:

```bash
python -m venv dsp1_client_venv
```

### 2. Activate the Virtual Environment
Activate the virtual environment. On Windows, use:

```bash
.\dsp1_client_venv\Scripts\activate
```
On macOS and Linux, use:

```bash
source dsp1_client_venv/bin/activate
```

### 3. Install Dependencies
Install the required dependencies from the requirements_client.txt file:

```bash
pip install -r requirements_client.txt
```

### 4. Generate gRPC Code
Generate the gRPC code from the services.proto file using the grpc_tools.protoc command:

```bash
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. services.proto
```

### 5.Running the Client code
To run the client code,  execute the Python scripts computation_client.py and file_client.py.

```bash
python computation_client.py
python file_client.py
```
