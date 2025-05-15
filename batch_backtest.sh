#!/bin/bash

STRATEGY="AggressiveRSIStrategy"
DOCKER_NAME="freqtrade"
PAST_PERIODS=("20240101-20240401" "20240301-20240501" "20250101-20250501")

for PERIOD in "${PAST_PERIODS[@]}"
do
    echo "Running backtest for period $PERIOD ..."
    docker exec -it $DOCKER_NAME freqtrade backtesting \
        --strategy $STRATEGY \
        --timerange $PERIOD \
        --export trades
done

