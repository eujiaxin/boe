from scripts.delete_db import run as clear_db
from scripts.populate_dummy import run as populate_db
from scripts.populate_reqs import run as populate_reqs


def run():
    clear_db()
    populate_db()
    populate_reqs()
