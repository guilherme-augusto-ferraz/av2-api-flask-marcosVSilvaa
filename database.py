# database.py
from flask_sqlalchemy import SQLAlchemy
from flask import Flask

db = SQLAlchemy()

def configure_database(app: Flask):
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    # A linha abaixo deve ser executada para criar o banco de dados na primeira vez
    # with app.app_context():
    #     db.create_all()