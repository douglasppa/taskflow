from alembic.config import CommandLine


def run_migrations():
    cli = CommandLine()
    cli.main(argv=["upgrade", "head"])
