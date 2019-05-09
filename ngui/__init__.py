import sys
import easygui as gui
from utils.Messages import messages as ms
from workAreas.state_manager import State
from ngui import create_new_patient, load_patient, db_exporter
from utils.exceptions import LeftIncompleteException


def make_initial_selection():
    action = gui.indexbox(ms["choose_an_option"], choices=(ms["create_new_patient"],
                                                           ms["open_patient"],
                                                           ms["export_to_csv"],
                                                           ms["exit"]),
                          default_choice=ms["create_new_patient"], cancel_choice=ms["exit"])
    if action == 0:
        create_new_patient.new_patient_fill_info()
    elif action == 1:
        load_patient.select_patient()
    elif action == 2:
        db_exporter.export_db()
    else:
        sys.exit()


def start(home_path=None):
    while 1:
        try:
            State.initialize()
            make_initial_selection()
            State.clear()
        except LeftIncompleteException as e:
            print(e)

