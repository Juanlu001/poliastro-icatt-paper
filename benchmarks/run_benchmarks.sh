#!/usr/bin/env bash
#
# Runs several iterations of benchmarks with different parameters
#
# Author: Juan Luis Cano Rodríguez <juanlu001@gmail.com>
#

# http://redsymbol.net/articles/unofficial-bash-strict-mode/
set -euo pipefail
IFS=$' \n\t'

BENCHMARKS_DIR=$HOME/Development/Python/poliastro.org/icatt/poliastro-icatt-paper/benchmarks
BENCHMARK_SCRIPT=$BENCHMARKS_DIR/test_benchmark.py
RESULTS_DIR=$BENCHMARKS_DIR/benchmark_nounits

WARMUP="on off"
NUMBA_JIT="1 0"

mkdir -p $RESULTS_DIR

for warmup in $WARMUP; do
    for jit in $NUMBA_JIT; do
        for ii in 0; do  # No need to run more
            NUMBA_DISABLE_JIT=$jit py.test $BENCHMARK_SCRIPT --benchmark-only --benchmark-save-data \
              --benchmark-warmup $warmup --benchmark-json="$RESULTS_DIR/benchmark-${ii}-${warmup}-${jit}.json"
        done
    done
done
