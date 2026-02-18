# Stub artbrief_gen for tests
last_args = None

def generate(season, episode):
    global last_args
    last_args = (season, episode)
    print(f"artbrief_gen.generate executed: {season} {episode}")
