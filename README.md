# fastapi-services-oauth2

This repository provides an approach on how to effectively structure a FastAPI application 
simplifying the implementation of multiple service logic, integrate it with Postgres backend, 
and implement straightforward OAuth2 Password authentication flow using Bearer and 
JSON Web Tokens (JWT).

[Read the tutorial][1] for more details.

[1]: https://viktorsapozhok.github.io/fastapi-oauth2-postgres/ "Structuring FastAPI app with multiple services"

## How to install

Clone this repository and install using `pip`.

```bash
$ pip install --editable .
```

## How to run

Configure the relevant DSN string to your Postgres backend database in `.env` file, 
or provide it from the environment variable `MYAPI_DATABASE__DSN`.

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