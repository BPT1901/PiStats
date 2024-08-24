import psutil
import socket
import time
import curses

FONT_SIZE_20 = '\033[20m'
FONT_SIZE_RESET = '\033[0m'

# function to get CPU usage
def get_cpu_usage():
    return psutil.cpu_percent(interval=2)
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

mount_point = '/srv/dev-disk-by-uuid-9d5957bc-1987-4e7f-9a6f-d0aad72c036f'
result = get_hdd_usage(mount_point)

# HDD read and write speeds
def get_disk_io(device_name):
  io_counters = psutil.disk_io_counters(perdisk=True)
  if device_name in io_counters:
      return io_counters[device_name]
  else:
      return None

device_name = 'sda1'


# function to get IP Address
def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    return ip


#Main Function
def display_system_stats(stdscr):

    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_GREEN, curses.COLOR_BLACK)
    cyan = curses.color_pair(1)
    magenta = curses.color_pair(2)
    red = curses.color_pair(3)
    green = curses.color_pair(4)
    
 
    curses.curs_set(0)
    
    stdscr.clear()
    stdscr.addstr(1,8, 'Sightline NAS', cyan)
    stdscr.refresh()
    
    previous_io = get_disk_io(device_name)
    if not previous_io:
        stdscr.addstr(2, 8, f"Device {device_name} not found", red)
        stdscr.refresh()
        time.sleep(2)
        return
    
    while True:
        cpu = get_cpu_usage()
        ram = get_ram_usage()
        ipadd = get_ip_address()
        total_gb, used_gb, free_gb, perc_used = result
        current_io = get_disk_io(device_name)
        read_speed = (current_io.read_bytes - previous_io.read_bytes) / (1024 * 1024)
        write_speed = (current_io.write_bytes - previous_io.write_bytes) / (1024 * 1024)
        previous_io = current_io
        
        
        stdscr.move(2, 0)
        stdscr.clrtoeol()
        stdscr.move(3, 0)
        stdscr.clrtoeol()
        stdscr.move(4, 0)
        stdscr.clrtoeol()
        stdscr.move(5, 0)
        stdscr.clrtoeol()
        stdscr.move(6, 0)
        stdscr.clrtoeol()
        stdscr.move(7, 0)
        stdscr.clrtoeol()
        stdscr.move(8, 0)
        stdscr.clrtoeol()
        stdscr.move(9, 0)
        stdscr.clrtoeol()
        stdscr.move(10, 0)
        stdscr.clrtoeol()
        stdscr.move(11, 0)
        stdscr.clrtoeol()
        stdscr.move(12, 0)
        stdscr.clrtoeol()
        stdscr.move(13, 0)
        stdscr.clrtoeol()
    
        
        stdscr.addstr(3, 8, f'CPU Usage: {cpu}%', magenta)
        stdscr.addstr(4, 8, f'RAM Usage: {ram}%', magenta)
        stdscr.addstr(6, 8, f'Total Disk Space: {total_gb:.2f} TB', magenta)
        stdscr.addstr(7, 8, f'Used Disk Space: {used_gb:.1f} GB', magenta)
        stdscr.addstr(8, 8, f'Free Disk Space: {free_gb:.2f} TB', magenta)
        stdscr.addstr(9, 8, f'Percentage Disk used: {perc_used} %', magenta)
        stdscr.addstr(10, 8, f'Read Speed: {read_speed:.2f} mbps', magenta)
        stdscr.addstr(11,8, f'Write Speed: {write_speed:.2f} mbps', magenta)

        stdscr.addstr(13, 8, f'NAS IP: {ipadd}', green)
        stdscr.refresh()
        
        time.sleep(2)
        
if __name__ == "__main__":
    curses.wrapper(display_system_stats)
    
