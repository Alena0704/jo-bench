import pandas as pd
import numpy as np
import plotly.express as px
import plotly
import functions
from preprocess_dataframe import get_preprocess_dataframe
import os
import re
import glob
import math
import plotly.graph_objs as go
from shutil import copyfile
import time


#preprocessing dataframe
def get_df(path_folder, file_name, mode, times):
    df = pd.DataFrame()
    if times>1:
        csv_files = glob.glob(path_folder + "/*.csv")
        df_list = (pd.read_csv(file) for file in csv_files)
        df   = pd.concat(df_list, ignore_index=True)
    else:
        df = pd.read_csv('{}/{}'.format(path_folder,file_name))
    df = df.fillna(0)
    df=df.rename(columns={'Plan time': 'plan_time'})
    df = df.rename(columns = {'Query Number':'query_number', 'Query Name':'query_name', 'Execution Time':'execution_time', 'Query hash':'query_hash'})
    df['query_number'] = df['query_number'].astype(int)
    df['query_hash'] = df['query_hash'].astype(str)
    df['plan_time'] = df['plan_time'].astype(float)
    if times>1:
        lst_data = []
        dict_query = {}
        for i in df.itertuples(index=False):
            if i.query_name in dict_query:
                dict_query[i.query_name][1] += i.execution_time
                dict_query[i.query_name][3] += i.plan_time
            else:
                dict_query[i.query_name] = [i.query_name, i.execution_time, i.query_hash, i.plan_time]
        df = pd.DataFrame(dict_query.values(), columns = ['query_name', 'execution_time', 'query_hash', 'plan_time'])
        df['exec_time_avg'] = df['execution_time']/times
        df['plan_time_avg'] = df['plan_time']/times
    return df

def renames(df, mode):
    df = df.rename(columns = {'plan_time':'plan_time_{}'.format(mode), 'execution_time':'execution_time_{}'.format(mode)})
    if mode == 'control' or mode == 'disabled':
        df = df.rename(columns = {'plan_time_avg':'plan_time_avg_{}'.format(mode), 'exec_time_avg':'exec_time_avg_{}'.format(mode)})
    return df

def forming_pdf(iteration, path, learn_iter):
    df_control = get_df('{}/{}_folder{}'.format(path, 'frozen',iteration),'frozen_1_report.csv', 'control', 1)
    df_disabled = get_df('{}/{}_folder{}'.format(path, 'disabled',iteration), 'disabled_1_report.csv', 'disabled', 1)
    df_learn = get_df('{}/{}_folder{}'.format(path, 'learn',iteration), '14_job_onepass_result_learn.csv', 'learn', learn_iter)
    df_disabled = renames(df_disabled, 'disabled')
    df_control = renames(df_control, 'control')
    df_learn = renames(df_learn, 'learn')
    df = df_disabled.merge(df_control, how='left', on='query_name')

    dict_hash = {}
    for i in df_disabled.itertuples(index=False):
        if i.query_hash in dict_hash:
            dict_hash[i.query_hash].append(i.query_name)
        else:
            dict_hash[i.query_hash] = []
            dict_hash[i.query_hash].append(i.query_name)
    return df

def upload_pics(contain, dir_to, filename):
    plotly.offline.plot(contain, image_filename=filename, image='svg')
    time.sleep(10)
    os.replace('{}/{}.svg'.format('/home/alena/Downloads', filename), '{}/{}.svg'.format(dir_to, filename))
    
    
