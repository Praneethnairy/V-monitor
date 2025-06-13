import docker
from logger import get_logger
import json
import os
import sys

class ContainerMonitor:
    def __init__(self):
        # Get the directory of the current script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        # Change to the script directory to ensure relative paths work
        os.chdir(script_dir)
        self.client = docker.from_env()
        self.logger = get_logger(__name__)

    def get_running_containers(self):
        return self.client.containers.list()

    def get_container_stats(self, container):
        try:
            stats = container.stats(stream=False)
            self.logger.info(f"Container {container.name} stats: {stats}")
            return {
                "id": container.id,
                "name": container.name,
                "cpu_percent": self._calculate_cpu_percent(stats),
                "memory_usage": stats["memory_stats"]["usage"],
                "memory_limit": stats["memory_stats"]["limit"],
                "network_io": stats.get("networks", {}),
            }
        except Exception as e:
            self.logger.error(f"Error getting container stats: {e}")
            return {}

    def _calculate_cpu_percent(self, stats):
        try:
            cpu_delta = stats["cpu_stats"]["cpu_usage"]["total_usage"] - stats["precpu_stats"]["cpu_usage"]["total_usage"]
            system_delta = stats["cpu_stats"]["system_cpu_usage"] - stats["precpu_stats"]["system_cpu_usage"]
            if system_delta > 0.0 and cpu_delta > 0.0:
                return (cpu_delta / system_delta) * len(stats["cpu_stats"]["cpu_usage"].get("percpu_usage", [1])) * 100.0
            return 0.0
        except Exception as e:
            self.logger.error(f"Error calculating CPU percent: {e}")
            return 0.0

    def get_all_containers_stats(self):
        try:
            containers = self.get_running_containers()
            self.logger.info(f"Found {len(containers)} running containers!!")
            return [self.get_container_stats(container) for container in containers]
        except Exception as e:
            self.logger.error(f"Error getting container stats: {e}")
            return []

if __name__ == "__main__":
    try:
        monitor = ContainerMonitor()
        result = monitor.get_all_containers_stats()
        print(json.dumps(result))
    except Exception as e:
        print(json.dumps({"error": str(e)}), file=sys.stderr)
        sys.exit(1)
