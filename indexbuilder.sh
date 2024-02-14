#!/bin/bash

if [ $# -ne 1 ]
then
    echo "Usage: $0 <input_data_file>"
    exit 1
fi

input_data_file=$1

if [ ! -e "$input_data_file" ]
then
    echo "Input data file does not exist: $input_data_file"
    exit 1
fi

python3 pylucene_indexer.py $input_data_file