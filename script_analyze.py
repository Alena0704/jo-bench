import plotly.graph_objs as go
import pandas as pd
import numpy as np
import plotly.express as px
import functions
from preprocess_dataframe import get_preprocess_dataframe
import os
import re
import glob
from argparse import ArgumentParser
import re
import plotly.graph_objs as go
import time
import plotly

w=1200
h=700

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

def rename(lst, cond_prev, cond_next, size):
    k=0
    for i in lst:
        if i==cond_prev and k>=size:
            i=cond_next
        k+=1
    return lst

def form_conditions(df_input, time_exem):
    df_input=df_input.sort_values('better_worse')
    lst_cond=[]
    lst_groups=['df_less0_15','df_less15_30','df_less30_60','df_less60_80', 'df_less80_100']
    df_input['better_worse']=((df_input['{}_time_disabled'.format(time_exem)]-df_input['{}_time_control'.format(time_exem)])/df_input['{}_time_disabled'.format(time_exem)])*100
    lst_contain=[0, 0, 0, 0,0]
    for i in df_input['better_worse']:
        if lst_contain[0]<25:
            lst_cond.append('df_less0_15')
            lst_contain[0]+=1
        elif lst_contain[1]<25:
            lst_cond.append('df_less15_30')
            lst_contain[1]+=1
        elif lst_contain[2]<25:
            lst_cond.append('df_less30_60')
            lst_contain[2]+=1
        elif lst_contain[3]<25:
            lst_cond.append('df_less60_80')
            lst_contain[3]+=1
        else:
            lst_cond.append('df_less80_100')
            lst_contain[4]+=1

    df_input['condition']=lst_cond
    sum_=0
    for i in lst_groups:
        sum_+=len(df_input[df_input['condition']==i])
        print(len(df_input[df_input['condition']==i]))
    print(sum_)
    return df_input, lst_groups

# time_exem: plan, execution
# type_graph: time_diff
def get_graphs(df,time_exem, type_graph, path, iteration):
    if type_graph=='time_both':
        ox = df['query_name']
        df,lst_groups = form_conditions(df.copy(),time_exem)
        for elem in lst_groups:
            fig = go.Figure()
            df_cond = df[df['condition']==elem]
            digits=re.findall(r'(\d+)', elem)
            if 'less' in elem:
                name='Время выполнения запроса с AQO и без от -{} до -{} разницей'.format(digits[0], digits[1])
                filename='{}_less{}_{}'.format(time_exem,digits[0], digits[1])
            else:
                name='Время выполнения запроса с AQO и без от {} до {} разницей'.format(digits[0], digits[1])
                filename='{}_much{}_{}'.format(time_exem,digits[0], digits[1])
            fig.add_trace(go.Bar(name='control', x=df_cond['query_name'], y=np.log10(df_cond['{}_time_control'.format(time_exem)]), text=round(df_cond['{}_time_control'.format(time_exem)],2)))
            fig.add_trace(go.Bar(name = 'disable', x=df_cond['query_name'], y=np.log10(df_cond['{}_time_disabled'.format(time_exem)]), text=round(df_cond['{}_time_disabled'.format(time_exem)],2)))
            fig.update_layout(title = name, width=w, height = h)
            upload_pics(fig, '{}/{}_folder{}'.format(path, 'frozen',iteration), filename)
            #fig.show()
    elif type_graph=='time_diff':
        ox = df['query_name']
        df,lst_groups = form_conditions(df.copy(),time_exem)
        for elem in lst_groups:
            fig = go.Figure()
            df_cond = df[df['condition']==elem]
            digits=re.findall(r'(\d+)', elem)
            if 'less' in elem:
                name='Разница времени выполнения с AQO и без от -{} до -{} разницей'.format(digits[0], digits[1])
                filename='diff_{}_less{}_{}'.format(time_exem,digits[0], digits[1])
            else:
                name='Разница времени выполнения с AQO и без от {} до {} разницей'.format(digits[0], digits[1])
                filename='diff_{}_much{}_{}'.format(time_exem,digits[0], digits[1])
            fig.add_trace(go.Bar(x = ox, y = df_cond['{}_time_disabled'.format(time_exem)]-df_cond['{}_time_control'.format(time_exem)], text=round(df_cond['{}_time_disabled'.format(time_exem)] - df_cond['{}_time_control'.format(time_exem)],2), textposition='outside'))
            fig.update_yaxes(zeroline=True, zerolinewidth=3, zerolinecolor='red')
            fig.update_layout(legend_orientation="h",
                              legend=dict(x=.5, xanchor="center"),
                              title=name,
                              xaxis_title="Имя файлов запросов",
                              yaxis_title="Разница времени выполнения",
                              margin=dict(l=0, r=0, t=50, b=0))
            fig.update_layout(width=w, height = h)
            upload_pics(fig, '{}/{}_folder{}'.format(path, 'frozen',iteration), filename)
    elif type_graph=='how_much_time_increased':
        ox = df['query_name']
        fig = go.Figure()
        if time_exem=='execution':
            name = "Во сколько раз вемя выполнения запроса с AQO превосходит без AQO"
        if time_exem=='plan':
            name = "Во сколько раз вемя планирования запроса с AQO превосходит без AQO"
        filename='{}_how_much'.format(time_exem)
        fig.add_trace(go.Scatter(x = ox, y = df['{}_time_disabled'.format(time_exem)]/df['{}_time_control'.format(time_exem)]))
        fig.add_trace(go.Scatter(x = ox, y = [1]*len(df['{}_time_disabled'.format(time_exem)])))
        fig.add_trace(go.Scatter(x = ox, y = [2]*len(df['{}_time_disabled'.format(time_exem)])))
        fig.update_yaxes(zeroline=True, zerolinewidth=3, zerolinecolor='red')
        fig.update_layout(legend_orientation="h",
                          legend=dict(x=.5, xanchor="center"),
                          title=name,
                          xaxis_title="Имя файлов запросов",
                          yaxis_title="Значение",
                          margin=dict(l=0, r=0, t=50, b=0))
        fig.update_layout(width=w, height = h)
        upload_pics(fig, '{}/{}_folder{}'.format(path, 'frozen',iteration), filename)

