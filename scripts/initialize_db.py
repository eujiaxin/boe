import os
from scripts.delete_db import run as clear_db
from scripts.populate_reqs import run as populate_reqs
from api.models import CallistaDataFile
from django.core.files.base import File
from django.conf import settings
import scripts.process_csv as pc


def run():
    clear_db()
    script_path = os.path.join(settings.BASE_DIR, "scripts")
    pc.bulk_pc(os.path.join(script_path, "dummy_data.csv"), True)
    populate_reqs()
