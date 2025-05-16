import socket
import json

UDP_IP = "0.0.0.0"
UDP_PORT = 14550
BUFFER_SIZE = 2048

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

print(f"[RFD] Listening for RC commands on {UDP_IP}:{UDP_PORT}")

while True:
    data, addr = sock.recvfrom(BUFFER_SIZE)
    try:
        rc_frame = json.loads(data.decode('utf-8'))
        print(f"[RC] From {addr}: {rc_frame}")
    except Exception as e:
        print(f"[ERROR] Failed to parse packet from {addr}: {e}")
