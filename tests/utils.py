import asyncio
import contextlib
import functools
import math
import time
from typing import Optional

import pytest


def fixed_start(fn):
    @functools.wraps(fn)
    def __inner(*a, **k):
        start = time.time()

        while time.time() < math.ceil(start):
            time.sleep(0.01)

        return fn(*a, **k)

    return __inner


def async_fixed_start(fn):
    @functools.wraps(fn)
    async def __inner(*a, **k):
        start = time.time()

        while time.time() < math.ceil(start):
            await asyncio.sleep(0.01)

        return await fn(*a, **k)

    return __inner


@contextlib.contextmanager
def window(delay_end: float, delay: Optional[float] = None):
    start = time.time()

    if delay is not None:
        while time.time() - start < delay:
            time.sleep(0.001)
    yield (int(start), int(start + delay_end))

    while time.time() - start < delay_end:
        time.sleep(0.001)


@contextlib.asynccontextmanager
async def async_window(delay_end: float, delay: Optional[float] = None):
    start = time.time()

    if delay is not None:
        while time.time() - start < delay:
            await asyncio.sleep(0.001)

    yield (int(start), int(start + delay_end))

    while time.time() - start < delay_end:
        await asyncio.sleep(0.001)


all_storage = pytest.mark.parametrize(
    "uri, args, fixture",
    [
        pytest.param("memory://", {}, None, id="in-memory"),
        pytest.param(
            "redis://localhost:7379",
            {},
            pytest.lazy_fixtures("redis_basic"),
            marks=pytest.mark.redis,
            id="redis_basic",
        ),
        pytest.param(
            "memcached://localhost:22122",
            {},
            pytest.lazy_fixtures("memcached"),
            marks=[pytest.mark.memcached, pytest.mark.flaky],
            id="memcached",
        ),
        pytest.param(
            "memcached://localhost:22122,localhost:22123",
            {},
            pytest.lazy_fixtures("memcached_cluster"),
            marks=[pytest.mark.memcached, pytest.mark.flaky],
            id="memcached-cluster",
        ),
        pytest.param(
            "redis+cluster://localhost:7001/",
            {},
            pytest.lazy_fixtures("redis_cluster"),
            marks=pytest.mark.redis_cluster,
            id="redis-cluster",
        ),
        pytest.param(
            "redis+cluster://:sekret@localhost:8400/",
            {},
            pytest.lazy_fixtures("redis_auth_cluster"),
            marks=pytest.mark.redis_cluster,
            id="redis-cluster-auth",
        ),
        pytest.param(
            "redis+cluster://localhost:8301",
            {
                "ssl": True,
                "ssl_cert_reqs": "required",
                "ssl_keyfile": "./tests/tls/client.key",
                "ssl_certfile": "./tests/tls/client.crt",
                "ssl_ca_certs": "./tests/tls/ca.crt",
            },
            pytest.lazy_fixtures("redis_ssl_cluster"),
            marks=pytest.mark.redis_cluster,
            id="redis-ssl-cluster",
        ),
        pytest.param(
            "redis+sentinel://localhost:26379/mymaster",
            {"use_replicas": False},
            pytest.lazy_fixtures("redis_sentinel"),
            marks=pytest.mark.redis_sentinel,
            id="redis-sentinel",
        ),
        pytest.param(
            "mongodb://localhost:37017/",
            {},
            pytest.lazy_fixtures("mongodb"),
            marks=pytest.mark.mongodb,
            id="mongodb",
        ),
        pytest.param(
            "etcd://localhost:2379",
            {},
            pytest.lazy_fixtures("etcd"),
            marks=[pytest.mark.etcd, pytest.mark.flaky],
            id="etcd",
        ),
    ],
)

moving_window_storage = pytest.mark.parametrize(
    "uri, args, fixture",
    [
        pytest.param("memory://", {}, None, id="in-memory"),
        pytest.param(
            "redis://localhost:7379",
            {},
            pytest.lazy_fixtures("redis_basic"),
            marks=pytest.mark.redis,
            id="redis",
        ),
        pytest.param(
            "redis+cluster://localhost:7001/",
            {},
            pytest.lazy_fixtures("redis_cluster"),
            marks=pytest.mark.redis_cluster,
            id="redis-cluster",
        ),
        pytest.param(
            "redis+cluster://:sekret@localhost:8400/",
            {},
            pytest.lazy_fixtures("redis_auth_cluster"),
            marks=pytest.mark.redis_cluster,
            id="redis-cluster-auth",
        ),
        pytest.param(
            "redis+cluster://localhost:8301",
            {
                "ssl": True,
                "ssl_cert_reqs": "required",
                "ssl_keyfile": "./tests/tls/client.key",
                "ssl_certfile": "./tests/tls/client.crt",
                "ssl_ca_certs": "./tests/tls/ca.crt",
            },
            pytest.lazy_fixtures("redis_ssl_cluster"),
            marks=pytest.mark.redis_cluster,
            id="redis-ssl-cluster",
        ),
        pytest.param(
            "redis+sentinel://localhost:26379/mymaster",
            {"use_replicas": False},
            pytest.lazy_fixtures("redis_sentinel"),
            marks=pytest.mark.redis_sentinel,
            id="redis-sentinel",
        ),
        pytest.param(
            "mongodb://localhost:37017/",
            {},
            pytest.lazy_fixtures("mongodb"),
            marks=pytest.mark.mongodb,
            id="mongodb",
        ),
    ],
)

