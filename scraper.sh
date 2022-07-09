#!/usr/bin/env bash
# Run to make readme and make git flow, add, commit, push to github

if [[ $# != 2 ]];
then
    echo "USAGE: $0 project_id option"
    echo "Options: 0: New Readme, 1: Apend to readme"
else
    echo "Doing readme"
    python main.py $1 $2
fi