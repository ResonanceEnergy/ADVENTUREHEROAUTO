# Stub asset_tools for tests
last_args = None

def postprocess(season, episode):
    global last_args
    last_args = (season, episode)
    print(f"asset_tools.postprocess executed: {season} {episode}")
