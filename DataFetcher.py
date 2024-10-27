import platform
import socket
import getpass
import os
import subprocess
import psutil
from screeninfo import get_monitors
from datetime import datetime


### OS INFO ###
def get_os_info():
    os_name = platform.system()
    os_version = platform.version()
    kernel_version = platform.release()
    architecture = platform.machine()
    return os_name, os_version, kernel_version, architecture


### CPU/GPU AND HARDWARE INFO ###
def get_cpu_info():
    cpu_model = platform.processor()
    cpu_cores = psutil.cpu_count(logical=False)
    cpu_threads = psutil.cpu_count(logical=True)
    cpu_freq = psutil.cpu_freq().current
    return cpu_model, cpu_cores, cpu_threads, cpu_freq

def get_gpu_info():
    try:
        gpu_info = subprocess.check_output("wmic path win32_videocontroller get name", shell=True).decode().strip().split('\n')[1:]
        gpu_model = gpu_info[0].strip() if gpu_info else "Unknown"
    except Exception as e:
        gpu_model = f"Error retrieving GPU info: {e}"
    return gpu_model

def get_memory_info():
    ram_total = psutil.virtual_memory().total / (1024**3)  # In GB
    ram_used = psutil.virtual_memory().used / (1024**3)
    ram_free = psutil.virtual_memory().available / (1024**3)
    swap_total = psutil.swap_memory().total / (1024**3)
    swap_used = psutil.swap_memory().used / (1024**3)
    return ram_total, ram_used, ram_free, swap_total, swap_used

def get_storage_info():
    disk_partitions = psutil.disk_partitions()
    disk_usage = [(part.device, psutil.disk_usage(part.mountpoint)) for part in disk_partitions]
    return disk_usage


### NETWORK INFO ###
def get_ip_info():
    local_ip = socket.gethostbyname(socket.gethostname())
    return local_ip

def get_wifi_ssid():
    try:
        wifi_info = subprocess.check_output("netsh wlan show interfaces", shell=True).decode()
        ssid = [line.split(":")[1].strip() for line in wifi_info.splitlines() if "SSID" in line][0]
    except IndexError:
        ssid = "No Wi-Fi SSID found"
    return ssid

def get_mac_address():
    interfaces = psutil.net_if_addrs()
    for interface, addresses in interfaces.items():
        for address in addresses:
            if address.family == psutil.AF_LINK:  # AF_LINK corresponds to MAC addresses
                return address.address
    return "MAC Address not found"

def get_hostname():
    hostname = socket.gethostname()
    return hostname

### SHELL AND TERMINAL INFO ###
def get_shell_info():
    shell = os.environ.get('ComSpec', 'Unknown Shell')  # 'ComSpec' is the Windows equivalent of SHELL
    return shell

def get_uptime():
    boot_time = datetime.fromtimestamp(psutil.boot_time())
    uptime = datetime.now() - boot_time
    return uptime

### USER AND SESSION INFO ###
def get_user_info():
    username = getpass.getuser()
    host = socket.gethostname()
    return username, host

def get_process_count():
    total_processes = len(psutil.pids())
    return total_processes

def get_high_usage_processes():
    high_usage_processes = [(p.info['name'], p.info['cpu_percent']) for p in psutil.process_iter(['name', 'cpu_percent'])]
    return high_usage_processes

### BATTERY AND POWER INFO
def get_battery_info():
    battery = psutil.sensors_battery()
    if battery:
        battery_percentage = battery.percent
        battery_status = "Charging" if battery.power_plugged else "Discharging"
    else:
        battery_percentage = None
        battery_status = "No Battery Found"
    return battery_percentage, battery_status

### LOAD AND PERFORMANCE INFO ###
def get_cpu_usage():
    cpu_usage = psutil.cpu_percent(interval=1)
    return cpu_usage

def get_memory_usage():
    memory_usage = psutil.virtual_memory().percent
    return memory_usage


### DISPLAY INFO ###
def get_display_info():
    monitors = [(monitor.width, monitor.height) for monitor in get_monitors()]
    return monitors
