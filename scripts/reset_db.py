from scripts.delete_db import run as clear_db
from scripts.populate_dummy import run as populate_db


def run():
    clear_db()
    populate_db()
