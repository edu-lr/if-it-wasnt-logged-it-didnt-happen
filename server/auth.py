# auth.py
# Maneja la validación de tokens de autenticación.
# Cada request debe incluir un token válido en el header Authorization.

from tokens import VALID_TOKENS

def validate_token(authorization: str):
    """
    Recibe el header Authorization completo: 'Token svc-auth-001'
    Devuelve el nombre del servicio si el token es válido.
    Devuelve None si el token no existe o el header tiene formato incorrecto.
    """

    # Verifica que el header exista y tenga el formato correcto
    if not authorization or not authorization.startswith("Token "):
        return None

    # Extrae el token del header, separando por espacio
    # Ejemplo: "Token svc-auth-001" → ["Token", "svc-auth-001"] → "svc-auth-001"
    token = authorization.split(" ")[1]

    # Busca el token en el diccionario de tokens válidos
    # Si existe devuelve el nombre del servicio, si no devuelve None
    return VALID_TOKENS.get(token)