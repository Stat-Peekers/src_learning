# ****************************************** Get Match Data ****************************************** #
# import system libraries:
import os
import sys
import json

import pandas as pd

from pandas.io.json import json_normalize

# src_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
# sys.path.append(src_dir)
# os.chdir(src_dir)

# Switch Working Directory 1 step higher:
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(parent_dir)
os.chdir(parent_dir)


class MatchDataExtraction:

    def __init__(self, complist=None):
        self.complist = complist
        self.data_dir = "open-data/data/matches/"
        self.match_jsons = []
        self.match_df = pd.DataFrame()

    def get_match_json(self):
        comp_folder_list = [folder_name for folder_name in os.listdir(self.data_dir)]
        match_jsons = []
        import time
        start = time.perf_counter()
        for c_folder in comp_folder_list:
            for m_filename in os.listdir(self.data_dir + c_folder):
                match_jsons.append(json.load(open(self.data_dir + c_folder + "/" + m_filename, encoding="utf-8")))
        stop = time.perf_counter()
        print("Time taken for normal FOR loop: ", stop - start)
        start = time.perf_counter()
        self.match_jsons = [json.load(open(self.data_dir + c_folder + "/" + m_filename, encoding="utf-8"))
                            for c_folder in comp_folder_list for m_filename in os.listdir(self.data_dir + c_folder)]
        stop = time.perf_counter()
        print("Time taken for list comp: ", stop - start)
        match_df = pd.DataFrame()
        for tour_index in range(len(self.match_jsons)):
            match_df = match_df.append(self.match_jsons[tour_index])

    def get_match_df(self):
        self.match_df = json_normalize(self.match_json)

    def get_match_final_call(self):
        self.get_match_json()
        self.get_match_df()


if __name__ == "__main__":
    match_obj = MatchDataExtraction()
    match_obj.get_match_final_call()
