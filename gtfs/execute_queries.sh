#!/bin/bash
# ./execute_queries.sh /Users/lgu/workspace/SPARQLAnything/sparql.anything/sparql-anything-cli/target/sparql-anything-0.8.0-SNAPSHOT.jar "1" "json" "test"

SPARQL_ANYTHING_JAR=$1
RESULTS_DIR=$(pwd)/$4

if [ ! -d $RESULTS_DIR ]; then
  mkdir $RESULTS_DIR
else
  echo "$RESULTS_DIR alredy exists!"
fi

source functions.sh

if [ -n "$5" ]; then
  QUERIES_TO_EXECUTE=$5
else
  QUERIES_TO_EXECUTE="1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18"
fi


for format in $3
do
  for size in $2
  do
    for query in $QUERIES_TO_EXECUTE
    do
      echo "Monitoring q$query strategy0 no_slice size $size $format"
      monitor-query $size "q$query" "strategy0" "no_slice" $format
      echo "Monitoring q$query strategy1 no_slice size $size $format"
      monitor-query $size "q$query" "strategy1" "no_slice" $format
      echo "Monitoring q$query strategy0 slice size $size $format"
      monitor-query $size "q$query" "strategy0" "slice" $format
      echo "Monitoring q$query strategy1 slice size $size $format"
      monitor-query $size "q$query" "strategy1" "slice" $format

      # ON_DISK
      echo "Monitoring q$query strategy0 no_slice size $size $format ondisk"
      monitor-query $size "q$query" "strategy0" "no_slice" $format "ondisk"
      echo "Monitoring q$query strategy1 no_slice size $size $format ondisk"
      monitor-query $size "q$query" "strategy1" "no_slice" $format "ondisk"
      echo "Monitoring q$query strategy0 slice size $size $format ondisk"
      monitor-query $size "q$query" "strategy0" "slice" $format "ondisk"
      echo "Monitoring q$query strategy1 slice size $size $format ondisk"
      monitor-query $size "q$query" "strategy1" "slice" $format "ondisk"
    done
  done
done






#cd $SPARQL_ANYTHING_QUERY_FOLDER

#java -jar $SPARQL_ANYTHING_JAR -q q1.sparql > /dev/null
#java -jar /Users/lgu/workspace/spice/sparql.anything/sparql-anything-cli/target/sparql-anything-0.7.0-SNAPSHOT.jar -q