#def analyze_error(path, mode):

def draw_stats_queries_with_least_error(df_copy, path, iter_, diff):
    df_stat=df_copy.copy()
    df_stat['queryid'] = df_stat['queryid'].astype(str)
    lst_min_val_with_aqo = []
    lst_min_iter_with_aqo = []
    for i in df_stat.itertuples(index=False):
        min_val = 100000
        iteration = -1
        for k,val in enumerate(i.cardinality_error_with_aqo_split):
            if val < 0.1:
                min_val = val
                iteration = k
                break
        lst_min_val_with_aqo.append(min_val)
        lst_min_iter_with_aqo.append(iteration)
    df_stat['min_iter_card_with'] = lst_min_iter_with_aqo
    df_stat['lst_min_val_with_aqo'] = lst_min_val_with_aqo
    oy=['not derived less error with 0.1','derived less error with 0.1']
    ox=[len(df_stat[df_stat['min_iter_card_with']==-1]),len(df_stat[df_stat['min_iter_card_with']>-1])]
    fig = go.Figure()
    fig = px.bar(x=ox, y=oy)
    fig.update_layout(legend_orientation="h",
                  legend=dict(x=.5, y = 0.4, xanchor="center"),
                  title="Сколько запросов достигло порога ошибки менее 0.1",
                  xaxis_title="Количество запросов",
                  margin=dict(l=0, r=0, t=50, b=0))
    upload_pics(fig, '{}/{}_folder{}'.format(path, 'frozen',iter_), 'aqo_stats_queries_with_less_error_{}'.format(diff))

def division_main_stats_graphs(df, col):
    df=df.sort_values(col)
    lst_cond=[]
    lst_contain=[0, 0, 0, 0,0]
    for i in df[col]:
        if lst_contain[0]<25:
            lst_cond.append('df_less0_15')
            lst_contain[0]+=1
        elif lst_contain[1]<25:
            lst_cond.append('df_less15_30')
            lst_contain[1]+=1
        elif lst_contain[2]<25:
            lst_cond.append('df_less30_60')
            lst_contain[2]+=1
        elif lst_contain[3]<25:
            lst_cond.append('df_less60_80')
            lst_contain[3]+=1
        else:
            lst_cond.append('df_less80_100')
            lst_contain[4]+=1
    df['condition']=lst_cond
    return df

