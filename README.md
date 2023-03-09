# join-order-benchmark

This repository is a fork of the [project](https://github.com/gregrahn/join-order-benchmark).
Here we unite queries and data in one place.
Main goal of this repository is simplifying of the deploy process.

Large tables divided into chunks each less than 100 MB.

Repository contains some scripts for quick deploy & run of the benchmark:
* *schema.sql* - creates the data schema.
* *copy.sql* - copies data from csv files into the tables. Uses `datadir` variable to make absolute paths to csv files. Use `psql -v` to define it.
* *parts.sql* - script which splitted the tables. Just for future reusage.
* *job* - a template script for quick launch of the benchmark.

Example below shows export procedure of all tables:

```
psql -f ~/jo-bench/schema.sql
psql -vdatadir="'/home/user/jo-bench'" -f ~/jo-bench/copy.sql
```
All scripts and files are stored in the source folder.

# Addition files
aqo_analyze folder contains notebooks for analyzing job results tests within graphs and diagrams, also base scripts for running tests.
files for run JOB test:
    First of all, run jo-create file for creating base, however you should change path for environment for his correctly working:
    ```
    INSTDIR - folder with your files postgresql
    QUERY_DIR - folder with your JOB queries files
    QUERY_DIR_TEST - folder with your extended JOB queries files
    PGDATA - folder PGDATA for postgresql instanse

    run it with command: bash jo-create
    ```
    Secondly, run job_test and change environment variable in there too.
    We have one global setting file for set up postgresql and three scripts for set up settings for aqo in different modes:
    setup_main_settigs.sh
    setup_disabled_settings.sh
    setup_learn_settings.sh
    setup_forced_settings.sh

files for aqo analyze:
    script_anayze.py contains script for automatic built necessary graphs (in process)
    functions.py contains necessary functions for calculated datasets
    preprocess_dataframe.py contains preprocessing sourced datasets from given csv files in the more respectable view
    script_clean.ipynb - example code for analyze or experiments
If you want to use python scripts you should install libraries:
    pandas, numpy, plotly, re, os, glob, argparse, math.
    Sorry, more information will be presented lately.

files for sr_plan testing:
    job_create - is the same file as previous jo-create, only used for sr_plan testing.
    job-sr_plan - contains scripts with two stages: registrate and freeze queries before measuring time planning and executes query.
    job-sr_plan_invalidate - invalidate or replaning plans for queries with extra stages.
    regitser_template - it is the different way for testing sr_plan: we try to register query template and freeze it by it's identifiers.
    job-sr_plan_after_registrated - script for testing sr_plan after having registrated its templates.
    test1.sql - prepared sql scripts for registrated query templates.



