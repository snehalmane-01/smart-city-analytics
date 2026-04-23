from __future__ import annotations

from dataclasses import dataclass, field
from time import time


@dataclass
class RateLimiter:
    requests_per_minute: int
    _bucket: dict[str, list[float]] = field(default_factory=dict)

    def allow(self, identity: str) -> bool:
        now = time()
        timestamps = self._bucket.setdefault(identity, [])
        one_minute_ago = now - 60
        timestamps[:] = [ts for ts in timestamps if ts >= one_minute_ago]
        if len(timestamps) >= self.requests_per_minute:
            return False
        timestamps.append(now)
        return True


def has_role(user_roles: set[str], required_role: str) -> bool:
    return required_role in user_roles
