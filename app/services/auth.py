from datetime import (
    datetime,
    timedelta,
)

from jose import (
    jwt,
    JWTError,
)
from fastapi import (
    Depends,
    status,
)
from fastapi.security import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm,
)
from passlib.context import CryptContext

from app.backend.config import config
from app.const import (
    TOKEN_ALGORITHM,
    TOKEN_EXPIRE_MINUTES,
    TOKEN_TYPE,
    AUTH_URL,
)
from app.exc import raise_with_log
from app.models.auth import UserModel
from app.schemas.auth import (
    CreateUserSchema,
    TokenSchema,
    UserSchema,
)
from app.services.base import (
    AppCRUD,
    AppService,
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_schema = OAuth2PasswordBearer(tokenUrl=AUTH_URL, auto_error=False)


async def get_current_user(token: str = Depends(oauth2_schema)) -> UserSchema | None:
    """Decode token to obtain user information.

    It extracts user information from token and verifies expiration time.
    If token is valid instance :class:`~app.schemas.auth.UserSchema` is returned,
    otherwise the corresponding exception is raised.

    Args:
        token:
            The token to verify.

    Returns:
        Decoded user dictionary.
    """

    if not token:
        raise_with_log(status.HTTP_401_UNAUTHORIZED, "Invalid token")

    try:
        # decode token using secret token key provided by config
        payload = jwt.decode(token, config.token_key, algorithms=[TOKEN_ALGORITHM])

        # extract encoded information
        name: int = payload.get("name")
        sub: str = payload.get("sub")
        expires_at: str = payload.get("expires_at")

        if sub is None:
            raise_with_log(status.HTTP_401_UNAUTHORIZED, "Invalid credentials")

        if is_expired(expires_at):
            raise_with_log(status.HTTP_401_UNAUTHORIZED, "Token expired")

        return UserSchema(name=name, email=sub)
    except JWTError:
        raise_with_log(status.HTTP_401_UNAUTHORIZED, "Invalid credentials")

    return None


def is_expired(expires_at: str) -> bool:
    """Return :obj:`True` if token has expired."""

    return datetime.strptime(expires_at, "%Y-%m-%d %H:%M:%S") < datetime.utcnow()


class AuthService(AppService):
    """Authentication service."""

    def create_user(self, user: CreateUserSchema) -> None:
        """Add user with hashed password to database."""

        AuthCRUD(self.db).add_user(user)

    def authenticate(
        self, login: OAuth2PasswordRequestForm = Depends()
    ) -> TokenSchema | None:
        """Generate token.

        It obtains username and password and verifies password vs
        hashed password stored in database. If valid then temporary
        token is generated, otherwise the corresponding exception is raised.
        """

        user = AuthCRUD(self.db).get_user(login.username)

        if not user:
            raise_with_log(status.HTTP_404_NOT_FOUND, "User not found")
        else:
            if not user.hashed_password:
                raise_with_log(status.HTTP_401_UNAUTHORIZED, "Incorrect password")

            if not Hasher.verify(user.hashed_password, login.password):
                raise_with_log(status.HTTP_401_UNAUTHORIZED, "Incorrect password")

            access_token = self._create_access_token(user.name, user.email)

            return TokenSchema(access_token=access_token, token_type=TOKEN_TYPE)

        return None

    def _create_access_token(self, name: str, email: str) -> str:
        """Encode user information and expiration time."""

        payload = {
            "name": name,
            "sub": email,
            "expires_at": self._expiration_time(),
        }

        return jwt.encode(payload, config.token_key, algorithm=TOKEN_ALGORITHM)

    @staticmethod
    def _expiration_time() -> str:
        """Generate token expiration time."""

        expires_at = datetime.utcnow() + timedelta(minutes=TOKEN_EXPIRE_MINUTES)
        return expires_at.strftime("%Y-%m-%d %H:%M:%S")


class AuthCRUD(AppCRUD):
    def add_user(self, user: CreateUserSchema) -> None:
        """Hash user password and write it to database."""

        user = UserModel(
            name=user.name,
            email=user.email,
            hashed_password=Hasher.bcrypt(user.password),
        )

        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

    def get_user(self, email: str) -> UserSchema:
        """Read user from database."""

        return UserSchema.from_orm(self.query(UserModel, email=email).first())


class Hasher:
    """Hashing and verifying passwords."""

    @staticmethod
    def bcrypt(password: str) -> str:
        """Generate a bcrypt hashed password.

        Args:
            password:
                The password to hash.

        Returns:
            The hashed password
        """

        return pwd_context.hash(password)

    @staticmethod
    def verify(hashed_password: str, plain_password: str) -> bool:
        """Verify a password against a hash.

        Args:
            hashed_password:
                The hashed password.
            plain_password:
                The plain password.

        Returns:
            True if the password matches, False otherwise.
        """

        return pwd_context.verify(plain_password, hashed_password)
