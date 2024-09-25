import grpc
import logging
import time

import services_pb2
import services_pb2_grpc

class ComputationClient:
    def __init__(self, computation_service_address):
        self.computation_channel = grpc.insecure_channel(computation_service_address)
        self.computation_stub = services_pb2_grpc.ComputationServiceStub(self.computation_channel)

    def add(self, i, j):
        request = services_pb2.AddRequest(i=i, j=j)
        try:
            response = self.computation_stub.Add(request)
            logging.info(f"Add {i} + {j} = {response.result}")
            return response.result
        except grpc.RpcError as e:
            logging.error(f"Add RPC failed: {e}")
            return None

    def sort(self, array):
        request = services_pb2.SortRequest(array=array)
        try:
            response = self.computation_stub.Sort(request)
            logging.info(f"Sort {array} = {response.sorted_array}")
            return response.sorted_array
        except grpc.RpcError as e:
            logging.error(f"Sort RPC failed: {e}")
            return None

    def add_async(self, i, j):
        request = services_pb2.AddRequest(i=i, j=j)
        try:
            response = self.computation_stub.AddAsync(request)
            logging.info(f"AddAsync {i} + {j}: Acknowledgment received with ack_id {response.ack_id}")
            return response.ack_id
        except grpc.RpcError as e:
            logging.error(f"AddAsync RPC failed: {e}")
            return None

    def sort_async(self, array):
        request = services_pb2.SortRequest(array=array)
        try:
            response = self.computation_stub.SortAsync(request)
            logging.info(f"SortAsync {array}: Acknowledgment received with ack_id {response.ack_id}")
            return response.ack_id
        except grpc.RpcError as e:
            logging.error(f"SortAsync RPC failed: {e}")
            return None

    def get_result(self, ack_id):
        request = services_pb2.ResultRequest(ack_id=ack_id)
        try:
            response = self.computation_stub.GetResult(request)
            if response.HasField("add_result"):
                logging.info(f"Result of {ack_id} is add_result: {response.add_result}")
                return response.add_result
            elif response.HasField("sort_result"):
                logging.info(f"Result of {ack_id} is sort_result: {response.sort_result}")
                return response.sort_result.sorted_array
            else:
                logging.warning(f"Result of {ack_id} not found")
                return None
        except grpc.RpcError as e:
            logging.error(f"GetResult RPC failed: {e}")
            return None

    def wait_for_result(self, ack_id, timeout=30):
        start_time = time.time()
        while time.time() - start_time < timeout:
            result = self.get_result(ack_id)
            if result is not None:
                return result
            time.sleep(1)
        logging.warning(f"Timeout waiting for result with ack_id: {ack_id}")
        return None

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    computation_client = ComputationClient("localhost:50052")

    # Perform synchronous computation operations
    i = int(input("Enter the first number for addition: "))
    j = int(input("Enter the second number for addition: "))
    result = computation_client.add(i, j)
    logging.info(f"Synchronous Add result: {result}")

    array = list(map(int, input("Enter the numbers for sorting (separated by space): ").split()))
    sorted_array = computation_client.sort(array)
    logging.info(f"Synchronous Sort result: {sorted_array}")

    # Perform asynchronous computation operations
    i = int(input("Enter the first number for asynchronous addition: "))
    j = int(input("Enter the second number for asynchronous addition: "))
    ack_id_add = computation_client.add_async(i, j)

    array = list(map(int, input("Enter the numbers for asynchronous sorting (separated by space): ").split()))
    ack_id_sort = computation_client.sort_async(array)

    # Wait and get results of asynchronous operations
    result_add = computation_client.wait_for_result(ack_id_add)
    result_sort = computation_client.wait_for_result(ack_id_sort)

    logging.info(f"Asynchronous Add result: {result_add}")
    logging.info(f"Asynchronous Sort result: {result_sort}")
