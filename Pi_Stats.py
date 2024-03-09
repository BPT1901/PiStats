import psutil
import socket
import time
import curses


#define function to get CPU usage
def get_cpu_usage():
    return psutil.cpu_percent(interval=2)
#define function to get RAM usage
def get_ram_usage():
    return psutil.virtual_memory().percent
#define function to get HDD usage
def get_hdd_usage():
    disk_usage = psutil.disk_usage('/')
    total_gb = disk_usage.total / (1024 ** 3)
    used_gb = disk_usage.used / (1024 ** 3)
    free_gb = disk_usage.free / (1024 ** 3)
    perc_used = disk_usage.percent
    return total_gb, used_gb, free_gb, perc_used
#define function to get IP Address
def get_ip_address():
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    return ip
#Function for the blinking character
def switch_chars():
    char1 = ':)'
    char2 = ';)'
    while True:
        yield char1
        yield char2

#Main Function
def display_system_stats(stdscr):
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    cyan = curses.color_pair(1)
    magenta = curses.color_pair(2)
    red = curses.color_pair(3)
    yellow = curses.color_pair(4)
    
    char_switch = switch_chars()
    
    curses.curs_set(0)
    
    stdscr.clear()
    stdscr.addstr(0,30, 'NAS Pi in a box', cyan)
    stdscr.refresh()
    
    while True:
        cpu = get_cpu_usage()
        ram = get_ram_usage()
        ipadd = get_ip_address()
        total_gb, used_gb, free_gb, perc_used = get_hdd_usage()
        char = next(char_switch)
        
        stdscr.move(2, 0)
        stdscr.clrtoeol()
        stdscr.move(3, 0)
        stdscr.clrtoeol()
        stdscr.move(4, 0)
        stdscr.clrtoeol()
        
        stdscr.addstr(2, 30, f'CPU Usage: {cpu}%', magenta)
        stdscr.addstr(3, 30, f'RAM Usage: {ram}%', magenta)
        stdscr.addstr(5, 30, f'Total Disk Space: {total_gb:.1f} GB', magenta)
        stdscr.addstr(6, 30, f'Used Disk Space: {used_gb:.1f} GB', magenta)
        stdscr.addstr(7, 30, f'Free Disk Space: {free_gb:.1f} GB', magenta)
        stdscr.addstr(8, 30, f'Percentage Disk used: {perc_used} %', magenta)
        stdscr.addstr(10, 30, f'NAS IP: {ipadd}', yellow)
        stdscr.addstr(12, 30, f'BT Loves You {char}',red)
        stdscr.refresh()
        
        time.sleep(2)
        
if __name__ == "__main__":
    curses.wrapper(display_system_stats)