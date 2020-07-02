# ****************************************** Get All Competitions ****************************************** #
# import system libraries:
import os
import sys
import json
import pandas as pd

from pandas.io.json import json_normalize

from common_files.common_functions import get_data_from_file_json

# Switch Working Directory 1 step higher:
src_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(src_dir)
os.chdir(src_dir)

parent_dir = os.path.abspath(os.path.join(src_dir, os.pardir))
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
    def _get_comp_json(self):
        self.comp_json = json.load(open(self.data_dir + "competitions.json"))

    def _get_comp_df(self):
        self.comp_df = json_normalize(self.comp_json)

    def _get_comp_final_call(self):
        self._get_comp_json()
        self._get_comp_df()

    def _get_comp_info(self):
        self._get_comp_final_call()

    # ********************** Get Event Data ********************** #
    def get_event_data(self, e_filename):
        self.event_json = get_data_from_file_json(self.event_data_dir + e_filename + ".json")

    # ********************** Get Match Data ********************** #
    def _get_match_json(self):
        comp_folder_list = [folder_name for folder_name in os.listdir(self.match_data_dir)]
        self.match_jsons = [json.load(open(self.match_data_dir + c_folder + "/" + m_filename, encoding="utf-8"))
                            for c_folder in comp_folder_list for m_filename in os.listdir(self.match_data_dir + c_folder)]

    # ********************** Get Event Data ********************** #
    def _get_event_json(self):
        event_json_list = [folder_name for folder_name in os.listdir(self.event_data_dir)]
        self.event_json = [json.load(open(self.event_data_dir + "/" + m_filename, encoding="utf-8"))
                           for m_filename in event_json_list]

    def _get_event_data_df(self):
        event_json_list = [folder_name for folder_name in os.listdir(self.event_data_dir)]

    def _get_match_df(self):
        for tour_index in range(len(self.match_jsons)):
            self.match_df = self.match_df.append(self.match_jsons[tour_index])
        self.match_df.reset_index(drop=True, inplace=True)

    def _get_comp_id(self):
        self.match_df["competition_id"] = json_normalize(self.match_df["competition"])["competition_id"]

    def _get_comp_stage_id(self):
        self.match_df["competition_stage_id"] = json_normalize(self.match_df["competition_stage"])["id"]

    def _get_stadium_id(self):
        try:
            self.match_df["stadium_id"] = json_normalize(self.match_df["stadium"])["id"]
        except AttributeError:
            print("There are some null values in the Stadium column.\nReplacing them with empty dictionaries.")
            self.match_df['stadium'] = self.match_df['stadium'].apply(lambda x: {} if pd.isna(x) else x)
            self.match_df["stadium_id"] = json_normalize(self.match_df["stadium"])["id"]

    def _get_referee_id(self):
        try:
            self.match_df["referee_id"] = json_normalize(self.match_df["referee"])["id"]
        except AttributeError:
            print("There are some null values in the Referee column.\nReplacing them with empty dictionaries.")
            self.match_df['referee'] = self.match_df['referee'].apply(lambda x: {} if pd.isna(x) else x)
            self.match_df["referee_id"] = json_normalize(self.match_df["referee"])["id"]

    def _get_home_team_stats(self):
        home_team_df = json_normalize(self.match_df["home_team"])
        self.match_df = pd.concat([self.match_df, home_team_df], axis=1)
        del home_team_df

    def _get_away_team_stats(self):
        away_team_df = json_normalize(self.match_df["away_team"])
        self.match_df = pd.concat([self.match_df, away_team_df], axis=1)
        del away_team_df

    def _get_event_final_call(self):
        # self._get_event_json()
        self._get_event_data_df()

    def _get_match_final_call(self):
        self._get_match_json()
        self._get_match_df()
        self._get_comp_id()
        self._get_comp_stage_id()
        self._get_stadium_id()
        self._get_home_team_stats()
        self._get_away_team_stats()
        self._get_referee_id()

    def _get_match_info(self):
        self._get_match_final_call()

    def _get_event_data(self):
        self._get_event_final_call()

    def final_data_extraction_call(self):
        # Extract competition info and arrange it for a DB table:
        self._get_comp_info()

        # Extract match data and arrange it for a DB table:
        self._get_match_info()

        # Extract event data and arrange it for a DB table:
        self._get_event_data()

    def upload_data_to_db(self):
        pass


# testing:
if __name__ == "__main__":
    ext_obj = DataExtraction()
    # Get All Data:
    ext_obj.final_data_extraction_call()
    ext_obj.comp_df.to_csv("data/input/comp_info.csv", index=False)
    ext_obj.match_df.to_csv("data/input/match_info.csv", index=False)
    ext_obj.event_df.to_csv("data/input/match_info.csv", index=False)
