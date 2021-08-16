#!/bin/bash

set -e
 
MODELS=$(find -name "*.blend")
NUM_MODELS=$(echo -e "$MODELS" | wc -l)
NUM_VALID=0

for model in $MODELS
do
  VALID="false"
  MESSAGE=$(./assertlocal $model) && VALID="true"
  if [[ $VALID == "true" ]];
  then
     NUM_VALID=$(($NUM_VALID + 1))
  else 
     echo "Invalid : $MESSAGE : $model"  
  fi
done

echo "Num valid models: $NUM_VALID /  $NUM_MODELS"

if [[ $NUM_VALID != $NUM_MODELS ]]
then
  exit 1
fi
