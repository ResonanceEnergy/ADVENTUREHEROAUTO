# Stub imagine_api for tests
last_args = None

def run_batch(season, episode):
    global last_args
    last_args = (season, episode)
    print(f"imagine_api.run_batch executed: {season} {episode}")
