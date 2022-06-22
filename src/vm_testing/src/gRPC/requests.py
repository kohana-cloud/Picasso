import gRPC.proto.query_pb2_grpc as rpc
import gRPC.proto.query_pb2 as chat
import threading
import random
import grpc
import uuid
import time

SERVER_HOST = "192.168.1.44"
SERVER_PORT = 15002

class Client:
    def __init__(self, tls=True):
        if tls:
            with open('gRPC/cert/server.crt', 'rb') as fio:
                tls_secret = grpc.ssl_channel_credentials(fio.read())
            self.channel = grpc.secure_channel(f"{SERVER_HOST}:{SERVER_PORT}", tls_secret)
        else:
            self.channel = grpc.insecure_channel(f"{SERVER_HOST}:{SERVER_PORT}")

        self.connection = rpc.HoneypotManagementServerStub(self.channel)

        # Create new listening thread for when new message streams come in
        threading.Thread(target=self.__listen_for_responses, daemon=True).start()

    def __listen_for_responses(self):
        # This is a blocking thread, recieve message responses   
        for event in self.connection.ChatStream(chat.Empty()):  
            print(f"Response[{event.type}] {event.message}")

    def send_message(self, type:str, message:str):
        event = chat.Event(type=type,message=message)

        self.connection.SendEvent(event)  # send the event to the server
