from functools import wraps

def notificacion(mensaje: str):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Usa los argumentos nombrados para formatear el mensaje
            try:
                print("Notificación:", mensaje.format(*args, **kwargs))
            except Exception as e:
                print(f"[ERROR en notificación]: {e}")
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
