#!/bin/bash
#
# Copyright (c) 2022 SPARQL Anything Contributors @ http://github.com/sparql-anything
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

# ./execute_queries.sh /Users/lgu/workspace/SPARQLAnything/sparql.anything/sparql-anything-cli/target/sparql-anything-0.8.0-SNAPSHOT.jar "1" "json" "test" <TMP_FOLDER>

SPARQL_ANYTHING_JAR=$1
RESULTS_DIR=$(pwd)/$4
TMP_FOLDER=$5

if [ ! -d $RESULTS_DIR ]; then
  mkdir $RESULTS_DIR
else
  echo "$RESULTS_DIR alredy exists!"
fi

if [ ! -d $TMP_FOLDER ]; then
  mkdir $TMP_FOLDER
else
  echo "$TMP_FOLDER alredy exists!"
fi

source functions.sh

if [ -n "$6" ]; then
  QUERIES_TO_EXECUTE=$6
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
      # echo "Monitoring q$query strategy0 slice size $size $format"
      # monitor-query $size "q$query" "strategy0" "slice" $format
      echo "Monitoring q$query strategy1 slice size $size $format"
      monitor-query $size "q$query" "strategy1" "slice" $format

      # ON_DISK
      # echo "Monitoring q$query strategy0 no_slice size $size $format ondisk"
      # monitor-query $size "q$query" "strategy0" "no_slice" $format "ondisk"
      echo "Monitoring q$query strategy1 no_slice size $size $format ondisk"
      monitor-query $size "q$query" "strategy1" "no_slice" $format $TMP_FOLDER
      # echo "Monitoring q$query strategy0 slice size $size $format ondisk"
      # monitor-query $size "q$query" "strategy0" "slice" $format "ondisk"
      # echo "Monitoring q$query strategy1 slice size $size $format ondisk"
      # monitor-query $size "q$query" "strategy1" "slice" $format "ondisk"

    done
  done
done






#cd $SPARQL_ANYTHING_QUERY_FOLDER

#java -jar $SPARQL_ANYTHING_JAR -q q1.sparql > /dev/null
#java -jar /Users/lgu/workspace/spice/sparql.anything/sparql-anything-cli/target/sparql-anything-0.7.0-SNAPSHOT.jar -q
