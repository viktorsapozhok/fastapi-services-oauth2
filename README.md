# fastapi-services-oauth2

This repository provides an approach on how to effectively structure a FastAPI application 
with multiple services using 3-tier design pattern, integrate it with Postgres backend, 
and implement straightforward OAuth2 Password authentication flow using Bearer and 
JSON Web Tokens (JWT).

[Read the tutorial][1] for more details.

[1]: https://medium.com/gitconnected/structuring-fastapi-project-using-3-tier-design-pattern-4d2e88a55757 "Structuring FastAPI Application Using 3-Tier Design Pattern"

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