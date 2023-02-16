INSTDIR=/home/alena/postgrespro20/tmp_install/bin
# AQO specific settings
$INSTDIR/psql -c "ALTER SYSTEM SET aqo.mode = 'learn'"
$INSTDIR/psql -c "ALTER SYSTEM SET aqo.force_collect_stat = 'on'"
$INSTDIR/psql -c "ALTER SYSTEM SET aqo.show_details = 'on'"
$INSTDIR/psql -c "ALTER SYSTEM SET aqo.show_hash = 'on'"
$INSTDIR/psql -c "ALTER SYSTEM SET aqo.join_threshold = 0"
$INSTDIR/psql -c "ALTER SYSTEM SET aqo.wide_search = 'off'"

# Core settings: force parallel workers
$INSTDIR/psql -c "ALTER SYSTEM SET max_parallel_workers_per_gather = 8"
$INSTDIR/psql -c "ALTER SYSTEM SET force_parallel_mode = 'on'"
$INSTDIR/psql -c "ALTER SYSTEM SET from_collapse_limit = 16"
$INSTDIR/psql -c "ALTER SYSTEM SET join_collapse_limit = 16"
$INSTDIR/psql -c "ALTER SYSTEM SET parallel_setup_cost = 1.0"
$INSTDIR/psql -c "ALTER SYSTEM SET parallel_tuple_cost = 0.00001"
$INSTDIR/psql -c "ALTER SYSTEM SET min_parallel_table_scan_size = 0"
$INSTDIR/psql -c "ALTER SYSTEM SET min_parallel_index_scan_size = 0"

# pg_stat_statements
$INSTDIR/psql -c "ALTER SYSTEM SET pg_stat_statements.track = 'all'"
$INSTDIR/psql -c "ALTER SYSTEM SET pg_stat_statements.track_planning = 'on'"

$INSTDIR/psql -c "SELECT pg_reload_conf();"