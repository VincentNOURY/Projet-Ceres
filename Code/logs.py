#MODE = 'debug' # Available modes debug, info, errors only
MODE = 'info'

def log(mode: str, message):
    if mode == 'debug':
        if MODE == 'debug':
            print("[Debug]", message)
    elif mode == 'info':
        if MODE in ['debug', 'info']:
            print("[Info]", message)
    elif mode == 'error':
        if MODE in ['debug', 'info', 'error only']:
            print("[Error]", message)
    else:
        print(f"[Error] Debug mode not recognised : {mode}.")
        raise
