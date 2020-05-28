# ****************************************** Get All Competetions ****************************************** #
# Import Libs:
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


class GetCompInfo:

    def __init__(self):
        self.data_dir = "open-data/data/"
        self.comp_json = {}
        self.comp_df = pd.DataFrame()

    def get_comp_json(self):
        self.comp_json = json.load(open(self.data_dir + "competitions.json"))

    def get_comp_df(self):
        self.comp_df = json_normalize(self.comp_json)

    def get_comp_final_call(self):
        self.get_comp_json()
        self.get_comp_df()
