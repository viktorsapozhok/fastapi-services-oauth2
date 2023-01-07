import click

from app.backend.database import create_session
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
@click.option("--name", type=str, help="User name")
@click.option("--email", type=str, help="Email")
@click.option("--password", type=str, help="Password")
def create_user(name: str, email: str, password: str) -> None:
    """Create new user.

    Write new user (with hashed password) to corresponding database table.

    Examples:
        myapi --name 'John Smith' --email john_smith@domain.com --password qwerty123
    """

    # initialize user schema
    user = CreateUserSchema(name=name, email=email, password=password)

    # generate new database session
    session = next(create_session())

    # write to database
    AuthService(session).create_user(user)
