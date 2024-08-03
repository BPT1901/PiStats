import psutil
import socket
import time
import curses

FONT_SIZE_20 = '\033[20m'
FONT_SIZE_RESET = '\033[0m'

#define function to get CPU usage
def get_cpu_usage():
    return psutil.cpu_percent(interval=2)
#define function to get RAM usage
def get_ram_usage():
    return psutil.virtual_memory().percent
#define function to get HDD usage
def get_hdd_usage():
    disk_usage = psutil.disk_usage('/srv/dev-disk-by-uuid-84f11321-c167-421a-b1ad-6a8c22395c66')
    total_gb = disk_usage.total / (1024 ** 3)
    used_gb = disk_usage.used / (1024 ** 3)
    free_gb = disk_usage.free / (1024 ** 3)
    perc_used = disk_usage.percent
    return total_gb, used_gb, free_gb, perc_used

#define HDD read and write speeds
def hdd_speeds(interval=1):
    disk_io_start = psutil.disk_io_counters(perdisk=True)
    
    time.sleep(interval)
    
    disk_io_end = psutil.disk_io_counters(perdisk=True)
    
    speeds = {}
    for disk in disk_io_start.keys():
        read_speed = (disk_io_end[disk].read_bytes - disk_io_start[disk].read_bytes) / interval
        write_speed = (disk_io_end[disk].write_bytes - disk_io_start[disk].write_bytes) / interval
        speeds[disk] = (read_speed, write_speed)
    return speeds

#define function to get IP Address
def get_ip_address():
   # hostname = socket.gethostname()
   # ip = socket.gethostbyname(hostname)

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))

    ip = s.getsockname()[0]
    return ip
#Function for the blinking character
def switch_chars():
    char1 = ':)'
    char2 = ':x'
    while True:
        yield char1
        yield char2

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
    
    char_switch = switch_chars()
    
    curses.curs_set(0)
    
    stdscr.clear()
    stdscr.addstr(1,8, 'NAS PI IN A BOX', cyan)
    stdscr.refresh()
    
    while True:
        cpu = get_cpu_usage()
        ram = get_ram_usage()
        ipadd = get_ip_address()
        total_gb, used_gb, free_gb, perc_used = get_hdd_usage()
        hdd_read_write_speeds = hdd_speeds()
        char = next(char_switch)
        
        stdscr.move(2, 0)
        stdscr.clrtoeol()
        stdscr.move(3, 0)
        stdscr.clrtoeol()
        stdscr.move(4, 0)
        stdscr.clrtoeol()
    
        
        stdscr.addstr(3, 8, f'CPU Usage: {cpu}%', magenta)
        stdscr.addstr(4, 8, f'RAM Usage: {ram}%', magenta)
        stdscr.addstr(6, 8, f'Total Disk Space: {total_gb:.2f} TB', magenta)
        stdscr.addstr(7, 8, f'Used Disk Space: {used_gb:.1f} GB', magenta)
        stdscr.addstr(8, 8, f'Free Disk Space: {free_gb:.2f} TB', magenta)
        stdscr.addstr(9, 8, f'Percentage Disk used: {perc_used} %', magenta)
        stdscr.addstr(10,8, f'HDD speeds: {hdd_read_write_speeds}', magenta)
        #stdscr.addstr(11,8, f'HDD write speed: {write_speed}', magenta)
        stdscr.addstr(12, 8, f'NAS IP: {ipadd}', green)
        #stdscr.addstr(13, 8, f'BT Loves You {char}',red)
        stdscr.refresh()
        
        time.sleep(2)
        
if __name__ == "__main__":
    curses.wrapper(display_system_stats)