async_all_storage = pytest.mark.parametrize(
    "uri, args, fixture",
    [
        pytest.param("async+memory://", {}, None, id="in-memory"),
        pytest.param(
            "async+redis://localhost:7379",
            {},
            pytest.lazy_fixtures("redis_basic"),
            marks=pytest.mark.redis,
            id="redis",
        ),
        pytest.param(
            "async+memcached://localhost:22122",
            {},
            pytest.lazy_fixtures("memcached"),
            marks=[pytest.mark.memcached, pytest.mark.flaky],
            id="memcached",
        ),
        pytest.param(
            "async+memcached://localhost:22122,localhost:22123",
            {},
            pytest.lazy_fixtures("memcached_cluster"),
            marks=[pytest.mark.memcached, pytest.mark.flaky],
            id="memcached-cluster",
        ),
        pytest.param(
            "async+redis+cluster://localhost:7001/",
            {},
            pytest.lazy_fixtures("redis_cluster"),
            marks=pytest.mark.redis_cluster,
            id="redis-cluster",
        ),
        pytest.param(
            "async+redis+cluster://:sekret@localhost:8400/",
            {},
            pytest.lazy_fixtures("redis_auth_cluster"),
            marks=pytest.mark.redis_cluster,
            id="redis-cluster-auth",
        ),
        pytest.param(
            "async+redis+cluster://localhost:8301",
            {
                "ssl": True,
                "ssl_cert_reqs": "required",
                "ssl_keyfile": "./tests/tls/client.key",
                "ssl_certfile": "./tests/tls/client.crt",
                "ssl_ca_certs": "./tests/tls/ca.crt",
            },
            pytest.lazy_fixtures("redis_ssl_cluster"),
            marks=pytest.mark.redis_cluster,
            id="redis-ssl-cluster",
        ),
        pytest.param(
            "async+redis+sentinel://localhost:26379/mymaster",
            {"use_replicas": False},
            pytest.lazy_fixtures("redis_sentinel"),
            marks=pytest.mark.redis_sentinel,
            id="redis-sentinel",
        ),
        pytest.param(
            "async+mongodb://localhost:37017/",
            {},
            pytest.lazy_fixtures("mongodb"),
            marks=pytest.mark.mongodb,
            id="mongodb",
        ),
        pytest.param(
            "async+etcd://localhost:2379",
            {},
            pytest.lazy_fixtures("etcd"),
            marks=[pytest.mark.etcd, pytest.mark.flaky],
            id="etcd",
        ),
    ],
)

async_moving_window_storage = pytest.mark.parametrize(
    "uri, args, fixture",
    [
        pytest.param("async+memory://", {}, None, id="in-memory"),
        pytest.param(
            "async+redis://localhost:7379",
            {},
            pytest.lazy_fixtures("redis_basic"),
            marks=pytest.mark.redis,
            id="redis",
        ),
        pytest.param(
            "async+redis+cluster://localhost:7001/",
            {},
            pytest.lazy_fixtures("redis_cluster"),
            marks=pytest.mark.redis_cluster,
            id="redis-cluster",
        ),
        pytest.param(
            "async+redis+cluster://:sekret@localhost:8400/",
            {},
            pytest.lazy_fixtures("redis_auth_cluster"),
            marks=pytest.mark.redis_cluster,
            id="redis-cluster-auth",
        ),
        pytest.param(
            "async+redis+cluster://localhost:8301",
            {
                "ssl": True,
                "ssl_cert_reqs": "required",
                "ssl_keyfile": "./tests/tls/client.key",
                "ssl_certfile": "./tests/tls/client.crt",
                "ssl_ca_certs": "./tests/tls/ca.crt",
            },
            pytest.lazy_fixtures("redis_ssl_cluster"),
            marks=pytest.mark.redis_cluster,
            id="redis-ssl-cluster",
        ),
        pytest.param(
            "async+redis+sentinel://localhost:26379/mymaster",
            {"use_replicas": False},
            pytest.lazy_fixtures("redis_sentinel"),
            marks=pytest.mark.redis_sentinel,
            id="redis-sentinel",
        ),
        pytest.param(
            "async+mongodb://localhost:37017/",
            {},
            pytest.lazy_fixtures("mongodb"),
            marks=pytest.mark.mongodb,
            id="mongodb",
        ),
    ],
)
