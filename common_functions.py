# ************************************************* Common Functions ************************************************* #

# import libraries
import os
import sys
import json
import time
import logging
import requests
import urllib.request

import numpy as np
import pandas as pd

from sklearn import linear_model, feature_selection
from sklearn.metrics import mean_squared_error, r2_score

# Switch Working Directory 1 step higher:
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(parent_dir)
os.chdir(parent_dir)


def get_data_from_url_json(my_json_url):
    data = 0
    try:
        response = requests.get(my_json_url)
        data = response.json()
    except Exception as ex:
        print('URL is not available. ' + str(ex))

    return data


def get_data_from_file_json(filename):
    data = 0
    try:
        data = json.load(open(filename))
    except Exception as ex:
        print('JSON file is not available. ' + str(ex))

    return data


def get_player_pics(p_id, t_name, p_name):
    dir_name = "pics/player_pics/" + str(t_name)
    file_name = dir_name + "/" + str(p_name) + ".png"
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
    if not os.path.exists(file_name):
        # noinspection PyBroadException
        try:
            temp_var = urllib.request.urlretrieve("https://www.prokabaddi.com/static-assets/images/players/small/26/"
                                                  + str(p_id) + ".png?v=5.04",
                                                  "pics/player_pics/" + str(t_name) + "/" + str(p_name) + ".png")
            del temp_var
        except Exception:
            print("Picture not available for " + str(p_name))
    else:
        print("Player pic already exists for " + str(p_name))


def padding_zeros_for_nulls(df, col):
    df[col] = np.where(df[col].isnull(), 0, df[col])
    return df[col]


def logger_setup(filename):
    logging.basicConfig(filename=filename, filemode="w", level=logging.DEBUG)
    log_obj = logging.getLogger()
    return log_obj


def my_linear_regression(x_train, y_train, x_test, y_test=None):

    # if y_test is not None:
    #     test_df = pd.concat([x_test, y_test], axis=1)
    # else:
    #     test_df = x_test

    regr_obj = linear_model.LinearRegression()
    regr_obj.fit(x_train, y_train)
    y_pred = regr_obj.predict(x_test)
    # The mean squared error
    mean_sqr_error = mean_squared_error(y_test, y_pred)
    # Explained variance score: 1 is perfect prediction
    r_sqr_score = r2_score(y_test, y_pred)

    return y_pred, regr_obj.coef_, mean_sqr_error, r_sqr_score


def my_cross_validation(df_x, y, n_splits=10):
    from sklearn.model_selection import KFold
    kf = KFold(n_splits=n_splits)
    kf.get_n_splits(df_x)
    count = 0
    final_df = pd.DataFrame(columns=["fold_no", "pred_coeffs", "mean_sqr_error", "r_sqr_error"])
    final_df["pred_coeffs"] = final_df["pred_coeffs"].astype(object)

    for train_index, test_index in kf.split(df_x):
        print("For fold no. " + str(count + 1))
        x_train, x_test = df_x.loc[train_index], df_x.loc[test_index]
        y_train, y_test = y.loc[train_index], y.loc[test_index]

        pred_df, pred_coef, mean_sq_err, r_sq_err = my_linear_regression(x_train, y_train, x_test, y_test)

        final_df.at[count, "fold_no"] = count + 1
        final_df.at[count, "pred_coeffs"] = list(pred_coef)
        final_df.loc[count, "mean_sqr_error"] = mean_sq_err
        final_df.loc[count, "r_sqr_error"] = r_sq_err

        count += 1
        # print("Coefficients: \n", pred_coef)
        # # The mean squared error
        # print("Mean squared error: %.2f" % mean_sq_err)
        # # Explained variance score: 1 is perfect prediction
        # print('Variance score: %.2f' % r_sq_err)

    final_df.to_csv("data/working/cv_results_" + time.strftime("%H-%M-%S") + ".csv", index=False)
