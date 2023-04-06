INSTDIR=/home/alena/postgrespro37_job/tmp_install/bin
export PGDATA=/home/alena/postgres_data_job
# AQO specific settings
$INSTDIR/psql -c "ALTER SYSTEM SET aqo.mode = 'frozen'"
$INSTDIR/psql -c "ALTER SYSTEM SET aqo.force_collect_stat = 'off'"
$INSTDIR/psql -c "ALTER SYSTEM SET aqo.show_details = 'on'"
$INSTDIR/psql -c "ALTER SYSTEM SET aqo.show_hash = 'on'"

# pg_stat_statements
$INSTDIR/psql -c "ALTER SYSTEM SET pg_stat_statements.track = 'all'"
$INSTDIR/psql -c "ALTER SYSTEM SET pg_stat_statements.track_planning = 'on'"

$INSTDIR/psql -c "SELECT pg_reload_conf();"