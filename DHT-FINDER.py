import requests
import json
import os
from termcolor import cprint, colored
import time
import itertools
import string
import pyfiglet

R = '\033[91m'
G = '\033[92m'
Y = '\033[93m'
B = '\033[94m'
P = '\033[95m'
C = '\033[96m'
W = '\033[97m'
N = '\033[0m'

clear = lambda: os.system('cls' if os.name == 'nt' else 'clear')

def show_banner(text, color):
    clear()
    banner = pyfiglet.figlet_format(text)
    print(f"{color}{banner}{N}")

def dht_hackers_banner():
    show_banner("DHT-HACKERS", R)
    print(f"{C}────────────────────────────────────────────────────────────")
    print(f"{G} THIS TOOL IS PAID! TO USE IT FOR FREE:")
    print(f"{P} SUBSCRIBE TO OUR CHANNEL FOR ETHICAL HACKING TUTORIALS!")
    print(f"{B} https://youtube.com/@dht-hackers_10?si=lsdJ-naJvp7ql-QT")
    print(f"{C}────────────────────────────────────────────────────────────{N}")
    time.sleep(2)
    os.system("termux-open-url https://youtube.com/@dht-hackers_10?si=lsdJ-naJvp7ql-QT")
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
    url = f"http://ip-api.com/json/{ip}?fields=status,message,country,regionName,city,zip,lat,lon,isp,org,as,query"
    response = requests.get(url).json()
    return response

def port_scan(ip):
    common_ports = [21, 22, 23, 25, 53, 80, 110, 443, 3306]
    open_ports = []
    cprint("\n[+] Scanning for open ports...", "yellow")
    for port in common_ports:
        result = os.system(f"timeout 1 bash -c '</dev/tcp/{ip}/{port}' 2>/dev/null && echo {port} open'")
        if result == 0:
            open_ports.append(port)
    return open_ports

def main():
    dht_hackers_banner()
    dht_ip_banner()
    ip = input(colored("[?] Enter IP to investigate: ", "yellow"))
    
    cprint("\n[+] Fetching IP info...", "green")
    data = ip_info(ip)

    if data["status"] != "success":
        cprint("[!] Failed to fetch IP info!", "red")
        return

    cprint(f"\n[+] IP Info for {data['query']}:", "cyan")
    print(f"Country     : {data['country']}")
    print(f"Region      : {data['regionName']}")
    print(f"City        : {data['city']}")
    print(f"ZIP Code    : {data['zip']}")
    print(f"Latitude    : {data['lat']}")
    print(f"Longitude   : {data['lon']}")
    print(f"ISP         : {data['isp']}")
    print(f"Organization: {data['org']}")
    print(f"ASN         : {data['as']}")
    
    # Port Scan
    ports = port_scan(ip)
    if ports:
        cprint(f"\n[+] Open Ports: {', '.join(str(p) for p in ports)}", "green")
    else:
        cprint("\n[-] No common ports open or scan blocked.", "red")

    # Save Report
    with open("dht_ip_report.txt", "a") as f:
        f.write(json.dumps(data, indent=2) + "\n")
    cprint("\n[+] Report saved to dht_ip_report.txt", "green")

if __name__ == "__main__":
    main()
