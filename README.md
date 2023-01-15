# fastapi-services-oauth2

This repository provides an approach on how to structure FastAPI application with 
multiple services, simple OAuth2 authentication, and Postgres backend.

## Structure overview

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

