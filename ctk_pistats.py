import customtkinter as ctk
import psutil
import socket

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

app = ctk.CTk()
app.geometry("320x240")
app.overrideredirect(True)

# function to get CPU usage
def get_cpu_usage():
    return psutil.cpu_percent(interval=None)

# function to get RAM usage
def get_ram_usage():
    return psutil.virtual_memory().percent

# function to get HDD usage
def get_hdd_usage(mount_point):
    disk_usage = psutil.disk_usage(mount_point)
    total_gb = disk_usage.total / (1024 ** 4)
    used_gb = disk_usage.used / (1024 ** 3)
    free_gb = disk_usage.free / (1024 ** 4)
    perc_used = disk_usage.percent
    return total_gb, used_gb, free_gb, perc_used

mount_point = '/'
result = get_hdd_usage(mount_point)

# HDD read and write speeds
def get_disk_io(device_name):
    io_counters = psutil.disk_io_counters(perdisk=True)
    if device_name in io_counters:
        return io_counters[device_name]
    else:
        return None

device_name = 'disk0'
previous_io = get_disk_io(device_name)

# function to get IP Address
def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip

# Create labels for displaying system stats
sightline_label = ctk.CTkLabel(app, text="Sightline NAS")
sightline_label.pack()
cpu_label = ctk.CTkLabel(app, text="CPU Usage: ", text_color="#a2f507")
cpu_label.pack()
ram_label = ctk.CTkLabel(app, text="RAM Usage: ", text_color="#a2f507")
ram_label.pack()
disk_label = ctk.CTkLabel(app, text="Disk Usage: ", text_color="#f1f514")
disk_label.pack()
io_label = ctk.CTkLabel(app, text="Disk IO: ", text_color="#f1f514")
io_label.pack()
ip_label = ctk.CTkLabel(app, text="NAS IP: ", text_color="#14f5ea")
ip_label.pack()

# Main Function
def display_system_stats():
    global previous_io

    cpu = get_cpu_usage()
    ram = get_ram_usage()
    ipadd = get_ip_address()
    total_gb, used_gb, free_gb, perc_used = result
    current_io = get_disk_io(device_name)
    if current_io is None:
        print(f"Error: No IO data for device {device_name}")
        return
    read_speed = (current_io.read_bytes - previous_io.read_bytes) / (1024 * 1024)
    write_speed = (current_io.write_bytes - previous_io.write_bytes) / (1024 * 1024)
    previous_io = current_io
    
    cpu_label.configure(text=f'CPU Usage: {cpu}%')
    ram_label.configure(text=f'RAM Usage: {ram}%')
    disk_label.configure(text=f'Total Disk Space: {total_gb:.2f} TB\nUsed Disk Space: {used_gb:.1f} GB\nFree Disk Space: {free_gb:.2f} TB\nPercentage Disk used: {perc_used} %')
    io_label.configure(text=f'Read Speed: {read_speed:.2f} mbps\nWrite Speed: {write_speed:.2f} mbps')
    ip_label.configure(text=f'NAS IP: {ipadd}')
    
    app.after(2000, display_system_stats)  # Schedule the function to run again after 2 seconds

# Start the periodic update
if previous_io is None:
    print(f"Error: No initial IO data for device {device_name}")
else:
    app.after(0, display_system_stats)

app.mainloop()