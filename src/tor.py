# Credits : Xolo/@efenatuyo
# Notice : this code aswell as "Tor.exe" is not part of our Lisence.

# U might be concerned with the Tor.exe file, it is the official Tor executable that can be download off of the tor website : 
# https://archive.torproject.org/tor-package-archive/torbrowser/13.0.16/tor-expert-bundle-windows-x86_64-13.0.16.tar.gz
# File's SHA256 : 66fd723d0dd219807c6d7dcc331e25c8d05adccf4a66312928fbe1d0e45670ed

import os, subprocess, psutil, requests, time, platform

class ServiceInstaller:
    def __init__(self, amount, proxy_start_port):
        self.amount = amount
        self.proxy_start_port = proxy_start_port
        self.Stop_Tor_Windows()

    def Generate_Config(self, config_path):
        tor_config = f"SOCKSPort {self.proxy_start_port}\n"
        # tor_config += "ExitNodes {fr},{de},{nl}\nExcludeExitNodes {us},{cn},{ru}\n" download geoip files if u wanna use this
        tor_config += "BandwidthRate 1GB\nBandwidthBurst 1GB\n"
        for i in range(self.amount):
            tor_config += f"HTTPTunnelPort {self.proxy_start_port + i+1}\n"
        with open(config_path, 'w') as f:
            f.write(tor_config)
        
    def download_tor(self):
        tor_url = "https://github.com/Bueezi/ZeFinder-Roblox-Group-Finder/raw/2fa8c1f08a5ab3a30946a97708b8f5566f10a621/src/tor/tor.exe" # We use the version of a commit so that the exe stays the same even if we change it in the repo
        response = requests.get(tor_url)
        if response.status_code != 200:
            return None
        exe_path = "src\\tor\\tor.exe"
        with open(exe_path, 'wb') as f:
            f.write(response.content)

    def Start_Tor(self):
        exe_path = "src\\tor\\tor.exe"
        config_path = "src\\tor\\config"
        self.Generate_Config(config_path)

        if platform.system() == "Linux":
            print("Running on Linux")
            process = subprocess.Popen(["/usr/bin/tor", "-f", config_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        else:
            if not os.path.isfile(exe_path):
                print("Getting Tor...")
                self.download_tor()
            process = subprocess.Popen(f"{exe_path} -nt-service -f {config_path}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        while 1:
            line = process.stdout.readline().decode().strip()
            time.sleep(0.001)
            # time.sleep(0.05) # Comment this out for debugging
            print(line)
            if "Bootstrapped 100% (done): Done" in line:
                break
            
    def Stop_Tor_Windows(self):
        for proc in psutil.process_iter():
            try:
                if proc.name() == "tor.exe":
                    proc.terminate()
                    
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass

def Make_Proxies(amount, proxy_start_port):
    ServiceInstaller(amount, proxy_start_port).Start_Tor()
    print("Tor Succesfully inited")
    return