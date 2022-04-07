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
    echo "Processing $QUERY_TEMPLATE_FILE"

    sed -e "s/%size/$size/g" -e "s/%strategy/0/g" -e "s/%slice/false/g" $QUERY_TEMPLATE_FILE > $size/"q$query-strategy0-no_slice.sparql"
    sed -e "s/%size/$size/g" -e "s/%strategy/1/g" -e "s/%slice/false/g" $QUERY_TEMPLATE_FILE > $size/"q$query-strategy1-no_slice.sparql"
    sed -e "s/%size/$size/g" -e "s/%strategy/0/g" -e "s/%slice/true/g" $QUERY_TEMPLATE_FILE > $size/"q$query-strategy0-slice.sparql"
    sed -e "s/%size/$size/g" -e "s/%strategy/1/g" -e "s/%slice/true/g" $QUERY_TEMPLATE_FILE > $size/"q$query-strategy1-slice.sparql"

  done
done
