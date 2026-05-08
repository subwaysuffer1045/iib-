import redis

def check_redis():
    try:
        r = redis.from_url("redis://localhost:6379/0")
        r.ping()
        print("Successfully connected to Redis!")
    except Exception as e:
        print(f"Failed to connect to Redis: {e}")

if __name__ == "__main__":
    check_redis()
