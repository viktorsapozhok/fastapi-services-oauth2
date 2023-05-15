# fastapi-services-oauth2

This repository provides an approach on how to structure FastAPI application with 
multiple services, simple OAuth2 Password authentication with Bearer and JWT tokens, 
and Postgres backend database.

[Read the tutorial][1] for more details.

[1]: https://viktorsapozhok.github.io/fastapi-oauth2-postgres/ "Structuring FastAPI app with multiple services"

## How to install

Clone this repository and install using `pip`.

```bash
$ pip install --editable .
```

## How to run

Configure the relevant DSN string to your Postgres backend database in `.env` file, 
or provide it from environment variable `MYAPI_DATABASE__DSN`.

To run the application use following.

```bash
$ uvicorn app.main:app
```

or 

```bash
$ MYAPI_DATABASE__DSN=postgresql://... uvicorn app.main:app
```

## License

MIT License (see [LICENSE](LICENSE)).