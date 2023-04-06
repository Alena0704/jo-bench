INSTDIR=/home/alena/postgrespro37_job/tmp_install/bin
export PGDATA=/home/alena/postgres_data_job
# AQO specific settings
$INSTDIR/psql -c "ALTER SYSTEM SET aqo.mode = 'learn'"
$INSTDIR/psql -c "ALTER SYSTEM SET aqo.force_collect_stat = 'on'"
$INSTDIR/psql -c "ALTER SYSTEM SET aqo.show_details = 'on'"
$INSTDIR/psql -c "ALTER SYSTEM SET aqo.show_hash = 'on'"
#$INSTDIR/psql -c "ALTER SYSTEM SET aqo.join_threshold = 4"
#$INSTDIR/psql -c "ALTER SYSTEM SET aqo.wide_search = 'off'"

# pg_stat_statements
$INSTDIR/psql -c "ALTER SYSTEM SET pg_stat_statements.track = 'all'"
$INSTDIR/psql -c "ALTER SYSTEM SET pg_stat_statements.track_planning = 'on'"
$INSTDIR/psql -c "ALTER SYSTEM SET min_parallel_table_scan_size = 4"
$INSTDIR/psql -c "ALTER SYSTEM SET min_parallel_index_scan_size = 4"
$INSTDIR/psql -c "ALTER SYSTEM SET max_parallel_workers_per_gather = 8"
$INSTDIR/psql -c "ALTER SYSTEM SET max_parallel_maintenance_workers = 8"	# taken from max_parallel_workers

$INSTDIR/psql -c "SELECT pg_reload_conf();"