def draw_aqo_stats_queries_iteration_convergence(df_copy, path, iter_):
    df_stat=df_copy.copy()
    lst_min_card_val_with_aqo = []
    lst_min_exec_val_with_aqo = []
    lst_min_card_val_without_aqo = []
    lst_min_exec_val_without_aqo = []
    lst_min_plan_val_with_aqo = []
    lst_min_plan_val_without_aqo = []
    lst_min_card_iter_with_aqo = []
    lst_min_exec_iter_with_aqo = []
    lst_min_plan_iter_with_aqo = []
    for i in df_stat.itertuples(index=False):
        min_val = 100000
        iteration = -1
        for k,val in enumerate(i.cardinality_error_with_aqo_split):
            if min_val>val:
                min_val = val
                iteration = k
        lst_min_card_val_with_aqo.append(min_val)
        lst_min_card_iter_with_aqo.append(iteration)
        min_val = 100000
        for k,val in enumerate(i.cardinality_error_without_aqo_split):
            if min_val>val:
                min_val = val
        lst_min_card_val_without_aqo.append(min_val)
        min_val = 100000
        iteration = -1
        for k,val in enumerate(i.execution_time_with_aqo_split):
            if min_val>val:
                min_val = val
                iteration = k
        lst_min_exec_val_with_aqo.append(min_val)
        lst_min_exec_iter_with_aqo.append(iteration)
        min_val = 100000
        for k,val in enumerate(i.execution_time_without_aqo_split):
            if min_val>val:
                min_val = val
        lst_min_exec_val_without_aqo.append(min_val)
        min_val = 100000
        iteration = -1
        for k,val in enumerate(i.planning_time_with_aqo_split):
            if min_val>val:
                min_val = val
                iteration = k
        lst_min_plan_val_with_aqo.append(min_val)
        lst_min_plan_iter_with_aqo.append(iteration)
        min_val = 100000
        for k,val in enumerate(i.planning_time_without_aqo_split):
            if min_val>val:
                min_val = val
        lst_min_plan_val_without_aqo.append(min_val)
    df_stat['min_val_card_with'] = lst_min_card_val_with_aqo
    df_stat['min_val_exec_with'] = lst_min_exec_val_with_aqo
    df_stat['min_val_plan_with'] = lst_min_plan_val_with_aqo
    df_stat['min_val_card_without'] = lst_min_card_val_without_aqo
    df_stat['min_val_exec_without'] = lst_min_exec_val_without_aqo
    df_stat['min_val_plan_without'] = lst_min_plan_val_without_aqo
    df_stat['min_iter_card_with'] = lst_min_card_iter_with_aqo
    df_stat['min_iter_exec_with'] = lst_min_exec_iter_with_aqo
    df_stat['min_iter_plan_with'] = lst_min_plan_iter_with_aqo

    df_stat['queryid'] = df_stat['queryid'].astype(str)
    df_stat = division_main_stats_graphs(df_stat, 'min_val_card_with')
    for i in ['df_less0_15','df_less15_30','df_less30_60','df_less60_80', 'df_less80_100']:
        get_graphics(df_stat[df_stat['condition']==i], path, iter_,i)

