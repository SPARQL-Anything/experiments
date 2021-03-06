#!/bin/bash

declare -a mem=( "4096" "1024" "512" "256" )


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

  MEM_FILE="$RESULTS_DIR/mem_${QUERY}_${FORMAT}.tsv"
  TIME_FILE="$RESULTS_DIR/time_${QUERY}_${FORMAT}.tsv"

  if [[ ! -f $MEM_FILE ]]; then
    echo -e "Query InputSize Strategy Slice MemoryLimit Run PID %cpu %mem vsz rss" >> $MEM_FILE
    echo -e "Query\tInputSize\tStrategy\tSlice\tMemoryLimit\tRun\tTime\tUnit\tStatus\tSTDErr" >> $TIME_FILE
  fi

  for mm in "${mem[@]}"
  do
    memory="-Xmx${mm}m"
    total=0

    RUN_CNT=0

  	for i in 1 2 3
  	do
        echo "$(date): $QUERY LIMIT $memory mb - $STRATEGY - $SLICE - SIZE $1 - RUN $i - FORMAT $FORMAT "

        MEM_RECORDS=""
        if [[ -f ERR_FILE ]]; then
          rm ERR_FILE
        fi

        t0=$(gdate +%s%3N)
        CNT=0
        java $memory -jar $SPARQL_ANYTHING_JAR -q $QUERY_FILE 2>>ERR_FILE > /dev/null &
        MPID=$!
        while kill -0 $MPID 2> /dev/null;  do
          MEM_RECORDS+="$QUERY $1 $STRATEGY $SLICE $mm RUN$i $(ps -p $MPID -o pid,%cpu,%mem,vsz,rss|sed 1d)\n"
          CNT=$((CNT+1))
          if [[ "$CNT" -eq 1500 ]]; then
            echo "Error: Timeout 300s" >> ERR_FILE
            echo "Error: Timeout 300s"
            kill $MPID 2> /dev/null
            break
          fi
          sleep 0.2
        done

  	   	t1=$(gdate +%s%3N)
        RUN_CNT=$((RUN_CNT+1))
        echo -e -n $MEM_RECORDS >> $MEM_FILE
        #echo $ERR
        if  [[ "$(cat ERR_FILE)" == *"Error"* ]]   ; then
          STATUS="Error"
        elif [[ "$(cat ERR_FILE)" == *"Exception"* ]] ; then
          STATUS="Exception"
        else
          STATUS="OK"
        fi

  	   	total=$(($total+$t1-$t0))
        TIME_RUN="$QUERY\t$1\t$STRATEGY\t$SLICE\t$mm\tRUN$i\t$(($t1-$t0))\tms\t$STATUS\t$(cat ERR_FILE)"
  	   	echo -e $TIME_RUN >> $TIME_FILE
        echo -e $TIME_RUN
        sleep 1

        if [[ "$(cat ERR_FILE)" == *"Timeout"* ]]; then
          break
        fi

        if [[ "$(cat ERR_FILE)" == *"OutOfMemoryError"* ]]; then
          echo "OutOfMemoryError"
          break
        fi

        if [[ "$(cat ERR_FILE)" == *"Exception"* ]]; then
          echo "Exception"
          break
        fi


  	done
    AVG="$QUERY\t$1\t$STRATEGY\t$SLICE\t$mm\tAVERAGE\t$(($total/RUN_CNT))\tms"


    echo -e $AVG >> $TIME_FILE
    echo -e $AVG

    if [[ "$(cat ERR_FILE)" == *"Timeout"* ]]; then
      AVG+="\tKilledForTimeout"
      break
    fi

    if [[ "$(cat ERR_FILE)" == *"OutOfMemoryError"* ]]; then
      AVG+="\tKilledForOutOfMemory"
      break
    fi

    if [[ "$(cat ERR_FILE)" == *"Exception"* ]]; then
      AVG+="\tKilledForException"
      break
    fi

  done

  sed 's/ \{1,\}/\t/g' $MEM_FILE > $MEM_FILE~
  rm $MEM_FILE
  mv $MEM_FILE~ $MEM_FILE
  cd ..

}

function monitor-query-singlerun-notimeout {

  cd $1
  STRATEGY=$3
  SLICE=$4
  QUERY=$2
  FORMAT=$5
  QUERY_FILE=$2-${FORMAT}-${STRATEGY}-${SLICE}.sparql
  MEMORY=$6

  MEM_FILE="$RESULTS_DIR/mem_${QUERY}_${FORMAT}.tsv"
  TIME_FILE="$RESULTS_DIR/time_${QUERY}_${FORMAT}.tsv"

  if [[ ! -f $MEM_FILE ]]; then
    echo -e "Query InputSize Strategy Slice MemoryLimit PID %cpu %mem vsz rss" >> $MEM_FILE
    echo -e "Query\tInputSize\tStrategy\tSlice\tMemoryLimit\tTime\tUnit\tStatus\tSTDErr" >> $TIME_FILE
  fi

  total=0

  RUN_CNT=0

  echo "$(date): $QUERY LIMIT $MEMORY mb - $STRATEGY - $SLICE - SIZE $1 - FORMAT $FORMAT "

  MEM_RECORDS=""
  if [[ -f ERR_FILE ]]; then
      rm ERR_FILE
  fi

  t0=$(gdate +%s%3N)
  java $MEMORY -jar $SPARQL_ANYTHING_JAR -q $QUERY_FILE 2>>ERR_FILE > /dev/null &
  MPID=$!
  while kill -0 $MPID 2> /dev/null;  do
    MEM_RECORDS+="$QUERY $1 $STRATEGY $SLICE $MEMORY $(ps -p $MPID -o pid,%cpu,%mem,vsz,rss|sed 1d)\n"
    sleep 0.2
  done
  t1=$(gdate +%s%3N)
  echo -e -n $MEM_RECORDS >> $MEM_FILE
  if [ "$(cat ERR_FILE)" == *"Error"* ] || [ "$(cat ERR_FILE)" == *"Exception"* ] ; then
      STATUS="Error"
  else
      STATUS="OK"
  fi
  if [[ "$(cat ERR_FILE)" == *"OutOfMemoryError"* ]]; then
    break
  fi
  total=$(($total+$t1-$t0))
  TIME_RUN="$QUERY\t$1\t$STRATEGY\t$SLICE\t$MEMORY\t$(($t1-$t0))\tms\t$STATUS\t$(cat ERR_FILE)"
  echo -e $TIME_RUN >> $TIME_FILE
  echo -e $TIME_RUN
  sleep 1

  sed 's/ \{1,\}/\t/g' $MEM_FILE > $MEM_FILE~
  rm $MEM_FILE
  mv $MEM_FILE~ $MEM_FILE
  cd ..

}
