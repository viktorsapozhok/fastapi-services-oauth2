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

### Database setup

First, we create a database schema called `myapi` and table `movies` in there. In this table,
we insert list of records with following fields: movie_id, title, released (release year) and 
rating (e.g. movie imdb rating).

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
SQLAlchemy models used in `movies` service.

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

Note, that you need to inherit your model from `BaseModel` (defined in `models/base.py`) 
if you operate over Postgres table or view. When you want to read data from Postgres 
table-valued functions, you can use `TableValuedMixin` class as it's shown below. 
In this case, `__tablename__` refers to corresponding Postgres function.

```python
from app.models.base import (
    BaseModel,
    TableValuedMixin,
)

class ReadFromTVFModel(TableValuedMixin, BaseModel):
    __tablename__ = "my_function"

    ...
```

