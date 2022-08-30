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

SPARQL_ANYTHING_JAR=$1
RESULTS_DIR=$(pwd)/$2

if [ ! -d $RESULTS_DIR ]; then
  mkdir $RESULTS_DIR
else
  echo "$RESULTS_DIR alredy exists!"
fi

source functions.sh


monitor-query 1 "q15" "strategy0" "slice" "json" "ondisk"

#monitor-query 1 "q1" "strategy0" "no_slice" "json" "ondisk"

#monitor-query 1 "q1" "strategy1" "slice" "csv"
#monitor-query 1 "q2" "strategy1" "slice" "csv"
#monitor-query 1 "q3" "strategy1" "slice" "csv"
#monitor-query 1 "q5" "strategy1" "slice" "csv"
#monitor-query 1 "q7" "strategy0" "no_slice" "csv"
#monitor-query 1 "q8" "strategy0" "slice" "csv"
#monitor-query 1 "q9" "strategy1" "no_slice" "csv"
#monitor-query 1 "q11" "strategy1" "no_slice" "csv"
#monitor-query 1 "q12" "strategy0" "no_slice" "csv"
#monitor-query 1 "q13" "strategy0" "no_slice" "csv"
#monitor-query 1 "q13" "strategy1" "no_slice" "csv"
#monitor-query 1 "q14" "strategy0" "no_slice" "csv"
#monitor-query 1 "q14" "strategy1" "slice" "csv"
#monitor-query 1 "q15" "strategy0" "no_slice" "csv"
#monitor-query 1 "q15" "strategy1" "no_slice" "csv"
#monitor-query 1 "q15" "strategy1" "slice" "csv"
#monitor-query 1 "q16" "strategy1" "slice" "csv"
#monitor-query 1 "q16" "strategy0" "slice" "csv"
#monitor-query 1 "q17" "strategy0" "no_slice" "csv"
#monitor-query 1 "q18" "strategy0" "slice" "csv"
#
#monitor-query 10 "q1" "strategy1" "slice" "csv"
#monitor-query 10 "q2" "strategy0" "no_slice" "csv"
#monitor-query 10 "q2" "strategy1" "no_slice" "csv"
#monitor-query 10 "q2" "strategy1" "slice" "csv"
#monitor-query 10 "q4" "strategy0" "slice" "csv"
#monitor-query 10 "q4" "strategy1" "slice" "csv"
#monitor-query 10 "q5" "strategy0" "slice" "csv"
#monitor-query 10 "q7" "strategy1" "no_slice" "csv"
#monitor-query 10 "q7" "strategy0" "slice" "csv"
#monitor-query 10 "q9" "strategy0" "no_slice" "csv"
#monitor-query 10 "q11" "strategy0" "slice" "csv"
#monitor-query 10 "q11" "strategy1" "slice" "csv"
#monitor-query 10 "q12" "strategy1" "no_slice" "csv"
#monitor-query 10 "q12" "strategy0" "slice" "csv"
#monitor-query 10 "q13" "strategy1" "no_slice" "csv"
#monitor-query 10 "q13" "strategy0" "slice" "csv"
#monitor-query 10 "q14" "strategy1" "no_slice" "csv"
#monitor-query 10 "q15" "strategy1" "no_slice" "csv"
#monitor-query 10 "q16" "strategy0" "slice" "csv"
#monitor-query 10 "q18" "strategy0" "slice" "csv"
#monitor-query 10 "q18" "strategy1" "slice" "csv"
#
#monitor-query 100 "q1" "strategy1" "slice" "csv"
#monitor-query 100 "q3" "strategy0" "no_slice" "csv"
#monitor-query 100 "q3" "strategy1" "slice" "csv"
#monitor-query 100 "q5" "strategy0" "slice" "csv"
#monitor-query 100 "q6" "strategy1" "slice" "csv"
#monitor-query 100 "q7" "strategy0" "slice" "csv"
#monitor-query 100 "q7" "strategy1" "slice" "csv"
#monitor-query 100 "q8" "strategy1" "no_slice" "csv"
#monitor-query 100 "q10" "strategy0" "no_slice" "csv"
#monitor-query 100 "q12" "strategy0" "no_slice" "csv"
#monitor-query 100 "q13" "strategy0" "slice" "csv"
#monitor-query 100 "q15" "strategy1" "no_slice" "csv"
#monitor-query 100 "q16" "strategy0" "no_slice" "csv"
#monitor-query 100 "q18" "strategy1" "no_slice" "csv"
#monitor-query 100 "q18" "strategy1" "slice" "csv"

