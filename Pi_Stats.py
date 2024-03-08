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
#def get_hdd_usage():
    #return psutil.disk_usage('Macintosh HD')
#define function to get IP Address
def get_ip_address():
    return socket.gethostbyname(socket.gethostname())


#Main Function
def display_system_stats(stdscr):
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
    cyan = curses.color_pair(1)
    magenta = curses.color_pair(2)
    red = curses.color_pair(3)
    
    stdscr.clear()
    stdscr.addstr(0,30, 'NAS Pi in a box', cyan)
    stdscr.refresh()
    
    while True:
        cpu = get_cpu_usage()
        ram = get_ram_usage()
        #hdd = get_hdd_usage()
        ip = get_ip_address()
        
        stdscr.move(2, 0)
        stdscr.clrtoeol()
        stdscr.move(3, 0)
        stdscr.clrtoeol()
        stdscr.move(4, 0)
        stdscr.clrtoeol()
        
        #stdscr.addstr(2, 20, f"CPU Usage: {get_cpu_usage()}%", magenta)
        stdscr.addstr(2, 30, f'CPU Usage: {cpu}%', magenta)
        stdscr.addstr(4, 30, f'RAM Usage: {ram}%', magenta)
        #print(f'Hard Disks: {hdd}%')
        stdscr.addstr(6, 30, f'NAS IP: {ip}', magenta)
        stdscr.addstr(8, 30, 'BT Loves You ;)',red)
        stdscr.refresh()
        
        
        time.sleep(3)
        
if __name__ == "__main__":
    curses.wrapper(display_system_stats)