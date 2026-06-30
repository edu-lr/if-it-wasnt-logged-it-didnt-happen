from tokens import VALID_TOKENS

def validate_token(authorization: str):
    
    # Recibe el header Authorization completo: 'Token svc-auth-001'
    # Devuelve el nombre del servicio si es válido, None si no lo es.
    
    if not authorization or not authorization.startswith("Token "):
        return None
    
    token = authorization.split(" ")[1]  # Extrae el token del header
    return VALID_TOKENS.get(token)       # Devuelve el servicio o NoneFD