import os
import sys
import configparser

import pandas as pd

from sqlalchemy import create_engine, inspect

src_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(src_dir)
os.chdir(src_dir)

parent_dir = os.path.abspath(os.path.join(src_dir, os.pardir))
sys.path.append(parent_dir)
os.chdir(parent_dir)


class DBConnect:

    def __init__(self, db_name):
        config_obj = configparser.ConfigParser()
        self.db_creds = config_obj.read("config/sp_db_creds.ini")
        self.conn_obj = ""
        self.host_name = config_obj["db_creds"]["hostname"]
        self.user_name = config_obj["db_creds"]["username"]
        self.pwd = config_obj["db_creds"]["pwd"]
        self.db_name = db_name
        self.conn_obj = create_engine("mysql://" + self.user_name + ":" + self.pwd + "@" + self.host_name + "/" + self.db_name)
        self.db_inspector = inspect(self.conn_obj)

    def get_table(self, table_name):
        """
        Obtain a specific table from the DB
        :param table_name: (str) Exact Name of the table
        :return: (pandas Dataframe) DB table that was requested
        """
        df = pd.read_sql_table(table_name, self.conn_obj, schema=self.db_name)
        return df

    def my_execute_sql_query(self, my_query):
        """
        Execute any SQL query passed
        :param my_query: (str) Query string to be executed
        :return: returns a Dataframe selected by the query provided
        :rtype: pandas DataFrame
        """
        df = pd.read_sql_query(my_query, self.conn_obj)
        return df

    def append_table_and_upload_data(self, data_df, table_name):
        data_df.to_sql(name=table_name, con=self.conn_obj, schema=self.db_name, if_exists="append", index=False)

    # def __init__(self, db_name):
    #     config_obj = configparser.ConfigParser()
    #     self.db_creds = config_obj.read("config/skpi_cpanel_creds.ini")
    #     self.conn_obj = ""
    #     self.host_name = config_obj["skpi_db_creds"]["host_name"]
    #     self.user_name = config_obj["skpi_db_creds"]["user_name"]
    #     self.pwd = config_obj["skpi_db_creds"]["pwd"]
    #     self.db_name = db_name
    #     self.conn_obj = create_engine("mysql://" + self.user_name + ":" + self.pwd + "@" + self.host_name + "/" + self.db_name)


if __name__ == "__main__":

    db_obj = DBConnect("statsbomb_data")
