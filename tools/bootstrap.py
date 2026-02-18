# Stub bootstrap module for tests
called = False

def run():
    global called
    called = True
    print("bootstrap.run executed")
