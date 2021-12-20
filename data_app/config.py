from logging import FileHandler
from celery import Celery
from flask import Flask, logging

service = Flask(__name__)

logger = logging.create_logger(service)
logger.addHandler(FileHandler("data_app.log"))

app = Celery(
    "data_app",
    backend="redis://localhost:6379/0",
    broker="redis://localhost:6379/0",
    include=["data_app.tasks"],
)
app.config_from_object("celeryconfig")
