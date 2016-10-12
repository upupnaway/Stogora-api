#!venv/bin/python
from flask.ext.script import Manager, Server, Shell

from cli.database import manager as database_manager
from stogora_app import app


def _make_context():
  return dict(app=app)


manager = Manager(app)
manager.add_command('shell', Shell(make_context=_make_context))
manager.add_command('runserver', Server())
manager.add_command('database', database_manager)

if __name__ == '__main__':
  manager.run()