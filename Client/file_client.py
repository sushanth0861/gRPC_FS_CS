import os
import grpc
import time
import logging
import threading
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

import services_pb2
import services_pb2_grpc

# gRPC channel options to disable HTTP proxy
grpc_channel_options = [('grpc.enable_http_proxy', 0)]

class FileClient:
    def __init__(self, file_service_address, sync_dir):
        self.file_channel = grpc.insecure_channel(file_service_address, options=grpc_channel_options)
        self.file_stub = services_pb2_grpc.FileServiceStub(self.file_channel)
        self.sync_dir = sync_dir
        self.logger = self.setup_logger()

    def setup_logger(self):
        logger = logging.getLogger('file_client')
        logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        ch = logging.StreamHandler()
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        return logger

    def upload_file(self, file_path):
        try:
            with open(file_path, 'rb') as f:
                content = f.read()
            filename = os.path.relpath(file_path, self.sync_dir)
            request = services_pb2.UploadFileRequest(filename=filename, content=content)
            response = self.file_stub.UploadFile(request)
            self.logger.info(f"Upload file '{filename}': {response.success}")
        except grpc.RpcError as e:
            self.logger.error(f"Error uploading file '{file_path}': {e}")

    def delete_file(self, file_path):
        try:
            filename = os.path.relpath(file_path, self.sync_dir)
            request = services_pb2.DeleteFileRequest(filename=filename)
            response = self.file_stub.DeleteFile(request)
            self.logger.info(f"Delete file '{filename}': {response.success}")
        except grpc.RpcError as e:
            self.logger.error(f"Error deleting file '{file_path}': {e}")

    def rename_file(self, old_file_path, new_file_path):
        try:
            old_filename = os.path.relpath(old_file_path, self.sync_dir)
            new_filename = os.path.relpath(new_file_path, self.sync_dir)
            request = services_pb2.RenameFileRequest(old_filename=old_filename, new_filename=new_filename)
            response = self.file_stub.RenameFile(request)
            self.logger.info(f"Rename file from '{old_filename}' to '{new_filename}': {response.success}")
        except grpc.RpcError as e:
            self.logger.error(f"Error renaming file '{old_file_path}' to '{new_file_path}': {e}")

    def start_watchdog(self):
        observer = Observer()
        observer.schedule(SyncEventHandler(self), self.sync_dir, recursive=True)
        observer.start()
        self.logger.info(f"Watching directory '{self.sync_dir}' for changes...")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()

class SyncEventHandler(FileSystemEventHandler):
    def __init__(self, file_client):
        super().__init__()
        self.file_client = file_client

    def on_created(self, event):
        if event.is_directory:
            return
        self.file_client.upload_file(event.src_path)

    def on_modified(self, event):
        if event.is_directory:
            return
        self.file_client.upload_file(event.src_path)

    def on_deleted(self, event):
        if event.is_directory:
            return
        self.file_client.delete_file(event.src_path)

    def on_moved(self, event):
        if event.is_directory:
            return
        self.file_client.rename_file(event.src_path, event.dest_path)

if __name__ == "__main__":
    file_client = FileClient("localhost:50051", "sync_folder")
    file_client.start_watchdog()
