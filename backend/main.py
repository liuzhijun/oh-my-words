import click
import uvicorn
from pathlib import Path
from database.database import DATABASE_FILE
from init_database import init

cmd = click.Group()


@cmd.command("database")
def database():
    init()

@cmd.command("serve")
@click.option('--host', default='127.0.0.1', help='host')
@click.option('--port', default=8000, help='port')
def serve(host, port):
    uvicorn.run("server:app", host=host, port=port)

if __name__ == '__main__':
    cmd()
