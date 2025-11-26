"""
JWT Token Handler

Genera y verifica JSON Web Tokens para autenticación.
"""

from datetime import datetime, timedelta
from typing import Dict, Optional
import jwt


class JWTHandler:
    """
    Manejador de JSON Web Tokens

    Crea y verifica tokens JWT para autenticación.
    """

    def __init__(
        self,
        secret_key: str = "your-secret-key-change-in-production",
        algorithm: str = "HS256",
        expiration_minutes: int = 60 * 24,  # 24 horas
    ):
        """
        Inicializa el manejador de JWT

        Args:
            secret_key: Clave secreta para firmar tokens
            algorithm: Algoritmo de encriptación
            expiration_minutes: Tiempo de expiración en minutos
        """
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.expiration_minutes = expiration_minutes

    def create_access_token(self, data: Dict) -> str:
        """
        Crea un token de acceso JWT

        Args:
            data: Datos a incluir en el token (payload)

        Returns:
            Token JWT como string
        """
        to_encode = data.copy()

        # Agregar tiempo de expiración
        expire = datetime.utcnow() + timedelta(minutes=self.expiration_minutes)
        to_encode.update({"exp": expire, "iat": datetime.utcnow()})

        # Generar token
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt

    def verify_token(self, token: str) -> Optional[Dict]:
        """
        Verifica y decodifica un token JWT

        Args:
            token: Token JWT a verificar

        Returns:
            Payload del token si es válido, None si es inválido
        """
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None

    def decode_token(self, token: str) -> Optional[Dict]:
        """
        Decodifica un token sin verificar (útil para debugging)

        Args:
            token: Token JWT

        Returns:
            Payload decodificado
        """
        try:
            return jwt.decode(token, options={"verify_signature": False})
        except Exception:
            return None
