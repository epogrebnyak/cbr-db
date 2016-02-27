#!/usr/bin/env bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PARENTDIR="$( dirname "$DIR" )"
export PYTHONPATH=$PYTHONPATH:$PARENTDIR
export CBR_DB_SETTINGS=settings
python3 -m cbr_db.bankform "$@"
