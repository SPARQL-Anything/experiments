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

# ./generate_queries.sh "1 10 100 1000" "<TEMP_FOLDER>"
SA_QUERIES=sparql-anything-query-templates
SA_CONSTRUCT=sparql-anything-construct-templates
TMP_FOLDER="$2/"


if [ ! -d $TMP_FOLDER ]; then
  mkdir $TMP_FOLDER
  echo "Folder $TMP_FOLDER created!"
else
  echo "$TMP_FOLDER alredy exists!"
fi

for size in $1
do
  if [ ! -d $size ]; then
    mkdir $size
  else
    echo "$size alredy exists!"
  fi

  #for QUERY_FILE in "$SA_QUERIES"/q*
  for query in {1..18}
  do

    #filename="$(basename -- $QUERY_FILE)"
    #filename="q$query.sparql"
    QUERY_TEMPLATE_FILE=$SA_QUERIES/"q$query.sparql"
    # QUERY_TEMPLATE_FILE_XML=$SA_QUERIES/"q${query}_xml.sparql"
    echo "Processing $QUERY_TEMPLATE_FILE"

    # CSV
    sed -e "s/%size/$size/g" -e "s/%strategy/0/g" -e "s/%slice/false/g" -e "s/%format/csv/g" -e "s/%param/csv.headers=true/g" $QUERY_TEMPLATE_FILE > $size/"q$query-csv-strategy0-no_slice.sparql"
    sed -e "s/%size/$size/g" -e "s/%strategy/1/g" -e "s/%slice/false/g" -e "s/%format/csv/g" -e "s/%param/csv.headers=true/g"  $QUERY_TEMPLATE_FILE > $size/"q$query-csv-strategy1-no_slice.sparql"
    # sed -e "s/%size/$size/g" -e "s/%strategy/0/g" -e "s/%slice/true/g" -e "s/%format/csv/g" -e "s/%param/csv.headers=true/g"  $QUERY_TEMPLATE_FILE > $size/"q$query-csv-strategy0-slice.sparql"
    sed -e "s/%size/$size/g" -e "s/%strategy/1/g" -e "s/%slice/true/g" -e "s/%format/csv/g" -e "s/%param/csv.headers=true/g"  $QUERY_TEMPLATE_FILE > $size/"q$query-csv-strategy1-slice.sparql"

    ## CSV ON DISK
    # sed -e "s/%size/$size/g" -e "s/%strategy/0/g" -e "s/%slice/false/g" -e "s/%format/json/g" -e "s~%param~blank-nodes=true,ondisk=${TMP_FOLDER}~g" $QUERY_TEMPLATE_FILE > $size/"q$query-csv-strategy0-no_slice-ondisk.sparql"
    sed -e "s/%size/$size/g" -e "s/%strategy/1/g" -e "s/%slice/false/g" -e "s/%format/json/g" -e "s~%param~blank-nodes=true,ondisk=${TMP_FOLDER}/q$query-csv-strategy1-no_slice-ondisk~g"  $QUERY_TEMPLATE_FILE > $size/"q$query-csv-strategy1-no_slice-ondisk.sparql"
    # sed -e "s/%size/$size/g" -e "s/%strategy/0/g" -e "s/%slice/true/g" -e "s/%format/json/g" -e "s~%param~blank-nodes=true,ondisk=${TMP_FOLDER}~g"  $QUERY_TEMPLATE_FILE > $size/"q$query-csv-strategy0-slice-ondisk.sparql"
    # sed -e "s/%size/$size/g" -e "s/%strategy/1/g" -e "s/%slice/true/g" -e "s/%format/json/g" -e "s~%param~blank-nodes=true,ondisk=${TMP_FOLDER}~g"  $QUERY_TEMPLATE_FILE > $size/"q$query-csv-strategy1-slice-ondisk.sparql"

    # JSON
    sed -e "s/%size/$size/g" -e "s/%strategy/0/g" -e "s/%slice/false/g" -e "s/%format/json/g" -e "s/%param/blank-nodes=true/g" $QUERY_TEMPLATE_FILE > $size/"q$query-json-strategy0-no_slice.sparql"
    sed -e "s/%size/$size/g" -e "s/%strategy/1/g" -e "s/%slice/false/g" -e "s/%format/json/g" -e "s/%param/blank-nodes=true/g"  $QUERY_TEMPLATE_FILE > $size/"q$query-json-strategy1-no_slice.sparql"
    # sed -e "s/%size/$size/g" -e "s/%strategy/0/g" -e "s/%slice/true/g" -e "s/%format/json/g" -e "s/%param/blank-nodes=true/g"  $QUERY_TEMPLATE_FILE > $size/"q$query-json-strategy0-slice.sparql"
    sed -e "s/%size/$size/g" -e "s/%strategy/1/g" -e "s/%slice/true/g" -e "s/%format/json/g" -e "s/%param/blank-nodes=true/g"  $QUERY_TEMPLATE_FILE > $size/"q$query-json-strategy1-slice.sparql"

    ## JSON ON DISK
    # sed -e "s/%size/$size/g" -e "s/%strategy/0/g" -e "s/%slice/false/g" -e "s/%format/json/g" -e "s~%param~blank-nodes=true,ondisk=${TMP_FOLDER}~g" $QUERY_TEMPLATE_FILE > $size/"q$query-json-strategy0-no_slice-ondisk.sparql"
    sed -e "s/%size/$size/g" -e "s/%strategy/1/g" -e "s/%slice/false/g" -e "s/%format/json/g" -e "s~%param~blank-nodes=true,ondisk=${TMP_FOLDER}/q$query-json-strategy1-no_slice-ondisk~g"  $QUERY_TEMPLATE_FILE > $size/"q$query-json-strategy1-no_slice-ondisk.sparql"
    # sed -e "s/%size/$size/g" -e "s/%strategy/0/g" -e "s/%slice/true/g" -e "s/%format/json/g" -e "s~%param~blank-nodes=true,ondisk=${TMP_FOLDER}~g"  $QUERY_TEMPLATE_FILE > $size/"q$query-json-strategy0-slice-ondisk.sparql"
    # sed -e "s/%size/$size/g" -e "s/%strategy/1/g" -e "s/%slice/true/g" -e "s/%format/json/g" -e "s~%param~blank-nodes=true,ondisk=${TMP_FOLDER}~g"  $QUERY_TEMPLATE_FILE > $size/"q$query-json-strategy1-slice-ondisk.sparql"


  done
