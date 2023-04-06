INSTDIR=/home/alena/postgrespro37_job/tmp_install/bin
export PGDATA=/home/alena/postgres_data_job
$INSTDIR/psql -c "ALTER SYSTEM SET aqo.mode = 'disabled'"
$INSTDIR/psql -c "ALTER SYSTEM SET aqo.force_collect_stat = 'on'"
$INSTDIR/psql -c "ALTER SYSTEM SET aqo.show_details = 'on'"
$INSTDIR/psql -c "ALTER SYSTEM SET aqo.show_hash = 'on'"

# Core settings: force parallel workers
#$INSTDIR/psql -c "ALTER SYSTEM SET max_parallel_workers_per_gather = 8"
#$INSTDIR/psql -c "ALTER SYSTEM SET force_parallel_mode = 'on'"
#$INSTDIR/psql -c "ALTER SYSTEM SET from_collapse_limit = 8"
#$INSTDIR/psql -c "ALTER SYSTEM SET join_collapse_limit = 8"
#$INSTDIR/psql -c "ALTER SYSTEM SET cpu_operator_cost = 0.0025"
#$INSTDIR/psql -c "ALTER SYSTEM SET cpu_index_tuple_cost = 0.005"
#$INSTDIR/psql -c "ALTER SYSTEM SET cpu_tuple_cost = 0.01"
#$INSTDIR/psql -c "ALTER SYSTEM SET random_page_cost = 1.1"
#$INSTDIR/psql -c "ALTER SYSTEM SET parallel_setup_cost = 1.0"
#$INSTDIR/psql -c "ALTER SYSTEM SET parallel_setup_cost = 1000.0"
#$INSTDIR/psql -c "ALTER SYSTEM SET parallel_tuple_cost = 0.00001"
#$INSTDIR/psql -c "ALTER SYSTEM SET parallel_tuple_cost = 0.1"
#$INSTDIR/psql -c "ALTER SYSTEM SET min_parallel_table_scan_size = 0"
#$INSTDIR/psql -c "ALTER SYSTEM SET min_parallel_index_scan_size = 0"
#$INSTDIR/psql -c "ALTER SYSTEM SET min_parallel_table_scan_size = 8MBMB"
#$INSTDIR/psql -c "ALTER SYSTEM SET min_parallel_index_scan_size = 512"
# pg_stat_statements
$INSTDIR/psql -c "ALTER SYSTEM SET pg_stat_statements.track = 'all'"
$INSTDIR/psql -c "ALTER SYSTEM SET pg_stat_statements.track_planning = 'on'"

$INSTDIR/psql -c "select aqo_reset();"

$INSTDIR/psql -c "SELECT pg_reload_conf();"