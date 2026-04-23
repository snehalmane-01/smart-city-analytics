from dataclasses import dataclass


@dataclass(frozen=True)
class DatabaseConfig:
    postgres_url: str
    mongodb_url: str
    timescaledb_url: str
    redis_url: str
