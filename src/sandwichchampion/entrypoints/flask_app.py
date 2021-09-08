from flask import Flask, jsonify, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .. import config
from ..domain import model
from ..adapters import orm, repository

orm.start_mappers()
get_session = sessionmaker(bind=create_engine(config.get_postgres_uri()))
app = Flask(__name__)


@app.route("/")
def index():
    return "<h1>hello!</h1>"


@app.route("/api/is_alive")
def is_alive():
    return {"message": "It's alive!"}, 200
