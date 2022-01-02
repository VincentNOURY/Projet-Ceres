MODE = 'debug' # Available modes debug, info, errors only

def log(mode: str, message):
    if mode == 'debug' and MODE == 'debug':
        print("[Debug]", message)
    elif mode == 'info' and MODE in ['debug', 'info']:
        print("[Info]", message)
    elif mode == 'error' and MODE in ['debug', 'info', 'error only']:
        print("[Error]", message)
    else:
        print("[Error] Debug mode not recognised.")
        raise
