from typing import Any

import click

from app.backend.database import create_factory
from app.const import ENV_DEV
from app.schemas.auth import CreateUserSchema
from app.services.auth import AuthService
from app.version import __version__


@click.group(invoke_without_command=True)
@click.option("--version", is_flag=True, help="Show package version")
def main(version: bool) -> None:
    """Welcome to API command line!"""

    if version:
        click.echo("Version: " + __version__)


@main.command()
@click.option("--env", default=ENV_DEV, help="Environment")
@click.option("--name", type=str, help="User name")
@click.option("--email", type=str, help="Email")
@click.option("--password", type=str, help="Password")
def create_user(**kwargs: Any) -> None:
    """Create new user."""

    user = CreateUserSchema(
        name=kwargs["name"], email=kwargs["email"], password=kwargs["password"]
    )

    session_factory = create_factory(kwargs["env"])

    with session_factory() as session:
        AuthService(session).create_user(user)
