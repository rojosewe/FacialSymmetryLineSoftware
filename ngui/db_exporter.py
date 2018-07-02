import os
from utils.conf import Conf as cf
import easygui as gui
from utils import JsonLoader, CSV
from utils.Messages import messages as ms


def export_db():
    location = gui.filesavebox(msg=ms["choose_save_location"], title=ms["save"],
                               default=cf.get("home_dir") + os.sep + 'db.csv', filetypes=["*.csv"])
    cf.set("home_dir", os.path.abspath(os.path.dirname(location)))
    if location is not None and not location.endswith(".csv"):
        location += ".csv"
    patients = JsonLoader.getAllPatients()
    CSV.patientsToCSV(patients, location)
