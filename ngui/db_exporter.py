import os
from utils.conf import Conf as cf
import easygui as gui
from utils import JsonLoader, CSV, excel
from utils.Messages import messages as ms

EXTENSION = ".xlsx"

def export_db():
    location = gui.filesavebox(msg=ms["choose_save_location"], title=ms["save"],
                               default=cf.get("home_dir") + os.sep + 'db' + EXTENSION, filetypes=["*" + EXTENSION])
    cf.set("home_dir", os.path.abspath(os.path.dirname(location)))
    if location is not None and not location.endswith(EXTENSION):
        location += EXTENSION
    patients = JsonLoader.getAllPatients()
    excel.patients_to_excel(patients, location)
