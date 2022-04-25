#!/bin/bash
#/Users/lgu/workspace/spice/sparql.anything/sparql-anything-cli/target/sparql-anything-0.7.0-SNAPSHOT.jar
SPARQL_ANYTHING_JAR=$1
RESULTS_DIR=$(pwd)/measures

if [ ! -d $RESULTS_DIR ]; then
  mkdir $RESULTS_DIR
else
  echo "$RESULTS_DIR alredy exists!"
fi


#declare -a mem=( "4096" "1024" "512" "256" )
#
#
#function errcho {
#    >&2 echo "$@"
#}
#
#function monitor-query {
#
#  cd $1
#  STRATEGY=$3
#  SLICE=$4
#  QUERY=$2
#  FORMAT=$5
#  QUERY_FILE=$2-${FORMAT}-${STRATEGY}-${SLICE}.sparql
#
#  MEM_FILE="$RESULTS_DIR/mem_${QUERY}_${FORMAT}.tsv"
#  TIME_FILE="$RESULTS_DIR/time_${QUERY}_${FORMAT}.tsv"
#
#  if [[ ! -f $MEM_FILE ]]; then
#    echo -e "Query InputSize Strategy Slice MemoryLimit Run PID %cpu %mem vsz rss" >> $MEM_FILE
#    echo -e "Query\tInputSize\tStrategy\tSlice\tMemoryLimit\tRun\tTime\tUnit\tStatus\tSTDErr" >> $TIME_FILE
#  fi
#
#  for mm in "${mem[@]}"
#  do
#    memory="-Xmx${mm}m"
#    total=0
#
#    RUN_CNT=0
#
#  	for i in 1 2 3
#  	do
#        echo "$(date): $QUERY LIMIT $memory mb - $STRATEGY - $SLICE - SIZE $1 - RUN $i - FORMAT $FORMAT "
#        #echo "Start Test $1 $memory $i " >> $MEM_FILE
#        MEM_RECORDS=""
#
#        if [[ -f ERR_FILE ]]; then
#          rm ERR_FILE
#        fi
#
#        t0=$(gdate +%s%3N)
#        #java $memory -jar $SPARQL_ANYTHING_JAR -q $QUERY_FILE > /dev/null &
#
#        CNT=0
#        java $memory -jar $SPARQL_ANYTHING_JAR -q $QUERY_FILE 2>>ERR_FILE > /dev/null &
#        MPID=$!
#        while kill -0 $MPID 2> /dev/null;  do
#          MEM_RECORDS+="$QUERY $1 $STRATEGY $SLICE $mm RUN$i $(ps -p $MPID -o pid,%cpu,%mem,vsz,rss|sed 1d)\n"
#          #echo -e "$QUERY $1 $STRATEGY $SLICE $mm RUN$i $(ps -p $MPID -o pid,%cpu,%mem,vsz,rss|sed 1d)" >> $MEM_FILE
#          CNT=$((CNT+1))
#          if [[ "$CNT" -eq 1500 ]]; then
#            echo "Error: Timeout 300s" >> ERR_FILE
#            echo "Error: Timeout 300s"
#            kill $MPID 2> /dev/null
#            break
#          fi
#          sleep 0.2
#        done
#
#  	   	t1=$(gdate +%s%3N)
#        RUN_CNT=$((RUN_CNT+1))
#        echo -e -n $MEM_RECORDS >> $MEM_FILE
#        #echo $ERR
#        if [[ "$(cat ERR_FILE)" == *"Error"* ]]; then
#          STATUS="Error"
#        else
#          STATUS="OK"
#        fi
#
#        if [[ "$(cat ERR_FILE)" == *"Timeout"* ]]; then
#          break
#        fi
#
#        if [[ "$(cat ERR_FILE)" == *"OutOfMemoryError"* ]]; then
#          break
#        fi
#
#  	   	total=$(($total+$t1-$t0))
#        TIME_RUN="$QUERY\t$1\t$STRATEGY\t$SLICE\t$mm\tRUN$i\t$(($t1-$t0))\tms\t$STATUS\t$(cat ERR_FILE)"
#  	   	echo -e $TIME_RUN >> $TIME_FILE
#        echo -e $TIME_RUN
#        #echo -e "\n\n" >> $MEM_FILE
#        sleep 1
#  	done
#    AVG="$QUERY\t$1\t$STRATEGY\t$SLICE\t$mm\tAVERAGE\t$(($total/RUN_CNT))\tms"
#
#    if [[ "$(cat ERR_FILE)" == *"Timeout"* ]]; then
#      AVG+="\tKilledForTimeout"
#      break
#    fi
#
#    if [[ "$(cat ERR_FILE)" == *"OutOfMemoryError"* ]]; then
#      AVG+="\tKilledForOutOfMemory"
#      break
#    fi
#
#    echo -e $AVG >> $TIME_FILE
#    echo -e $AVG
#
#  done
#
#  sed 's/ \{1,\}/\t/g' $MEM_FILE > $MEM_FILE~
#  rm $MEM_FILE
#  mv $MEM_FILE~ $MEM_FILE
#  cd ..
#
#}
#monitor-query 10 "q1" "strategy1" "no_slice"
#monitor-query 1 "q1" "strategy1" "no_slice" "csv"
#monitor-query 100 "q8" "strategy0" "slice" "csv"
#monitor-query 1000 "q9" "strategy0" "slice" "csv"
#exit

source functions.sh

for format in $3
do
  for size in $2
  do
    for query in {1..18}
    do
      echo "Monitoring q$query strategy0 no_slice size $size $format"
      monitor-query $size "q$query" "strategy0" "no_slice" $format
      echo "Monitoring q$query strategy1 no_slice size $size $format"
      monitor-query $size "q$query" "strategy1" "no_slice" $format
      echo "Monitoring q$query strategy0 slice size $size $format"
      monitor-query $size "q$query" "strategy0" "slice" $format
      echo "Monitoring q$query strategy1 slice size $size $format"
      monitor-query $size "q$query" "strategy1" "slice" $format
    done
  done
done






#cd $SPARQL_ANYTHING_QUERY_FOLDER

#java -jar $SPARQL_ANYTHING_JAR -q q1.sparql > /dev/null
#java -jar /Users/lgu/workspace/spice/sparql.anything/sparql-anything-cli/target/sparql-anything-0.7.0-SNAPSHOT.jar -q
