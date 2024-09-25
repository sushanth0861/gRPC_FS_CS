import grpc
import logging
from concurrent import futures
import services_pb2
import services_pb2_grpc
from concurrent.futures import ThreadPoolExecutor
import uuid
import time

class ComputationService(services_pb2_grpc.ComputationServiceServicer):
    def __init__(self):
        self.results = {}
        self.executor = ThreadPoolExecutor(max_workers=10)

    def Add(self, request, context):
        result = request.i + request.j
        logging.info(f"Computed Add: {request.i} + {request.j} = {result}")
        return services_pb2.AddResponse(result=result)

    def Sort(self, request, context):
        sorted_array = sorted(request.array)
        logging.info(f"Computed Sort: {request.array} -> {sorted_array}")
        return services_pb2.SortResponse(sorted_array=sorted_array)

    def AddAsync(self, request, context):
        ack_id = str(uuid.uuid4())
        logging.info(f"Received AddAsync request: {request.i} + {request.j}, ack_id={ack_id}")
        self.executor.submit(self._process_add, ack_id, request)
        return services_pb2.AckResponse(ack_id=ack_id)

    def SortAsync(self, request, context):
        ack_id = str(uuid.uuid4())
        logging.info(f"Received SortAsync request: {request.array}, ack_id={ack_id}")
        self.executor.submit(self._process_sort, ack_id, request)
        return services_pb2.AckResponse(ack_id=ack_id)

    def GetResult(self, request, context):
        result = self.results.pop(request.ack_id, None)
        if result:
            logging.info(f"Result found for ack_id={request.ack_id}")
            return result
        else:
            logging.warning(f"Result not found for ack_id={request.ack_id}")
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('Result not found')
            return services_pb2.ResultResponse()

    def _process_add(self, ack_id, request):
        result = request.i + request.j
        response = services_pb2.ResultResponse(add_result=result)
        self.results[ack_id] = response
        logging.info(f"Processed AddAsync for ack_id={ack_id}, result={result}")

    def _process_sort(self, ack_id, request):
        sorted_array = sorted(request.array)
        response = services_pb2.ResultResponse(sort_result=services_pb2.SortResponse(sorted_array=sorted_array))
        self.results[ack_id] = response
        logging.info(f"Processed SortAsync for ack_id={ack_id}, sorted_array={sorted_array}")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    services_pb2_grpc.add_ComputationServiceServicer_to_server(ComputationService(), server)
    server.add_insecure_port('[::]:50052')
    server.start()
    logging.info("Computation Server running on port 50052...")
    server.wait_for_termination()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    serve()