def get_graphics(df_stat, path, iter_, diff):
    fig = go.Figure()
    fig.add_trace(go.Scatter(name='Итерация с минимальной кардинальностью с aqo', x = df_stat['query_name'].to_list(), y = df_stat['min_iter_card_with'].to_list()))
    fig.add_trace(go.Scatter(name='Кардинальность с aqo', x = df_stat['query_name'].to_list(), y = df_stat['min_val_card_with'].to_list()))
    fig.add_trace(go.Scatter(name='Кардинальность без aqo', x = df_stat['query_name'].to_list(), y = df_stat['min_val_card_without'].to_list()))
    #fig.add_trace(go.Scatter(x = ox, y = [-1]*len(df_stat['min_iter_card_with'])))
    #fig.add_trace(go.Scatter(x = ox, y = [1]*len(df_stat['min_iter_card_with'])))
    #fig.add_trace(go.Scatter(x = ox, y = [3]*len(df_stat['min_iter_card_with'])))
    #fig.add_trace(go.Scatter(x = ox, y = [5]*len(df_stat['min_iter_card_with'])))
    fig.update_layout(legend_orientation="h",
                  legend=dict(x=.5, y = 0.4, xanchor="center"),
                  title="На какой итерации сходимость и сравнение кардинальностей",
                  xaxis_title="Хеши запросов",
                  yaxis_title="Значение",
                  margin=dict(l=0, r=0, t=50, b=0))
    fig.update_layout(width=w, height = h)
    upload_pics(fig, '{}/{}_folder{}'.format(path, 'frozen',iter_), 'aqo_stats_queries_iter_vals_convergence_{}'.format(diff))

    fig = go.Figure()
    fig.add_trace(go.Scatter(name='Кардинальность с aqo', x = df_stat['query_name'].to_list(), y = df_stat['min_val_card_with'].to_list()))
    fig.add_trace(go.Scatter(name='Время выполнения c aqo', x = df_stat['query_name'].to_list(), y = df_stat['min_val_exec_with'].to_list()))
    fig.add_trace(go.Scatter(name='Время планирования c aqo', x = df_stat['query_name'].to_list(), y = df_stat['min_val_plan_with'].to_list()))
    #fig.add_trace(go.Scatter(x = ox, y = [-1]*len(df_stat['min_iter_card_with'])))
    #fig.add_trace(go.Scatter(x = ox, y = [1]*len(df_stat['min_iter_card_with'])))
    #fig.add_trace(go.Scatter(x = ox, y = [3]*len(df_stat['min_iter_card_with'])))
    #fig.add_trace(go.Scatter(x = ox, y = [5]*len(df_stat['min_iter_card_with'])))
    fig.update_layout(legend_orientation="h",
                  legend=dict(x=.5, y = 0.4, xanchor="center"),
                  title="Сравнение кардинальностей и времени планирования и выполнения запросов",
                  xaxis_title="Хеши запросов",
                  yaxis_title="Значение",
                  margin=dict(l=0, r=0, t=50, b=0))
    fig.update_layout(width=w, height = h)
    upload_pics(fig, '{}/{}_folder{}'.format(path, 'frozen',iter_), 'aqo_stats_queries_vals_convergence_{}'.format(diff))

    fig = go.Figure()
    fig.add_trace(go.Scatter(name='Время выполнения с aqo', x = df_stat['query_name'].to_list(), y = df_stat['min_val_exec_with'].to_list()))
    fig.add_trace(go.Scatter(name='Время планирования c aqo', x = df_stat['query_name'].to_list(), y = df_stat['min_val_plan_with'].to_list()))
    fig.add_trace(go.Scatter(name='Время выполнения без aqo', x = df_stat['query_name'].to_list(), y = df_stat['min_val_exec_without'].to_list()))
    fig.add_trace(go.Scatter(name='Время планирования без aqo', x = df_stat['query_name'].to_list(), y = df_stat['min_val_plan_without'].to_list()))
    fig.update_layout(legend_orientation="h",
                  legend=dict(x=.5, y = 0.4, xanchor="center"),
                  title="Сравнение времени выполнения и планирования",
                  xaxis_title="Хеши запросов",
                  yaxis_title="Значение",
                  margin=dict(l=0, r=0, t=50, b=0))
    fig.update_layout(width=w, height = h)
    upload_pics(fig, '{}/{}_folder{}'.format(path, 'frozen',iter_), 'aqo_stats_queries_vals_times_{}'.format(diff))


