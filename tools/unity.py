# Stub unity for tests
called = False

def build_ios():
    global called
    called = True
    print("unity.build_ios executed")
