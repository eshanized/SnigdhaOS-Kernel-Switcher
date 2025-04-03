import psutil
import time

def get_cpu_usage():
    """Get the current CPU usage percentage."""
    return psutil.cpu_percent(interval=1)

def get_memory_usage():
    """Get the current memory usage percentage."""
    memory = psutil.virtual_memory()
    return memory.percent

def get_disk_usage(mount_point='/'):
    """Get the current disk usage percentage for a specific mount point."""
    disk = psutil.disk_usage(mount_point)
    return disk.percent

def get_network_io():
    """Get network I/O statistics."""
    io = psutil.net_io_counters()
    return {
        'bytes_sent': io.bytes_sent,
        'bytes_recv': io.bytes_recv,
        'packets_sent': io.packets_sent,
        'packets_recv': io.packets_recv,
        'errin': io.errin,
        'errout': io.errout,
        'dropin': io.dropin,
        'dropout': io.dropout
    }

def monitor_system(interval=5):
    """Monitor the system at regular intervals and print the results."""
    try:
        while True:
            print(f"CPU Usage: {get_cpu_usage()}%")
            print(f"Memory Usage: {get_memory_usage()}%")
            print(f"Disk Usage: {get_disk_usage()}%")
            print(f"Network I/O: {get_network_io()}")
            print("-" * 40)
            time.sleep(interval)
    except KeyboardInterrupt:
        print("Monitoring stopped.")

if __name__ == "__main__":
    monitor_system()