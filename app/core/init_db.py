from alembic.config import CommandLine
import sys

def run_migrations():
    cli = CommandLine()
    cli.main(argv=["upgrade", "head"])