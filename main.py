import tkinter as tk
from tkinter import ttk
import psutil
import socket
import platform

class SystemInfoWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("imBobby")
        self.configure(bg="black")

        notebook = ttk.Notebook(self, style="Dark.TNotebook")
        notebook.pack(fill="both", expand=True)

        system_info_tab = tk.Frame(notebook, bg="black")
        hardware_monitor_tab = tk.Frame(notebook, bg="black")

        notebook.add(system_info_tab, text="General")
        notebook.add(hardware_monitor_tab, text="Monitor")

        self.create_system_info_tab(system_info_tab)
        self.create_hardware_monitor_tab(hardware_monitor_tab)

    def create_system_info_tab(self, tab):
        general_label = tk.Label(tab, text="General", font=("Hack", 12), bg="#232323", fg="#FF8200")
        general_label.pack(fill='x', padx=(10, 395), pady=(10, 0)) 

        system_info = get_system_info()
        for key, value in system_info.items():
            label = tk.Label(tab, text=f"{key}: {value}", justify='left', anchor='w', font=("Hack", 10), bg="#121212", fg="#FF8200", padx=10, pady=10)
            label.pack(fill='x', padx=(10, 395), pady=(0))

        last_label = tk.Label(tab, text="", bg="#121212", height=0)
        last_label.pack(fill='x', padx=(10, 395), pady=(0, 10))

    def create_hardware_monitor_tab(self, tab):
        network_frame = tk.Frame(tab, relief=tk.GROOVE, borderwidth=0, bg="#232323")
        hardware_frame = tk.Frame(tab, relief=tk.GROOVE, borderwidth=0, bg="#232323")
        disk_frame = tk.Frame(tab, relief=tk.GROOVE, borderwidth=0, bg="#232323")

        network_label = tk.Label(network_frame, text="Network Information", font=("Hack", 12), bg="#232323", fg="#FF8200")
        hardware_label = tk.Label(hardware_frame, text="Hardware Info", font=("Hack", 12), bg="#232323", fg="#FF8200")
        disk_label = tk.Label(disk_frame, text="Disk Space", font=("Hack", 12), bg="#232323", fg="#FF8200")

        network_info = tk.Label(network_frame, text="", justify=tk.LEFT, anchor=tk.N, font=("Hack", 10), bg="#121212", fg="#FF8200", padx=10, pady=10, height=20)
        hardware_info = tk.Label(hardware_frame, text="", justify=tk.LEFT, anchor=tk.N, font=("Hack", 10), bg="#121212", fg="#FF8200", padx=10, pady=10, height=20)
        disk_info = tk.Label(disk_frame, text="", justify=tk.LEFT, anchor=tk.N, font=("Hack", 10), bg="#121212", fg="#FF8200", padx=10, pady=10, height=20)

        network_label.pack()
        network_info.pack()
        hardware_label.pack()
        hardware_info.pack()
        disk_label.pack()
        disk_info.pack()

        network_frame.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')
        hardware_frame.grid(row=0, column=1, padx=10, pady=10, sticky='nsew')
        disk_frame.grid(row=0, column=2, padx=10, pady=10, sticky='nsew')

        self.update_hardware_monitor(network_info, hardware_info, disk_info)

    def update_hardware_monitor(self, network_info, hardware_info, disk_info):
        network_data = get_network_info()
        network_info.configure(text=network_data)

        hardware_data = get_hardware_usage()
        hardware_info.configure(text=hardware_data)

        disk_data = get_disk_space()
        disk_info.configure(text=disk_data)

        self.after(5000, self.update_hardware_monitor, network_info, hardware_info, disk_info)

def get_network_info():
    info = psutil.net_if_addrs()
    formatted_info = ""
    for interface, addrs in info.items():
        formatted_info += f"Interface: {interface}\n"
        for addr in addrs:
            if addr.family == socket.AF_INET:
                formatted_info += f"  IP Address: {addr.address}\n"
            elif addr.family == socket.AF_LINK:
                formatted_info += f"  MAC Address: {addr.address}\n"
        formatted_info += "\n"
    return formatted_info

def get_hardware_usage():
    cpu_usage = psutil.cpu_percent()
    memory = psutil.virtual_memory()
    system_info = platform.uname()

    hardware_info = f"System: {system_info.system}\n"
    hardware_info += f"Node Name: {system_info.node}\n"
    hardware_info += f"Release: {system_info.release}\n"
    hardware_info += f"Version: {system_info.version}\n"
    hardware_info += f"Machine: {system_info.machine}\n"
    hardware_info += f"Processor: {system_info.processor}\n"

    return f"CPU Usage: {cpu_usage:.2f}%\nMemory Usage: {memory.percent:.2f}%\n{hardware_info}"

def get_disk_space():
    partitions = psutil.disk_partitions()
    info = ""
    for partition in partitions:
        usage = psutil.disk_usage(partition.mountpoint)
        info += f"Drive {partition.device}\n"
        info += f"Total Space: {usage.total / (1024 ** 3):.2f} GB\n"
        info += f"Used Space: {usage.used / (1024 ** 3):.2f} GB\n"
        info += f"Free Space: {usage.free / (1024 ** 3):.2f} GB\n\n"
    return info

def get_processor_info():
    cpu_info = platform.processor()
    try:
        cpu_freq = psutil.cpu_freq().current / 1000  # Convert to GHz
    except AttributeError:
        cpu_freq = "N/A"  # If the clock speed information is not available
    return f"{cpu_info} @ {cpu_freq} GHz"

def get_windows_edition():
    import winreg

    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows NT\CurrentVersion") as key:
            edition = winreg.QueryValueEx(key, "ProductName")[0]
            version = winreg.QueryValueEx(key, "DisplayVersion")[0]
    except Exception as e:
        edition = "N/A"
        version = "N/A"

    return f"{edition} ({version})"

def get_macos_edition():
    try:
        os_version = platform.mac_ver()[0]
    except Exception as e:
        os_version = "N/A"

    return f"macOS {os_version}"

def get_linux_edition():
    try:
        with open("/etc/os-release", "r") as file:
            lines = file.readlines()
            edition = next((line.split('=')[1].strip('"') for line in lines if line.startswith("PRETTY_NAME")), "N/A")
    except Exception as e:
        edition = "N/A"

    return edition

def get_system_info():
    system_info = {
        "Device name": platform.node(),
        "Processor": get_processor_info(),
        "Installed RAM": f"{round(psutil.virtual_memory().total / (1024**3), 2)} GB",
        "Device ID": platform.node(),
        "System type": platform.architecture()[0],
        "Edition": get_edition_info(),
        "Version": platform.version(),
        "Installed on": platform.system(),
        "OS build": platform.release(),
    }
    return system_info

def get_edition_info():
    system = platform.system()
    if system == "Windows":
        return get_windows_edition()
    elif system == "Darwin":  # macOS
        return get_macos_edition()
    elif system == "Linux":
        return get_linux_edition()
    else:
        return "N/A"

if __name__ == "__main__":
    app = SystemInfoWindow()
    app.mainloop()
