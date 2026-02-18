# Stub episode_gen for tests
last_args = None

def generate(season, episode):
    global last_args
    last_args = (season, episode)
    print(f"episode_gen.generate executed: {season} {episode}")
