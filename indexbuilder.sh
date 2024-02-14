#!/bin/bash

if [ $# -ne 1 ]
then
    echo "Usage: $0 <input_data_dir>"
    exit 1
fi

input_data_dir=$1

if [ ! -d "$input_data_dir" ]
then
    echo "Input directory does not exist: $input_data_dir"
    exit 1
fi

python3 pylucene_indexer.py $input_data_dir