def draw_aqo_stats_queries_difference(df_copy, path, iter_):
    df_stat=df_copy.copy()
    df_stat['queryid'] = df_stat['queryid'].astype(str)
    lst_columns = ['cardinality_error_without_aqo_split', 'cardinality_error_with_aqo_split']
    lst_columns_with = ['planning_time_with_aqo_split', 'execution_time_with_aqo_split']
    lst_columns_without = ['planning_time_without_aqo_split', 'execution_time_without_aqo_split']
    for i in lst_columns:
        df_stat_sum = functions.last_errors(df_stat, i)
    for i in lst_columns_with:
        df_stat_sum = functions.sum_errors(df_stat, i, 'with')
    for i in lst_columns_without:
        df_stat_sum = functions.sum_errors(df_stat, i, 'without')
    df_stat = division_main_stats_graphs(df_stat, 'cardinality_error_with_aqo_split')
    for i in ['df_less0_15','df_less15_30','df_less30_60','df_less60_80', 'df_less80_100']:
        draw_aqo_stats_queries_cardinality_difference(df_stat[df_stat['condition']==i], path, iter_, i)
    df_stat = division_main_stats_graphs(df_stat, 'planning_time_with_aqo_split')
    for i in ['df_less0_15','df_less15_30','df_less30_60','df_less60_80', 'df_less80_100']:
        draw_aqo_stats_queries_plan_time(df_stat[df_stat['condition']==i], path, iter_, i)
    df_stat = division_main_stats_graphs(df_stat, 'execution_time_with_aqo_split')
    for i in ['df_less0_15','df_less15_30','df_less30_60','df_less60_80', 'df_less80_100']:
        draw_aqo_stats_queries_exec_diff(df_stat[df_stat['condition']==i], path, iter_, i)

def draw_aqo_stats_queries_cardinality_difference(df_copy, path, iter_, diff):
    df_stat_sum=df_copy.copy()
    df_stat_sum['queryid'] = df_stat_sum['queryid'].astype(str)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x = df_stat_sum['query_name'], y = [3]*len(df_stat_sum['cardinality_error_with_aqo_split'])))
    fig.add_trace(go.Scatter(x = df_stat_sum['query_name'], y = [-1]*len(df_stat_sum['cardinality_error_with_aqo_split'])))
    fig.add_trace(go.Scatter(x = df_stat_sum['query_name'], y = [1]*len(df_stat_sum['cardinality_error_with_aqo_split'])))
    fig.add_trace(go.Bar(name = 'without AQO', x=df_stat_sum['query_name'],
                        y=df_stat_sum['cardinality_error_without_aqo_split']-df_stat_sum['cardinality_error_with_aqo_split'],
                        text=round(df_stat_sum['cardinality_error_without_aqo_split']-df_stat_sum['cardinality_error_with_aqo_split'],2),
                        textposition='outside'))
    fig.update_layout(barmode='stack', width=w, height = h, title="Разница ошибки кардинальности",
                      xaxis_title="Хеши запросов",
                      yaxis_title="Значение",)
    upload_pics(fig, '{}/{}_folder{}'.format(path, 'frozen',iter_), 'aqo_stats_queries_cardinality_difference_{}'.format(diff))

def draw_aqo_stats_queries_plan_time(df_copy, path, iter_, diff):
    df_stat_sum=df_copy.copy()
    df_stat_sum['queryid'] = df_stat_sum['queryid'].astype(str)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x = df_stat_sum['query_name'], y = [0.1]*len(df_stat_sum['planning_time_without_aqo_split'])))
    fig.add_trace(go.Scatter(x = df_stat_sum['query_name'], y = [-0.1]*len(df_stat_sum['planning_time_without_aqo_split'])))
    fig.add_trace(go.Scatter(x = df_stat_sum['query_name'], y = [0]*len(df_stat_sum['planning_time_without_aqo_split'])))
    fig.add_trace(go.Bar(name='with AQO', x=df_stat_sum['query_name'], y=df_stat_sum['planning_time_without_aqo_split']-df_stat_sum['planning_time_with_aqo_split'],
                        text=round(df_stat_sum['planning_time_without_aqo_split']-df_stat_sum['planning_time_with_aqo_split'],4), textposition='outside'))
    fig.update_layout(barmode='stack', width=w, height = h, title="Ошибка во времени планирования запросов",
                      xaxis_title="Хеши запросов",
                      yaxis_title="Значение",)
    upload_pics(fig, '{}/{}_folder{}'.format(path, 'frozen',iter_), 'aqo_stats_queries_plan_time_{}'.format(diff))

