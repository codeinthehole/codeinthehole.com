#! /bin/bash
#
# Get statistics from MySQL and feed them into Ganglia for monitoring.
#
# To use, simply adjust the path to gmetric and mysql credentials as appropriate.
#
# Author: David Winterbottom (david.winterbottom@gmail.com)
# Site:   http://codeinthehole.com

# Config
declare -r GMETRIC=/usr/bin/gmetric
declare -r NEW_DATA_FILE=/tmp/mysql-stats.new
declare -r OLD_DATA_FILE=/tmp/mysql-stats.old
declare -r MYSQL_USER="root"
declare -r MYSQL_PASSWORD="insert-password-here"

# Sanity checks
if test -z "$GMETRIC" ; then
    printf "The command $GMETRIC is not available";
    exit 192
fi

# Function for submiting metrics
function record_value
{
    if [ $# -lt 1 ]; then
        printf "You must specify a look-up value\n"
        exit 192
    fi
    LOOKUP_VAR=$1
    GANGLIA_NAME=${2-unspecified}
    GANGLIA_TYPE=${3-float}
    GANGLIA_UNITS=${4-units}
    GANGLIA_VALUE=`grep "$LOOKUP_VAR[^_]" "$NEW_DATA_FILE" | awk '{print $2}'`
    printf " * $GANGLIA_NAME: $GANGLIA_VALUE\n"
    $GMETRIC --type "$GANGLIA_TYPE" --name "$GANGLIA_NAME" --value $GANGLIA_VALUE --unit "$GANGLIA_UNITS"
}

# Function for submitting delta metrics
function record_value_rate
{
    if [ $# -lt 1 ]; then
        printf "You must specify a look-up value\n"
        exit 192
    fi
    MYSQL_VAR=$1
    GANGLIA_NAME=${2-unspecified}
    GANGLIA_TYPE=${3-float}
    GANGLIA_UNITS=${4-"per second"}

    # Get values from old and new files
    PREVIOUS_VALUE=`grep "$MYSQL_VAR[^_]" "$OLD_DATA_FILE" | awk '{print $2}'`
    NEW_VALUE=`grep "$MYSQL_VAR[^_]" "$NEW_DATA_FILE" | awk '{print $2}'`
    DELTA_VALUE=$[ $NEW_VALUE-$PREVIOUS_VALUE ]
    PREVIOUS_TIMESTAMP=`date -r "$OLD_DATA_FILE" +%s`
    NEW_TIMESTAMP=`date -r "$NEW_DATA_FILE" +%s`
    DELTA_TIMESTAMP=$[ $NEW_TIMESTAMP-$PREVIOUS_TIMESTAMP ]
    if [ $DELTA_VALUE -lt 0 ] || [ $DELTA_TIMESTAMP -lt 0 ]; then
        # Something strange here - MYSQL may just have started.  Ignore for now
        printf "Weird data value - skipping\n"
    else
        # Need to pipe to bc to perform floating point operations
        DELTA_RATE=`echo "scale=4; $DELTA_VALUE/$DELTA_TIMESTAMP" | bc -l`
        printf " * $GANGLIA_NAME -- Previous value: $PREVIOUS_VALUE, new value: $NEW_VALUE, delta: $DELTA_VALUE, previous timestamp: $PREVIOUS_TIMESTAMP, new timestamp: $NEW_TIMESTAMP, delta: $DELTA_TIMESTAMP, $DELTA_RATE per second\n"
        $GMETRIC --type "$GANGLIA_TYPE" --name "$GANGLIA_NAME" --value $DELTA_VALUE --unit "$GANGLIA_UNITS"
    fi
}

# Read MySQL statistics into a temporary file
mysql --user=$MYSQL_USER --password=$MYSQL_PASSWORD --execute "SHOW GLOBAL STATUS" > "$NEW_DATA_FILE"

# Submit metrics
record_value_rate "Connections" "MYSQL_CONNECTIONS" "float" "Connections/sec"
record_value_rate "Com_update" "MYSQL_UPDATE_QUERIES" "float" "Queries/sec"
record_value_rate "Com_select" "MYSQL_SELECT_QUERIES" "float" "Queries/sec"
record_value_rate "Com_insert" "MYSQL_INSERT_QUERIES" "float" "Queries/sec"
record_value_rate "Com_delete" "MYSQL_DELETE_QUERIES" "float" "Queries/sec"
record_value_rate "Created_tmp_tables" "MYSQL_CREATED_TMP_TABLES" "float" "Tables created/sec"
record_value_rate "Slow_queries" "MYSQL_SLOW_QUERIES" "float" "Queries/sec" 
record_value_rate "Qcache_hits" "MYSQL_QUERY_CACHE_HITS" "float" "Hits/sec"
record_value "Qcache_queries_in_cache" "MYSQL_QUERIES_IN_CACHE" "float" "Queries"
record_value_rate "Questions" "MYSQL_QUESTIONS" "float" "Questions/sec"
record_value_rate "Threads_connected" "MYSQL_THREADS_CONNECTED" "float" "Threads connected/sec"
record_value "Threads_running" "MYSQL_THREADS_RUNNING" "float" "Threads running"

# Copy data
cp "$NEW_DATA_FILE" "$OLD_DATA_FILE"