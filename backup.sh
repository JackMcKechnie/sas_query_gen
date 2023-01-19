#!/bin/bash
DATE=$(date +"%d-%b-%Y-%H:%M")

SRCDIR="./query_gen_results"
DESTDIR="../../backup/"

tar -cvf ./query_gen_results/$DATE.tar.gz ./query_gen_results
mv ./query_gen_results/*.tar.gz ./backups