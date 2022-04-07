#!/bin/bash
#/Users/lgu/workspace/spice/sparql.anything/sparql-anything-cli/target/sparql-anything-0.7.0-SNAPSHOT.jar
SPARQL_ANYTHING_JAR=$1
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

  cd $1
  STRATEGY=$3
  SLICE=$4
  QUERY=$2
  FORMAT=$5
  QUERY_FILE=$2-${FORMAT}-${STRATEGY}-${SLICE}.sparql

  MEM_FILE="$RESULTS_DIR/mem_${QUERY}_${FORMAT}"
  TIME_FILE="$RESULTS_DIR/time_${QUERY}_${FORMAT}"

  if [[ ! -f $MEM_FILE ]]; then
    echo -e "Query InputSize Strategy Slice MemoryLimit Run PID %cpu %mem vsz rss" >> $MEM_FILE
    echo -e "Query\tInputSize\tStrategy\tSlice\tMemoryLimit\tRun\tTime\tUnit\tStatus\tSTDErr" >> $TIME_FILE
  fi

  for mm in "${mem[@]}"
  do
    memory="-Xmx${mm}m"
    total=0

  	for i in 1 2 3
  	do
        echo "$QUERY LIMIT $memory mb - $STRATEGY - $SLICE - SIZE $1 - RUN $i - FORMAT $FORMAT "
        #echo "Start Test $1 $memory $i " >> $MEM_FILE
        MEM_RECORDS=""

        t0=$(gdate +%s%3N)
        #java $memory -jar $SPARQL_ANYTHING_JAR -q $QUERY_FILE > /dev/null &
        java $memory -jar $SPARQL_ANYTHING_JAR -q $QUERY_FILE 2>ERR_FILE > /dev/null &
        MPID=$!
        #errcho "Monitoring $MPID"
        #Timeout??
        while kill -0 $MPID 2> /dev/null;  do
          MEM_RECORDS+="$QUERY $1 $STRATEGY $SLICE $mm RUN$i $(ps -p $MPID -o pid,%cpu,%mem,vsz,rss|sed 1d)\n"
          #echo -e "$QUERY $1 $STRATEGY $SLICE $mm RUN$i $(ps -p $MPID -o pid,%cpu,%mem,vsz,rss|sed 1d)" >> $MEM_FILE
          sleep 0.1
        done
  	   	t1=$(gdate +%s%3N)
        echo -e -n $MEM_RECORDS >> $MEM_FILE
        #echo $ERR
        if [[ "$(cat ERR_FILE)" == *"Error"* ]]; then
          STATUS="Error"
        else
          STATUS="OK"
        fi

  	   	total=$(($total+$t1-$t0))
        TIME_RUN="$QUERY\t$1\t$STRATEGY\t$SLICE\t$mm\tRUN$i\t$(($t1-$t0))\tms\t$STATUS\t$(cat ERR_FILE)"
  	   	echo -e $TIME_RUN >> $TIME_FILE
        echo -e $TIME_RUN
        #echo -e "\n\n" >> $MEM_FILE
        sleep 1
  	done
    AVG="$QUERY\t$1\t$STRATEGY\t$SLICE\t$mm\tAVERAGE\t$(($total/3))\tms"
    echo -e $AVG >> $TIME_FILE
    echo -e $AVG
    rm ERR_FILE
  done

  sed 's/ \{1,\}/\t/g' $MEM_FILE > $MEM_FILE~
  rm $MEM_FILE
  mv $MEM_FILE~ $MEM_FILE
  cd ..

}
#monitor-query 10 "q1" "strategy1" "no_slice"
#monitor-query 1 "q1" "strategy1" "no_slice" "csv"
#monitor-query 1 "q1" "strategy1" "no_slice" "json"
#exit

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
