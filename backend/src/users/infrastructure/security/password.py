"""
Password Hashing Utility

Utiliza bcrypt para hashear y verificar passwords de forma segura.
"""

import bcrypt


class PasswordHasher:
    """
    Utilidad para hashear y verificar passwords

    Utiliza bcrypt con salt automático para seguridad.
    """

    def hash(self, password: str) -> str:
        """
        Hashea un password

        Args:
            password: Password en texto plano

        Returns:
            Password hasheado
        """
        # Generar salt y hashear
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
        return hashed.decode("utf-8")

    def verify(self, password: str, hashed_password: str) -> bool:
        """
        Verifica un password contra su hash

        Args:
            password: Password en texto plano
            hashed_password: Hash del password

        Returns:
            True si el password es correcto
        """
        try:
            return bcrypt.checkpw(
                password.encode("utf-8"), hashed_password.encode("utf-8")
            )
        except Exception:
            return False
