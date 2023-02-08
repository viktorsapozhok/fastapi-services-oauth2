# fastapi-services-oauth2

This repository provides an approach on how to structure FastAPI application with 
multiple services, simple OAuth2 authentication, and Postgres backend.

## Structure overview

Application consists of 4 packages which provide service related functionality: 
`routers`, `services`, `schemas`, and `models`. Adding a new service requires 
adding a new module in each of these packages. 

Package `backend` provides database session manager and configs. In case, application 
communicates not only with database, but also with other backends (e.g. other API), 
the corresponding clients can be placed in `backend`.

```bash
    .
    └── app/
        ├── backend             # Backend functionality and configs
        |   ├── config.py           # Configuration settings
        │   └── database.py         # Database session manager
        ├── models              # SQLAlchemy models
        │   ├── auth.py             # Authentication models
        |   ├── base.py             # Base classes, mixins
        |   └── ...                 # Service models
        ├── routers             # API routes
        |   ├── auth.py             # Authentication routers
        │   └── ...                 # Service routers
        ├── schemas             # Pydantic models
        |   ├── auth.py              
        │   └── ...
        ├── services            # Business logic
        |   ├── auth.py             # Create user, generate and verify tokens
        |   ├── base.py             # Base classes, mixins
        │   └── ...
        ├── cli.py              # Command-line utilities
        ├── const.py            # Constants
        ├── exc.py              # Exception handlers
        └── main.py             # Application runner
```

Module `cli` provides command-line functionality related to API services but not required
access through API endpoints. It's main focus is to complete tasks that need to be done 
manually or by scheduler. For instance, create a new user and store its hashed data in database.

Module `main` represents FastAPI entry point and initiates `app` object (instance of `FastAPI` class).
This `app` is referred by server when running `uvicorn main:app` command.

## Adding a new service

To illustrate the proposed structure, let's create a simple service reading data from
postgres backend and sending it back to user. 

### Backend setup

First, we create a database schema called `myapi` and table `movies` in there. In this table,
we insert list of records with following fields: `movie_id`, `title`, `released` (release year) and 
`rating` (e.g. imdb rating).

```sql
CREATE SCHEMA IF NOT EXISTS myapi;

CREATE TABLE IF NOT EXISTS myapi.movies (
    movie_id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    released INTEGER NOT NULL,
    rating NUMERIC(2, 1) NOT NULL
);
```

### Models

As a next step, we create a new file `models/movies.py` and declare there all 
SQLAlchemy models used across `movies` service.

```python
from sqlalchemy import (
    Column,
    Integer,
    Float,
    String,
)

from app.models.base import BaseModel


class MovieModel(BaseModel):
    __tablename__ = "movies"

    movie_id = Column(Integer, primary_key=True)
    title = Column(String)
    released = Column(Integer)
    rating = Column(Float)
```

Note, that when you inherit your model from `BaseModel` (defined in `models/base.py`),
which in turn is inherited from SQLAlchemy base class, then mapping to the specific database
schema is done via the `metadata` attribute of the generated declarative base class 
(see `backend/database.py` for details).

If you operate over Postgres table-valued functions, you can use `TableValuedMixin` class 
as it's shown below. In this case, `__tablename__` refers to the corresponding Postgres 
function.

```python
from app.models.base import (
    BaseModel,
    TableValuedMixin,
)

class TableValuedFunctionModel(TableValuedMixin, BaseModel):
    __tablename__ = "my_function"

    ...
```

### Schemas

Package `schemas` provide Pydantic models that are used to serialize data used throughout
the application, e.g. request data (passed via router parameters) and response data 
(declared as router `response_model`).

As a next step, we create a new file `schemas/movies.py` and declare there all schemas 
(Pydantic models) used across `movies` service. In our case, it will be a single `MovieSchema`
used as a request response model.

```python
from pydantic import BaseModel


class MovieSchema(BaseModel):
    movie_id: int
    title: str
    released: int
    rating: float

    class Config:
        orm_mode = True
```

We set Config property to `True` to support mapping between `MovieSchema` and corresponding
SQLAlchemy `MovieModel`.

### Routers

Package `routers` enables to define path operations and keep it organized, i.e. 
separate paths related to multiple services. As usual, let's create a new file for our
service `routers/movies.py` and define there two entry points: `get_movie` that returns
the movie given `movie_id`, and `get_new_movies` that returns all movies released
since given `year` and having rating higher than given `rating`.

```python
from typing import List

from fastapi import (
    APIRouter,
    Depends,
)
from sqlalchemy.orm import Session

from app.backend.database import create_session
from app.schemas.movies import MovieSchema
from app.services.movies import MovieService

router = APIRouter(prefix="/movies")


@router.get("/", response_model=MovieSchema)
async def get_movie(
    movie_id: int,
    session: Session = Depends(create_session),
) -> MovieSchema:
    return MovieService(session).get_movie(movie_id)


@router.get("/new", response_model=List[MovieSchema])
async def get_new_movies(
    year: int,
    rating: float,
    session: Session = Depends(create_session),
) -> List[MovieSchema]:
    return MovieService(session).get_new_movies(year, rating)
```

