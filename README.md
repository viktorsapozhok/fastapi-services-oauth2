# fastapi-services-oauth2

This repository provides an approach on how to structure FastAPI application with 
multiple services, simple OAuth2 authentication, and Postgres backend.

[Read the tutorial][1] for more details.

[1]: https://viktorsapozhok.github.io/fastapi-oauth2-postgres/ "Structuring FastAPI app with multiple services"

## How to install

Clone this repository and install using `pip`.

```bash
$ pip install --editable .
```

Verify installation using `myapi` command.

```bash
$ myapi --version
Version: 0.0.0
```

## How to run

Set the relevant DSN string to your Postgres backend database in `.env` file. 
By default, application uses `dev` environment, i.e. `MYAPI_DATABASE__DEV` DSN string
will be used. You can change environment using `MYAPI_ENV` environment variable.

To run application in `dev` backend environment, you can simply use following.

```bash
$ uvicorn app.main:app
```

To run in another environment (e.g. in `stage`), you can use following.

```bash
$ MYAPI_ENV=stage uvicorn app.main:app
```

## License

MIT License (see [LICENSE](LICENSE)).