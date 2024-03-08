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
    stdscr.clear()
    stdscr.addstr(0,0, 'NAS Pi in a box', curses.A_BOLD)
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
        
        stdscr.addstr(2, 0, f'CPU Usage: {cpu}%')
        stdscr.addstr(3, 0, f'RAM Usage: {ram}%')
        #print(f'Hard Disks: {hdd}%')
        stdscr.addstr(4, 0, f'NAS IP: {ip}')
        stdscr.addstr(6, 0, 'BT Loves You ;)')
        stdscr.refresh()
        
        
        time.sleep(3)
        
if __name__ == "__main__":
    curses.wrapper(display_system_stats)