#!/usr/bin/env bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PARENTDIR="$( dirname "$DIR" )"
export PYTHONPATH=$PYTHONPATH:$PARENTDIR
echo $PYTHONPATH
python3 -m cbr_db.bankform "$@"
