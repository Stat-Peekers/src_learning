# ****************************************** Get Event Data ****************************************** #
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


class EventDataExtraction:

    def __init__(self):
        self.data_dir = "open-data/data/events"
        self.event_json = {}
        self.event_df = pd.DataFrame()

    def get_event_json(self):
        self.event_json = json.load(open(self.data_dir + "eventetitions.json"))

    def get_event_df(self):
        self.event_df = json_normalize(self.event_json)

    def get_event_final_call(self):
        self.get_event_json()
        self.get_event_df()
