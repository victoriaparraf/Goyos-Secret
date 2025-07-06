from functools import wraps

YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"

def notificacion(mensaje: str):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                print(f"{YELLOW}Notificación: {RESET}{mensaje.format(*args, **kwargs)}")
            except Exception as e:
                print(f"{RED}[ERROR en notificación]: {e}{RESET}")
            return func(*args, **kwargs)
        return wrapper
    return decorator


@notificacion("Reserva confirmada para {fecha} en {restaurante}.")
def crear_reserva(fecha, restaurante):
    pass

@notificacion("Reserva cancelada (ID: {id_reserva}).")
def cancelar_reserva(id_reserva):
    pass

@notificacion("Pre-orden con {n_platos} platos.")
def registrar_preorden(n_platos):
    pass

# Ejemplo de llamadas:
crear_reserva(fecha="2024-07-07", restaurante="Goyo's")
cancelar_reserva(id_reserva="12345")
registrar_preorden(n_platos=4)