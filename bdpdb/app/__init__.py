import os
import logging
from flask import Flask
from flask_appbuilder import SQLA
from flask_appbuilder import AppBuilder
from sqlalchemy.engine import Engine
from sqlalchemy import event
from .security import MySecurityManager

logging.basicConfig(format='%(asctime)s:%(levelname)s:%(name)s:%(message)s')
logging.getLogger().setLevel(logging.DEBUG)


app = Flask(__name__)
app.config.from_object('config')
app.jinja_env.auto_reload = True
app.config['TEMPLATES_AUTO_RELOAD'] = True
#app.run(debug=True)

db = SQLA(app)
appbuilder = AppBuilder(app, db.session, security_manager_class=MySecurityManager)

app.jinja_env.filters['rel_path'] = lambda paths: os.path.relpath(*paths)
app.jinja_env.filters['basename'] = os.path.basename

@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()
    

from app import models, views
