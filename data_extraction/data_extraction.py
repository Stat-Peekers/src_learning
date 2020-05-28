# ****************************************** Get All Competitions ****************************************** #
# import system libraries:
import os
import sys
import json

import pandas as pd

from pandas.io.json import json_normalize

from common_functions import get_data_from_file_json

# Switch Working Directory 1 step higher:
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(parent_dir)
os.chdir(parent_dir)


class DataExtraction:

    def __init__(self):
        # Initiation for competition data:
        self.data_dir = "open-data/data/"
        self.comp_json = {}
        self.comp_df = pd.DataFrame()
        # Initiation for match data:
        self.match_data_dir = "open-data/data/matches/"
        self.match_jsons = []
        self.match_df = pd.DataFrame()
        # Initiation for event data:
        self.event_data_dir = "open-data/data/events/"
        self.event_json = {}
        self.event_df = pd.DataFrame()

    # ******************* Get competition Data ******************* #
    def get_comp_json(self):
        self.comp_json = json.load(open(self.data_dir + "competitions.json"))

    def get_comp_df(self):
        self.comp_df = json_normalize(self.comp_json)

    def get_comp_final_call(self):
        self.get_comp_json()
        self.get_comp_df()

    def get_comp_info(self):
        self.get_comp_final_call()

    # ********************** Get Event Data ********************** #
    def get_event_data(self, e_filename):
        self.event_json = get_data_from_file_json(self.event_data_dir + e_filename + ".json")

    # ********************** Get Match Data ********************** #
    def get_match_json(self):
        comp_folder_list = [folder_name for folder_name in os.listdir(self.match_data_dir)]
        self.match_jsons = [json.load(open(self.match_data_dir + c_folder + "/" + m_filename, encoding="utf-8"))
                            for c_folder in comp_folder_list for m_filename in os.listdir(self.match_data_dir + c_folder)]

    def get_match_df(self):
        for tour_index in range(len(self.match_jsons)):
            self.match_df = self.match_df.append(self.match_jsons[tour_index])

    def get_match_final_call(self):
        self.get_match_json()
        self.get_match_df()

    def get_match_info(self):
        self.get_match_final_call()


# testing:
if __name__ == "__main__":
    ext_obj = DataExtraction()
    # Get Comp Data:
    ext_obj.get_comp_info()
    ext_obj.comp_df.to_csv("data/input/comp_info.csv", index=False)
    # Get Match info:
    ext_obj.get_match_final_call()
    ext_obj.match_df.to_csv("data/input/match_info.csv", index=False)
