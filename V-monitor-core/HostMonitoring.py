import psutil
from logger import get_logger

class HostMonitor:
    def __init__(self):
        self.logger = get_logger(__name__)

    def get_cpu_usage(self):
        try:
            return psutil.cpu_percent(interval=1)
        except Exception as e:
            self.logger.error(f"Error getting CPU usage: {e}")
            return 0.0
    
    def get_memory_usage(self):
        try:
            return psutil.virtual_memory().percent
        except Exception as e:
            self.logger.error(f"Error getting memory usage: {e}")
            return 0.0
    
    def get_disk_usage(self):
        try:
            return psutil.disk_usage('/').percent
        except Exception as e:
            self.logger.error(f"Error getting disk usage: {e}")
            return 0.0

    def get_io_counters(self):
        try:
            return psutil.disk_io_counters()
        except Exception as e:
            self.logger.error(f"Error getting IO counters: {e}")
            return 0.0

    def get_all_details(self):
        try:
            data_t = {
                "cpu_usage": self.get_cpu_usage(),
                "memory_usage": self.get_memory_usage(),
                "disk_usage": self.get_disk_usage(),
                "io_counters": self.get_io_counters()
            }
            self.logger.info(f"Host details: {data_t}")
            return data_t
        except Exception as e:
            self.logger.error(f"Error getting all details: {e}")
            return {}

# if __name__ == "__main__":
#     logger = get_logger(__name__)
#     monitor = HostMonitor()
#     for i in range(100):
#         logger.info(monitor.get_all_details())
#         time.sleep(1)