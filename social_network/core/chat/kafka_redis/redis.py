from redis import StrictRedis


def create_redis_connection() -> StrictRedis:
    return StrictRedis(
        host="localhost",
        port=6379,
        db=0,
    )