def draw_aqo_stats_queries_exec_diff(df_copy, path, iter_, diff):
    df_stat_sum=df_copy.copy()
    df_stat_sum['queryid'] = df_stat_sum['queryid'].astype(str)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x = df_stat_sum['query_name'], y = [2]*len(df_stat_sum['execution_time_without_aqo_split'])))
    fig.add_trace(go.Scatter(x = df_stat_sum['query_name'], y = [-1]*len(df_stat_sum['execution_time_without_aqo_split'])))
    fig.add_trace(go.Scatter(x = df_stat_sum['query_name'], y = [1]*len(df_stat_sum['execution_time_without_aqo_split'])))
    fig.add_trace(go.Bar(name = 'without AQO', x=df_stat_sum['query_name'], y=df_stat_sum['execution_time_without_aqo_split']-df_stat_sum['execution_time_with_aqo_split'],
                        text=round(df_stat_sum['execution_time_without_aqo_split']-df_stat_sum['execution_time_with_aqo_split'],2), textposition='outside'))
    fig.update_layout(barmode='stack', width=w, height = h, title="Разница ошибки во времени выполнения запросов",
                      xaxis_title="Хеши запросов",
                      yaxis_title="Значение",)
    upload_pics(fig, '{}/{}_folder{}'.format(path, 'frozen',iter_), 'aqo_stats_queries_exec_diff_{}'.format(diff))

def det_analyze_statistic(df_orig, path, mode, iter_):
    df_stat_copy = pd.read_csv('{}/{}_aqo_query_stat.csv'.format('{}/{}_folder{}'.format(path, 'frozen',iter_), mode))
    lst_stat_columns = ['execution_time_with_aqo', 'execution_time_without_aqo',
       'planning_time_with_aqo', 'planning_time_without_aqo',
       'cardinality_error_with_aqo', 'cardinality_error_without_aqo']
    lst_stat_cut = [1, 1, 1, 1, 1, 1]
    df_stat = get_preprocess_dataframe(df_stat_copy, lst_stat_columns, lst_stat_cut)

    sLength = len(df_stat['queryid'])
    df_stat['query_name'] = pd.Series(np.random.randn(sLength), index=df_stat.index)
    lst={}
    df_stat['queryid'] = df_stat['queryid'].astype(str)
    df_orig['query_hash_x'] = df_orig['query_hash_x'].astype(str)
    #df_stat['query_name']='0'*len(df_stat)
    for j in df_orig.itertuples(index=False):
        if j.query_hash_x not in lst:
            lst[j.query_hash_x]=[]
            lst[j.query_hash_x].append(j.query_name)
        else:
            lst[j.query_hash_x].append(j.query_name)
    dictionary={'queryid':[], 'query_name':[]}
    for key,value in lst.items():
        dictionary['queryid'].append(key)
        dictionary['query_name'].append(value)

    df1 = pd.DataFrame(list(lst.items()), columns=['queryid', 'query_name'])
    df_stat=df_stat.merge(df1, how='left', on='queryid')
    df_stat=df_stat.drop(['query_name_x'], axis=1)
    df_stat=df_stat.rename(columns={"query_name_y": "query_name"})
    df_stat['query_name'] = df_stat['query_name'].astype(str)

    draw_aqo_stats_queries_difference(df_stat, path, iter_)
    draw_aqo_stats_queries_iteration_convergence(df_stat, path, iter_)

    df_stat = division_main_stats_graphs(df_stat, 'cardinality_error_with_aqo_split')
    for i in ['df_less0_15','df_less15_30','df_less30_60','df_less60_80', 'df_less80_100']:
        draw_stats_queries_with_least_error(df_stat[df_stat['condition']==i], path, iter_, i)


def get_analyzes(iteration, path, learn_iter):
    df = forming_pdf(iteration, path, learn_iter)
    #get_graphs(df,'execution', 'time_both', path,iteration)
    #get_graphs(df,'plan', 'time_both', path,iteration)
    #get_graphs(df,'plan', 'time_diff', path,iteration)
    #get_graphs(df,'execution', 'time_diff', path,iteration)
    #get_graphs(df,'execution', 'how_much_time_increased', path,iteration)
    #get_graphs(df,'plan', 'how_much_time_increased', path,iteration)
    det_analyze_statistic(df, path, 'frozen',iteration)



if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument('-i', '--iter_path', type=int,
        help='Option which defines iterable number')
    parser.add_argument('-p', '--path', type=str,
        help='Option which defines path with saved data')
    parser.add_argument('-l', '--learn_iter', type=int,
        help='Option which defines learn number of iteration')
    args = parser.parse_args()
    get_analyzes(args.iter_path, args.path, args.learn_iter)