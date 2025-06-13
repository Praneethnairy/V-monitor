import psutil
from logger import get_logger
import json
import os
import sys

class HostMonitor:
    def __init__(self):
        # Get the directory of the current script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        # Change to the script directory to ensure relative paths work
        os.chdir(script_dir)
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
            io_stats = psutil.disk_io_counters()
            return {
                "read_count": io_stats.read_count,
                "write_count": io_stats.write_count,
                "read_bytes": io_stats.read_bytes,
                "write_bytes": io_stats.write_bytes,
                "read_time": io_stats.read_time,
                "write_time": io_stats.write_time,
                "read_merged_count": io_stats.read_merged_count,
                "write_merged_count": io_stats.write_merged_count,
                "busy_time": io_stats.busy_time
            }
        except Exception as e:
            self.logger.error(f"Error getting IO counters: {e}")
            return {}

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

if __name__ == "__main__":
    try:
        monitor = HostMonitor()
        result = monitor.get_all_details()
        print(json.dumps(result))
    except Exception as e:
        print(json.dumps({"error": str(e)}), file=sys.stderr)
        sys.exit(1)
