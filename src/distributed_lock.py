import redis
import time
import uuid
from typing import List, Optional


class RedisDistributedLock:
    def __init__(self, server: redis.Redis):
        self.server = server

    def acquire_lock(self, resource: str, ttl: int) -> Optional[str]:
        identifier = str(uuid.uuid4())
        end_time = int(time.time() * 1000) + ttl
        while int(time.time() * 1000) < end_time:
            if self.server.set(resource, identifier, nx=True, px=ttl):
                return identifier
            time.sleep(0.1)
        return None

    def _release_lock(self, resource: str, identifier: str) -> int:
        if self.server.get(resource) == identifier:
            self.server.delete(resource)
            return 1
        return 0


class RedLock:
    def __init__(self, servers: List[redis.Redis]):
        self.servers = servers

    @staticmethod
    def _acquire_lock(server: redis.Redis, resource: str, identifier: str, ttl: int) -> bool:
        if server.set(resource, identifier, nx=True, px=ttl):
            return True
        return False

    @staticmethod
    def _release_lock(server: redis.Redis, resource: str, identifier: str):
        if server.get(resource) == identifier:
            server.delete(resource)

    def acquire_lock(self, resource: str, ttl: int) -> Optional[str]:
        identifier = str(uuid.uuid4())
        end_time = int(time.time() * 1000 + ttl)  # convert to milliseconds
        while int(time.time() * 1000) < end_time:
            acquired_locks = 0
            for server in self.servers:
                if self._acquire_lock(server, resource, identifier, ttl):
                    acquired_locks += 1
            if acquired_locks >= len(self.servers) // 2 + 1:
                return identifier
            time.sleep(0.05)
        self.release_lock(resource, identifier)
        return None

    def release_lock(self, resource: str, identifier: str):
        for server in self.servers:
            self._release_lock(server, resource, identifier)
