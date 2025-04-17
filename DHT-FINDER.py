import requests
import json
import os
import socket
import time
from termcolor import cprint, colored
import pyfiglet
from webbrowser import open as web_open
from concurrent.futures import ThreadPoolExecutor

# Terminal Colors
R = '\033[91m'
G = '\033[92m'
Y = '\033[93m'
B = '\033[94m'
P = '\033[95m'
C = '\033[96m'
N = '\033[0m'

clear = lambda: os.system('cls' if os.name == 'nt' else 'clear')

def show_banner(text, color):
    clear()
    banner = pyfiglet.figlet_format(text, "dos_rebel")
    print(f"{color}{banner}{N}")

def dht_hackers_banner():
    show_banner("DHT-HACKERS", R)
    print(f"{C}────────────────────────────────────────────────────────────")
    print(f"{G} THIS TOOL IS PAID! TO USE IT FOR FREE:")
    print(f"{P} SUBSCRIBE TO OUR CHANNEL FOR ETHICAL HACKING TUTORIALS!")
    print(f"{B} https://youtube.com/@dht-hackers_10")
    print(f"{C}────────────────────────────────────────────────────────────{N}")
    time.sleep(2)
    web_open("https://youtube.com/@dht-hackers_10")
    input(f"{Y}Press Enter after subscribing to continue...{N}")
    clear()

def dht_ip_banner():
    show_banner("DHT-FINDER", B)
    print(f"{C}────────────────────────────────────────────────────────────")
    print(f"{G} FAST & POWERFUL IP INFORMATION GATHERING TOOL")
    print(f"{Y} Developed by: DHT-HACKERS TEAM | Multi-threaded | High Performance")
    print(f"{Y} CODED by: KRISHU")
    print(f"{C}────────────────────────────────────────────────────────────{N}")

def ip_info(ip):
    try:
        url = f"http://ip-api.com/json/{ip}?fields=status,message,country,regionName,city,zip,lat,lon,isp,org,as,query"
        response = requests.get(url, timeout=5)
        return response.json()
    except requests.RequestException as e:
        return {"status": "fail", "message": str(e)}

# Threaded port scanner
def scan_port(ip, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            if s.connect_ex((ip, port)) == 0:
                return port
    except:
        pass
    return None

def port_scan(ip):
    common_ports = [21, 22, 23, 25, 53, 80, 110, 443, 3306, 8080, 8443, 137, 139, 445, 1433]
    cprint("\n[+] Scanning for open ports (multi-threaded)...", "yellow")

    open_ports = []
    with ThreadPoolExecutor(max_workers=50) as executor:
        futures = [executor.submit(scan_port, ip, port) for port in common_ports]
        for future in futures:
            result = future.result()
            if result:
                open_ports.append(result)
    return open_ports

def save_report(data):
    try:
        with open("dht_ip_report.txt", "a") as f:
            f.write(json.dumps(data, indent=2) + "\n")
        cprint("[+] Report saved to dht_ip_report.txt", "green")
    except Exception as e:
        cprint(f"[!] Failed to save report: {e}", "red")

def main():
    dht_hackers_banner()
    dht_ip_banner()

    ip = input(colored("[?] Enter IP to investigate (or type 'exit' to quit): ", "yellow")).strip()
    if ip.lower() == "exit":
        cprint("\n[!] Exiting. Thanks for using DHT-Finder!", "cyan")
        return False

    cprint("\n[+] Fetching IP info...", "green")
    data = ip_info(ip)

    if data["status"] != "success":
        cprint(f"[!] Error: {data.get('message', 'Unknown error')}", "red")
        return True

    cprint(f"\n[+] IP Info for {data['query']}:", "cyan")
    for key, val in data.items():
        if key != "status":
            print(f"{key.capitalize():<12}: {val}")

    open_ports = port_scan(ip)
    if open_ports:
        cprint(f"\n[+] Open Ports: {', '.join(map(str, open_ports))}", "green")
    else:
        cprint("\n[-] No common ports open or scan blocked.", "red")

    save_report(data)
    input("press enter...")
    return True

if __name__ == "__main__":
    try:
        while True:
            if not main():
                break
    except KeyboardInterrupt:
        cprint("\n[!] Interrupted by user. Exiting...", "red")
