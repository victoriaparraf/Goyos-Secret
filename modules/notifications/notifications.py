from functools import wraps

YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"

def notificacion(mensaje: str, data_extractor=None):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            try:
                if data_extractor:
                    notification_data = data_extractor(result)
                    print(f"{YELLOW}Notificación: {RESET}{mensaje.format(**notification_data)}")
                else:
                    print(f"{YELLOW}Notificación: {RESET}{mensaje.format(*args, **kwargs)}")
            except Exception as e:
                print(f"{RED}[ERROR en notificación]: {e}{RESET}")
            return result
        return wrapper
    return decorator

@notificacion("Pre-orden con {n_platos} platos.")
def registrar_preorden(n_platos):
    pass