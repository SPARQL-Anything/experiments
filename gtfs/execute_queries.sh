#!/bin/bash

SPARQL_ANYTHING_JAR=/Users/lgu/workspace/spice/sparql.anything/sparql-anything-cli/target/sparql-anything-0.7.0-SNAPSHOT.jar
SPARQL_ANYTHING_QUERY_FOLDER=/Users/lgu/workspace/spice/CogComplexityAndPerformaceEvaluation/gtfs/1
RESULTS_DIR=$(pwd)/measures

if [ ! -d $RESULTS_DIR ]; then
  mkdir $RESULTS_DIR
else
  echo "$RESULTS_DIR alredy exists!"
fi


declare -a mem=("256" "512" "1024" "4096")


function errcho {
    >&2 echo "$@"
}

function monitor-query {

  cd $SPARQL_ANYTHING_QUERY_FOLDER

  MEM_FILE="$RESULTS_DIR/mem_$1"
  TIME_FILE="$RESULTS_DIR/time_$1"

  for mm in "${mem[@]}"
  do
    memory="-Xmx${mm}m"
    total=0

  	for i in 1 2 3
  	do
        echo "$1 LIMIT $memory RUN $i"
        #echo "Start Test $1 $memory $i " >> $MEM_FILE
        t0=$(gdate +%s%3N)
        java $memory -jar $SPARQL_ANYTHING_JAR -q $1 > /dev/null &
        MPID=$!
        #errcho "Monitoring $MPID"
        #Timeout??
        while kill -0 $MPID 2> /dev/null;  do
          echo -e "$1 $mm RUN$i $(ps -p $MPID -o pid,%cpu,%mem,vsz,rss|sed 1d)" >> $MEM_FILE
          sleep 0.1
        done
  	   	t1=$(gdate +%s%3N)
  	   	total=$(($total+$t1-$t0))
        TIME_RUN="$1\t$mm\tRUN$i\t$(($t1-$t0))\tms"
  	   	echo -e $TIME_RUN >> $TIME_FILE
        echo -e $TIME_RUN
        #echo -e "\n\n" >> $MEM_FILE
        sleep 1
  	done
    AVG="$1\t$mm\tAVERAGE\t$(($total/3))\tms"
    echo -e $AVG >> $TIME_FILE
    echo -e $AVG
  done

  sed 's/ \{1,\}/\t/g' $MEM_FILE > $MEM_FILE~
  rm $MEM_FILE
  mv $MEM_FILE~ $MEM_FILE

}

monitor-query q1.sparql

#cd $SPARQL_ANYTHING_QUERY_FOLDER

#java -jar $SPARQL_ANYTHING_JAR -q q1.sparql > /dev/null
#java -jar /Users/lgu/workspace/spice/sparql.anything/sparql-anything-cli/target/sparql-anything-0.7.0-SNAPSHOT.jar -q
