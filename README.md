# aeternity-dev-tools

## Introduction

This repo is for tools and notes for working with aeternity when you're running an epoch node on your local machine.

## aeternity-functions.sh

This script is intended to be called from your .bashrc like this:

`. /path/to/aeternity-functions.sh`

It will parse your `epoch.yaml` (clumsily, needs improvement), and set the environment variables `AE_LOCAL_PORT` and `AE_LOCAL_INTERNAL_PORT`. It has a dependency on [jq] (https://stedolan.github.io/jq/).

### Functions and aliases provided, variables exported

`aepub_key` calls the internal port and parses the result, returning the public key.
`aeupdate_pub_key` exports the result of calling `aepub_key` into the variable `AE_PUB_KEY`.
`aecd` changes to the epoch working directory.
`aebalance` returns the current balance.
`aespend-tx` transfers given currency to a pub key, with fee (`aespend-tx recipient amount fee`)

`AE_PUB_KEY` is exported for general use.

## Python classes

There are two classes useful for writing Oracle and AENS (naming system) applications, and some test classes which demonstrate them.

This code is very much a work in progress. Feedback welcomed.

### Oracle

This class implements class for Oracle clients and servers. The files `oracle-client.py` and `oracle-server.py` demonstrate this. This code is extremely verbose at the moment.

##### Server example usage
Starts a server with request type 'foo2' and response type 'bar2', a query fee of 0, ttl of 100 and the resulting fee is 5 æons (= 4 + 1 per 1000 ttl units)
```
$ ./oracle-server.py 'foo2' 'bar2' 0 100 5
{"target": "oracle", "action": "register", "payload": {"type": "OracleRegisterTxObject", "vsn": 1, "account": "akKf3HQR8BgozbyhuoEgDRHD4RA5cpt9XF99UKUbGmYCAhGbEyg2dYRwhn7866pVSxeNAMQvmSFPz2Qs8ZVHddoF7N7n9CF", "query_format": "foo2", "response_format": "bar2", "query_fee": 0, "ttl": {"type": "delta", "value": 100}, "fee": 5}}
Height: 423
Height: 423
Height: 424
{'action': 'mined_block', 'origin': 'miner', 'payload': {'height': 424, 'hash': 'bh$NjSd7Nc8RK3HZuCrphENDWrtjDFm3hXfK5Ym2i7kHYqFuAihL'}}
{'action': 'subscribe', 'origin': 'oracle', 'payload': {'result': 'ok', 'subscribed_to': {'oracle_id': 'ok$3Kf3HQR8BgozbyhuoEgDRHD4RA5cpt9XF99UKUbGmYCAhGbEyg2dYRwhn7866pVSxeNAMQvmSFPz2Qs8ZVHddoF7N7n9CF', 'type': 'query'}}}
{'action': 'mined_block', 'origin': 'miner', 'payload': {'height': 425, 'hash': 'bh$2oejcGmAVzNQ5tozkBBGMefckkv6WBvKr6Rk2wXvJnEGq6gNrM'}}
{'action': 'mined_block', 'origin': 'miner', 'payload': {'height': 426, 'hash': 'bh$KAMkbZ7zJYPHGMf6v2uxEv5nTNde4uDy4jDJGt7xhedUQbhsv'}}
{'action': 'mined_block', 'origin': 'miner', 'payload': {'height': 427, 'hash': 'bh$2AmwfjofaZWC4LBDyhryCQszyVYjAiX5DN91PM514E45hy4gYs'}}
{'action': 'mined_block', 'origin': 'miner', 'payload': {'height': 428, 'hash': 'bh$NnJBGXmSxBvQP5npzSUhkuM2wkfYoy38CMfAX7rytMASS2P7v'}}
{'action': 'new_oracle_query', 'origin': 'node', 'payload': {'sender': 'ak$3Kf3HQR8BgozbyhuoEgDRHD4RA5cpt9XF99UKUbGmYCAhGbEyg2dYRwhn7866pVSxeNAMQvmSFPz2Qs8ZVHddoF7N7n9CF', 'query': 'foo5', 'query_id': 'oq$VACEnx7C3su5xHjSuDLR15NNUaCgdQwMRADeSfxEGZ5VVWcNC'}}
{"target": "oracle", "action": "response", "payload": {"type": "OracleResponseTxObject", "vsn": 1, "query_id": "oq$VACEnx7C3su5xHjSuDLR15NNUaCgdQwMRADeSfxEGZ5VVWcNC", "fee": 5, "response": "Response!"}}
{'action': 'response', 'origin': 'oracle', 'payload': {'result': 'ok', 'query_id': 'oq$VACEnx7C3su5xHjSuDLR15NNUaCgdQwMRADeSfxEGZ5VVWcNC'}}
```

#### Client example usage

This uses the Oracle id returned above to send a query. The parameters are the query fee (we overpaid, as the Oracle costs 0), request ttl, response ttl, total fee, and the query itself.

```
$ ./oracle-client.py 'ok$3Kf3HQR8BgozbyhuoEgDRHD4RA5cpt9XF99UKUbGmYCAhGbEyg2dYRwhn7866pVSxeNAMQvmSFPz2Qs8ZVHddoF7N7n9CF' 1 5 5 6 "foo5"
{"target": "oracle", "action": "query", "payload": {"type": "OracleQueryTxObject", "vsn": 1, "oracle_pubkey": "ok$3Kf3HQR8BgozbyhuoEgDRHD4RA5cpt9XF99UKUbGmYCAhGbEyg2dYRwhn7866pVSxeNAMQvmSFPz2Qs8ZVHddoF7N7n9CF", "query_fee": 1, "query_ttl": {"type": "delta", "value": 5}, "response_ttl": {"type": "delta", "value": 5}, "fee": 6, "query": "foo5"}}
{"action":"query","origin":"oracle","payload":{"result":"ok","query_id":"oq$VACEnx7C3su5xHjSuDLR15NNUaCgdQwMRADeSfxEGZ5VVWcNC"}}
{"target": "oracle", "action": "subscribe", "payload": {"type": "response", "query_id": "oq$VACEnx7C3su5xHjSuDLR15NNUaCgdQwMRADeSfxEGZ5VVWcNC"}}
{'action': 'subscribe', 'origin': 'oracle', 'payload': {'result': 'ok', 'subscribed_to': {'query_id': 'oq$VACEnx7C3su5xHjSuDLR15NNUaCgdQwMRADeSfxEGZ5VVWcNC', 'type': 'response'}}}
{'action': 'mined_block', 'origin': 'miner', 'payload': {'height': 428, 'hash': 'bh$NnJBGXmSxBvQP5npzSUhkuM2wkfYoy38CMfAX7rytMASS2P7v'}}
{'action': 'mined_block', 'origin': 'miner', 'payload': {'height': 429, 'hash': 'bh$cMA143KtqkfFHQLtrqbQh7D86zg9mD3VBF3uCH5K8cPH1vvRT'}}
{'action': 'new_oracle_response', 'origin': 'node', 'payload': {'query_id': 'oq$VACEnx7C3su5xHjSuDLR15NNUaCgdQwMRADeSfxEGZ5VVWcNC', 'response': 'Response!'}}
{'query_id': 'oq$VACEnx7C3su5xHjSuDLR15NNUaCgdQwMRADeSfxEGZ5VVWcNC', 'response': 'Response!'}
```