#monitor-query 1000 "q12" "strategy0" "no_slice" "csv"

#monitor-query 1 "q1" "strategy0" "no_slice" "json"
#monitor-query 1 "q1" "strategy1" "slice" "json"
#monitor-query 1 "q2" "strategy0" "slice" "json"
#monitor-query 1 "q6" "strategy0" "no_slice" "json"
#monitor-query 1 "q7" "strategy0" "slice" "json"
#monitor-query 1 "q8" "strategy0" "slice" "json"
#monitor-query 1 "q10" "strategy0" "no_slice" "json"
#monitor-query 1 "q12" "strategy0" "slice" "json"
#monitor-query 1 "q15" "strategy1" "no_slice" "json"
#monitor-query 1 "q15" "strategy0" "slice" "json"
#
#monitor-query 10 "q1" "strategy1" "no_slice" "json"
#monitor-query 10 "q2" "strategy0" "no_slice" "json"
#monitor-query 10 "q2" "strategy0" "slice" "json"
#monitor-query 10 "q3" "strategy0" "slice" "json"
#monitor-query 10 "q3" "strategy1" "slice" "json"
#monitor-query 10 "q9" "strategy0" "no_slice" "json"
#monitor-query 10 "q9" "strategy1" "no_slice" "json"
#monitor-query 10 "q11" "strategy0" "no_slice" "json"
#monitor-query 10 "q11" "strategy0" "slice" "json"
#monitor-query 10 "q16" "strategy0" "no_slice" "json"
#
#monitor-query 100 "q1" "strategy0" "no_slice" "json"
#monitor-query 100 "q2" "strategy0" "slice" "json"
#monitor-query 100 "q4" "strategy0" "slice" "json"
#monitor-query 100 "q7" "strategy0" "slice" "json"
#monitor-query 100 "q7" "strategy1" "slice" "json"
#monitor-query 100 "q8" "strategy1" "no_slice" "json"
#monitor-query 100 "q8" "strategy0" "slice" "json"
#monitor-query 100 "q9" "strategy1" "slice" "json"
#monitor-query 100 "q10" "strategy1" "slice" "json"
#monitor-query 100 "q11" "strategy1" "no_slice" "json"
#monitor-query 100 "q11" "strategy1" "slice" "json"
#monitor-query 100 "q13" "strategy1" "no_slice" "json"
#monitor-query 100 "q13" "strategy0" "slice" "json"
#monitor-query 100 "q14" "strategy0" "no_slice" "json"
#monitor-query 100 "q14" "strategy1" "no_slice" "json"
#monitor-query 100 "q14" "strategy0" "slice" "json"
#monitor-query 100 "q14" "strategy1" "slice" "json"
#monitor-query 100 "q15" "strategy1" "no_slice" "json"
#monitor-query 100 "q15" "strategy1" "slice" "json"
#monitor-query 100 "q16" "strategy1" "slice" "json"
#monitor-query 100 "q17" "strategy0" "no_slice" "json"
#monitor-query 100 "q17" "strategy1" "no_slice" "json"
#monitor-query 100 "q18" "strategy0" "no_slice" "json"
#monitor-query 100 "q18" "strategy0" "slice" "json"
#
#monitor-query 1000 "q1" "strategy0" "no_slice" "json"
#monitor-query 1000 "q1" "strategy0" "slice" "json"
#monitor-query 1000 "q1" "strategy1" "slice" "json"
#monitor-query 1000 "q2" "strategy0" "no_slice" "json"
#monitor-query 1000 "q2" "strategy1" "no_slice" "json"
#monitor-query 1000 "q3" "strategy0" "no_slice" "json"
#monitor-query 1000 "q3" "strategy1" "no_slice" "json"
#monitor-query 1000 "q4" "strategy1" "slice" "json"
#monitor-query 1000 "q7" "strategy0" "no_slice" "json"
#monitor-query 1000 "q8" "strategy0" "no_slice" "json"
#monitor-query 1000 "q9" "strategy0" "no_slice" "json"
#monitor-query 1000 "q9" "strategy0" "slice" "json"
#monitor-query 1000 "q9" "strategy1" "slice" "json"
#monitor-query 1000 "q10" "strategy0" "no_slice" "json"
#monitor-query 1000 "q11" "strategy0" "no_slice" "json"
#monitor-query 1000 "q11" "strategy1" "no_slice" "json"
#monitor-query 1000 "q12" "strategy0" "no_slice" "json"
#monitor-query 1000 "q13" "strategy0" "no_slice" "json"
#monitor-query 1000 "q13" "strategy0" "slice" "json"
#monitor-query 1000 "q14" "strategy0" "no_slice" "json"
#monitor-query 1000 "q15" "strategy0" "no_slice" "json"
#monitor-query 1000 "q15" "strategy1" "no_slice" "json"
#monitor-query 1000 "q16" "strategy0" "no_slice" "json"
#monitor-query 1000 "q17" "strategy0" "no_slice" "json"
#monitor-query 1000 "q17" "strategy0" "slice" "json"
#monitor-query 1000 "q18" "strategy0" "no_slice" "json"

