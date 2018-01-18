#!/bin/bash
# Functions and env variable for working with aeternity
#
# You just need to set EPOCH_HOME and have a normal config there and
# the scripts will do the rest for you.
export EPOCH_HOME=~/projects/aeternity/src/epoch/_build/local/rel/epoch/
export AE_LOCAL_PORT=`cat $EPOCH_HOME/epoch.yaml|grep -A1 http: | grep port|awk -F ':' '{print $2}' | sed -s 's/ //g'`
export AE_LOCAL_INTERNAL_PORT=`cat $EPOCH_HOME/epoch.yaml|grep -A6 http: | grep -A1 internal| grep port|awk -F ':' '{print $2}' | sed -s 's/ //g'`

alias aepub_key="curl -s http://127.0.0.1:$AE_LOCAL_INTERNAL_PORT/v2/account/pub-key|jq '.pub_key'|sed -e 's/\"//g'"
alias aeupdate_pub_key="export AE_PUB_KEY=`aepub_key`"
aeupdate_pub_key
alias aecd="cd $EPOCH_HOME"
alias aebalance="curl -sG http://127.0.0.1:3013/v2/account/balance --data-urlencode '\"pub_key=$AE_PUB_KEY\"'|jq .balance"

function aespend-tx {
    if [ "$#" -ne 3 ]; then
	echo "Usage: aespend-tx recipient_pub_key amount fee"
    else
	curl -X POST -H "Content-Type: application/json" -d '{"recipient_pubkey":"$1", "amount":$2, "fee":$3}' http://127.0.0.1:3113/v2/spend-tx
    fi
}

