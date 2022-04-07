#!/bin/bash
SA_QUERIES=sparql-anything-query-templates

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
    QUERY_TEMPLATE_FILE_XML=$SA_QUERIES/"q${query}_xml.sparql"
    echo "Processing $QUERY_TEMPLATE_FILE"

    # CSV
    sed -e "s/%size/$size/g" -e "s/%strategy/0/g" -e "s/%slice/false/g" -e "s/%format/csv/g" -e "s/%param/csv.headers=true/g" $QUERY_TEMPLATE_FILE > $size/"q$query-csv-strategy0-no_slice.sparql"
    sed -e "s/%size/$size/g" -e "s/%strategy/1/g" -e "s/%slice/false/g" -e "s/%format/csv/g" -e "s/%param/csv.headers=true/g"  $QUERY_TEMPLATE_FILE > $size/"q$query-csv-strategy1-no_slice.sparql"
    sed -e "s/%size/$size/g" -e "s/%strategy/0/g" -e "s/%slice/true/g" -e "s/%format/csv/g" -e "s/%param/csv.headers=true/g"  $QUERY_TEMPLATE_FILE > $size/"q$query-csv-strategy0-slice.sparql"
    sed -e "s/%size/$size/g" -e "s/%strategy/1/g" -e "s/%slice/true/g" -e "s/%format/csv/g" -e "s/%param/csv.headers=true/g"  $QUERY_TEMPLATE_FILE > $size/"q$query-csv-strategy1-slice.sparql"

    # JSON
    sed -e "s/%size/$size/g" -e "s/%strategy/0/g" -e "s/%slice/false/g" -e "s/%format/json/g" -e "s/%param/blank-nodes=true/g" $QUERY_TEMPLATE_FILE > $size/"q$query-json-strategy0-no_slice.sparql"
    sed -e "s/%size/$size/g" -e "s/%strategy/1/g" -e "s/%slice/false/g" -e "s/%format/json/g" -e "s/%param/blank-nodes=true/g"  $QUERY_TEMPLATE_FILE > $size/"q$query-json-strategy1-no_slice.sparql"
    sed -e "s/%size/$size/g" -e "s/%strategy/0/g" -e "s/%slice/true/g" -e "s/%format/json/g" -e "s/%param/blank-nodes=true/g"  $QUERY_TEMPLATE_FILE > $size/"q$query-json-strategy0-slice.sparql"
    sed -e "s/%size/$size/g" -e "s/%strategy/1/g" -e "s/%slice/true/g" -e "s/%format/json/g" -e "s/%param/blank-nodes=true/g"  $QUERY_TEMPLATE_FILE > $size/"q$query-json-strategy1-slice.sparql"


    # XML
    sed -e "s/%size/$size/g" -e "s/%strategy/0/g" -e "s/%slice/false/g" -e "s/%format/xml/g" -e "s/%param/blank-nodes=true/g" $QUERY_TEMPLATE_FILE_XML > $size/"q$query-xml-strategy0-no_slice.sparql"
    sed -e "s/%size/$size/g" -e "s/%strategy/1/g" -e "s/%slice/false/g" -e "s/%format/xml/g" -e "s/%param/blank-nodes=true/g"  $QUERY_TEMPLATE_FILE_XML > $size/"q$query-xml-strategy1-no_slice.sparql"
    sed -e "s/%size/$size/g" -e "s/%strategy/0/g" -e "s/%slice/true/g" -e "s/%format/xml/g" -e "s/%param/blank-nodes=true/g"  $QUERY_TEMPLATE_FILE_XML > $size/"q$query-xml-strategy0-slice.sparql"
    sed -e "s/%size/$size/g" -e "s/%strategy/1/g" -e "s/%slice/true/g" -e "s/%format/xml/g" -e "s/%param/blank-nodes=true/g"  $QUERY_TEMPLATE_FILE_XML > $size/"q$query-xml-strategy1-slice.sparql"


  done
done
