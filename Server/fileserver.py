import os
import grpc
import logging
from concurrent import futures
import services_pb2
import services_pb2_grpc

class FileService(services_pb2_grpc.FileServiceServicer):
    def __init__(self, base_dir):
        self.base_dir = base_dir
        if not os.path.exists(base_dir):
            os.makedirs(base_dir)
        logging.info(f"Initialized FileService with base directory: {base_dir}")

    def UploadFile(self, request, context):
        full_path = os.path.join(self.base_dir, request.filename)
        with open(full_path, 'wb') as f:
            f.write(request.content)
        logging.info(f"Uploaded file: {request.filename}")
        return services_pb2.UploadFileResponse(success=True)

    def DeleteFile(self, request, context):
        full_path = os.path.join(self.base_dir, request.filename)
        if os.path.exists(full_path):
            os.remove(full_path)
            logging.info(f"Deleted file: {request.filename}")
            return services_pb2.DeleteFileResponse(success=True)
        logging.warning(f"Failed to delete file (not found): {request.filename}")
        return services_pb2.DeleteFileResponse(success=False)

    def RenameFile(self, request, context):
        old_full_path = os.path.join(self.base_dir, request.old_filename)
        new_full_path = os.path.join(self.base_dir, request.new_filename)
        if os.path.exists(old_full_path):
            os.rename(old_full_path, new_full_path)
            logging.info(f"Renamed file from {request.old_filename} to {request.new_filename}")
            return services_pb2.RenameFileResponse(success=True)
        logging.warning(f"Failed to rename file (not found): {request.old_filename}")
        return services_pb2.RenameFileResponse(success=False)

def serve():
    logging.basicConfig(level=logging.INFO)
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    services_pb2_grpc.add_FileServiceServicer_to_server(FileService("server_files"), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    logging.info("File Server running on port 50051...")
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