### Services

As a last step, we create a new file `services/movies.py` where we implement service
related logic, in our case it's simply reading data from corresponding db objects and
converting it to the response schema.

Every service is a subclass of `AppService` class which provides database session object.

Data access methods are isolated from service logic as a subclass of `AppCRUD` class 
which provides helper functions for CRUD operations over db objects.

```python
from typing import List

from app.models.movies import MovieModel
from app.schemas.movies import MovieSchema
from app.services.base import (
    AppCRUD,
    AppService,
)


class MovieService(AppService):
    def get_movie(self, movie_id: int) -> MovieSchema:
        return MovieCRUD(self.db).get_movie(movie_id)

    def get_new_movies(self, year: int, rating: float) -> List[MovieSchema]:
        return MovieCRUD(self.db).get_new_movies(year, rating)


class MovieCRUD(AppCRUD):
    def get_movie(self, movie_id: int) -> MovieSchema:
        return MovieSchema.from_orm(self.query(MovieModel, movie_id=movie_id).first())

    def get_new_movies(self, year: int, rating: float) -> List[MovieSchema]:
        query = self.query(
            MovieModel, MovieModel.released >= year, MovieModel.rating >= rating
        )

        return [MovieSchema.from_orm(obj) for obj in query.all()]
```

### Config

Configuration settings are provided via `backend/config.py` module and can be read from
environment variables prefixed with `MYAPI_`. It also supports dotenv parsing from `.env`
file placed in project root directory. 

If you have multiple backends, e.g. `prod`, `stage` and `dev`, you can set up corresponding 
DSN strings in dotenv file and switch between backends using environment variable
`MYAPI_ENV` (by default, it refers to `dev` environment).

```bash
$ cat .env
MYAPI_DATABASE__PROD="postgresql://user:password@host:port/dbname_prod"
MYAPI_DATABASE__STAGE="postgresql://user:password@host:port/dbname_stage"
MYAPI_DATABASE__DEV="postgresql://user:password@host:port/dbname_dev"

$ MYAPI_ENV=stage uvicorn app.main:app
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

Or you can initialize everything using environment variables only.

```bash
$ MYAPI_ENV=dev MYAPI_DATABASE__DEV="postgresql://" uvicorn app.main:app
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

## Authentication

Authentication service is integrated to application using the same design pattern 
we used for adding `movies` service.

For demonstration purposes, we use OAuth2 Password grant type as a protocol to get an 
access token given `username` and `password`. The Password grant type is one of the
simplest OAuth grants and involves only one step: the app provides a login form to collect
user's credentials (username and password) and makes a POST request to the server in order
to exchange the password for an access token.

Note, that the Password grant is not recommended way as it requires the application collect
user's password. Check the OAuth 2.0 security best practices to remove the Password grant
from OAuth.

### Backend setup

First, we create table `users` in the backend database where the application will store
user information. 

```sql
CREATE TABLE IF NOT EXISTS myapi.users (
    user_id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    hashed_password TEXT NOT NULL,
    UNIQUE(email)
);
```

Application does not store user's plain password, it uses hashing algorithm to encode 
passwords before writing data to database.

We add `auth` module in each of four principal packages (the same as we did for `movies` service).
`AuthService` class (see `services/auth.py` for details) below implements writing user's
data to database table.

```python
from passlib.context import CryptContext

from app.models.auth import UserModel
from app.schemas.auth import CreateUserSchema
from app.services.base import (
    AppCRUD,
    AppService,
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService(AppService):
    def create_user(self, user: CreateUserSchema) -> None:
        AuthCRUD(self.db).add_user(user)
        

class AuthCRUD(AppCRUD):
    def add_user(self, user: CreateUserSchema) -> None:
        user = UserModel(
            name=user.name,
            email=user.email,
            hashed_password=Hasher.bcrypt(user.password),
        )

        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)


class Hasher:
    @staticmethod
    def bcrypt(password: str) -> str:
        return pwd_context.hash(password)

    @staticmethod
    def verify(hashed_password: str, plain_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)
```

The convenience methods for making CRUD operations over users can be added to command 
line interface via `cli` module. Below is an example on how to create new user via 
command-line.

```python
import click

from app.backend.database import create_session
from app.schemas.auth import CreateUserSchema
from app.services.auth import AuthService


@click.group()
def main() -> None:
    pass


@main.command()
@click.option("--name", type=str, help="User name")
@click.option("--email", type=str, help="Email")
@click.option("--password", type=str, help="Password")
def create_user(name: str, email: str, password: str) -> None:
    user = CreateUserSchema(name=name, email=email, password=password)
    session = next(create_session())
    AuthService(session).create_user(user)
```

Now executing following from command-line you get a new record in `users` table.

```bash
myapi create-user --name 'John Smith' --email john@domain.com --password qwerty123 
```