#monitor-query 100 "q9" "strategy0" "no_slice" "json"

#monitor-query-singlerun-notimeout 1000 "q1" "strategy0" "slice" "csv" "-Xmx4096m"
#monitor-query-singlerun-notimeout 1000 "q1" "strategy1" "slice" "csv" "-Xmx4096m"
#monitor-query-singlerun-notimeout 1000 "q3" "strategy1" "no_slice" "csv" "-Xmx4096m"
#monitor-query-singlerun-notimeout 1000 "q8" "strategy1" "no_slice" "csv" "-Xmx4096m"

#monitor-query-singlerun-notimeout 1000 "q8" "strategy0" "slice" "csv" "-Xmx4096m"
#monitor-query-singlerun-notimeout 1000 "q8" "strategy1" "slice" "csv" "-Xmx4096m"
#monitor-query-singlerun-notimeout 1000 "q9" "strategy0" "slice" "csv" "-Xmx4096m"
#monitor-query-singlerun-notimeout 1000 "q9" "strategy1" "slice" "csv" "-Xmx4096m"

#monitor-query-singlerun-notimeout 1000 "q10" "strategy0" "slice" "csv" "-Xmx4096m"
#monitor-query-singlerun-notimeout 1000 "q10" "strategy1" "slice" "csv" "-Xmx4096m"
#monitor-query-singlerun-notimeout 1000 "q12" "strategy0" "slice" "csv" "-Xmx4096m"
#monitor-query-singlerun-notimeout 1000 "q12" "strategy1" "slice" "csv" "-Xmx4096m"
#monitor-query-singlerun-notimeout 1000 "q13" "strategy1" "no_slice" "csv" "-Xmx4096m"
#monitor-query-singlerun-notimeout 1000 "q14" "strategy0" "slice" "csv" "-Xmx4096m"
#monitor-query-singlerun-notimeout 1000 "q14" "strategy1" "slice" "csv" "-Xmx4096m"
#monitor-query-singlerun-notimeout 1000 "q16" "strategy0" "slice" "csv" "-Xmx4096m"
#monitor-query-singlerun-notimeout 1000 "q16" "strategy1" "slice" "csv" "-Xmx4096m"
#monitor-query-singlerun-notimeout 1000 "q17" "strategy0" "slice" "csv" "-Xmx4096m"
#monitor-query-singlerun-notimeout 1000 "q17" "strategy1" "slice" "csv" "-Xmx4096m"