done


echo "Generating SPARQL CONSTRUCTS"
for size in $1
do

  QUERY_TEMPLATE_FILE=$SA_CONSTRUCT/"c1.sparql"
  query=1
  echo "Processing $QUERY_TEMPLATE_FILE"

  # CSV
  sed -e "s/%size/$size/g" -e "s/%strategy/0/g" -e "s/%slice/false/g" -e "s/%format/csv/g" -e "s/%param/csv.headers=true/g" $QUERY_TEMPLATE_FILE > $size/"c$query-csv-strategy0-no_slice.sparql"
  sed -e "s/%size/$size/g" -e "s/%strategy/1/g" -e "s/%slice/false/g" -e "s/%format/csv/g" -e "s/%param/csv.headers=true/g"  $QUERY_TEMPLATE_FILE > $size/"c$query-csv-strategy1-no_slice.sparql"
  # sed -e "s/%size/$size/g" -e "s/%strategy/0/g" -e "s/%slice/true/g" -e "s/%format/csv/g" -e "s/%param/csv.headers=true/g"  $QUERY_TEMPLATE_FILE > $size/"c$query-csv-strategy0-slice.sparql"
  sed -e "s/%size/$size/g" -e "s/%strategy/1/g" -e "s/%slice/true/g" -e "s/%format/csv/g" -e "s/%param/csv.headers=true/g"  $QUERY_TEMPLATE_FILE > $size/"c$query-csv-strategy1-slice.sparql"

  ## CSV ON DISK
  # sed -e "s/%size/$size/g" -e "s/%strategy/0/g" -e "s/%slice/false/g" -e "s/%format/json/g" -e "s~%param~blank-nodes=true,ondisk=${TMP_FOLDER}~g" $QUERY_TEMPLATE_FILE > $size/"c$query-csv-strategy0-no_slice-ondisk.sparql"
  sed -e "s/%size/$size/g" -e "s/%strategy/1/g" -e "s/%slice/false/g" -e "s/%format/json/g" -e "s~%param~blank-nodes=true,ondisk=${TMP_FOLDER}/c$query-csv-strategy1-no_slice-ondisk~g"  $QUERY_TEMPLATE_FILE > $size/"c$query-csv-strategy1-no_slice-ondisk.sparql"
  # sed -e "s/%size/$size/g" -e "s/%strategy/0/g" -e "s/%slice/true/g" -e "s/%format/json/g" -e "s~%param~blank-nodes=true,ondisk=${TMP_FOLDER}~g"  $QUERY_TEMPLATE_FILE > $size/"c$query-csv-strategy0-slice-ondisk.sparql"
  # sed -e "s/%size/$size/g" -e "s/%strategy/1/g" -e "s/%slice/true/g" -e "s/%format/json/g" -e "s~%param~blank-nodes=true,ondisk=${TMP_FOLDER}~g"  $QUERY_TEMPLATE_FILE > $size/"c$query-csv-strategy1-slice-ondisk.sparql"

  # JSON
  sed -e "s/%size/$size/g" -e "s/%strategy/0/g" -e "s/%slice/false/g" -e "s/%format/json/g" -e "s/%param/blank-nodes=true/g" $QUERY_TEMPLATE_FILE > $size/"c$query-json-strategy0-no_slice.sparql"
  sed -e "s/%size/$size/g" -e "s/%strategy/1/g" -e "s/%slice/false/g" -e "s/%format/json/g" -e "s/%param/blank-nodes=true/g"  $QUERY_TEMPLATE_FILE > $size/"c$query-json-strategy1-no_slice.sparql"
  # sed -e "s/%size/$size/g" -e "s/%strategy/0/g" -e "s/%slice/true/g" -e "s/%format/json/g" -e "s/%param/blank-nodes=true/g"  $QUERY_TEMPLATE_FILE > $size/"c$query-json-strategy0-slice.sparql"
  sed -e "s/%size/$size/g" -e "s/%strategy/1/g" -e "s/%slice/true/g" -e "s/%format/json/g" -e "s/%param/blank-nodes=true/g"  $QUERY_TEMPLATE_FILE > $size/"c$query-json-strategy1-slice.sparql"

  ## JSON ON DISK
  # sed -e "s/%size/$size/g" -e "s/%strategy/0/g" -e "s/%slice/false/g" -e "s/%format/json/g" -e "s~%param~blank-nodes=true,ondisk=${TMP_FOLDER}~g" $QUERY_TEMPLATE_FILE > $size/"c$query-json-strategy0-no_slice-ondisk.sparql"
  sed -e "s/%size/$size/g" -e "s/%strategy/1/g" -e "s/%slice/false/g" -e "s/%format/json/g" -e "s~%param~blank-nodes=true,ondisk=${TMP_FOLDER}/c$query-json-strategy1-no_slice-ondisk~g"  $QUERY_TEMPLATE_FILE > $size/"c$query-json-strategy1-no_slice-ondisk.sparql"
  # sed -e "s/%size/$size/g" -e "s/%strategy/0/g" -e "s/%slice/true/g" -e "s/%format/json/g" -e "s~%param~blank-nodes=true,ondisk=${TMP_FOLDER}~g"  $QUERY_TEMPLATE_FILE > $size/"c$query-json-strategy0-slice-ondisk.sparql"
  # sed -e "s/%size/$size/g" -e "s/%strategy/1/g" -e "s/%slice/true/g" -e "s/%format/json/g" -e "s~%param~blank-nodes=true,ondisk=${TMP_FOLDER}~g"  $QUERY_TEMPLATE_FILE > $size/"c$query-json-strategy1-slice-ondisk.sparql"

done
