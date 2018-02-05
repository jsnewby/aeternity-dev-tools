= The Python classes for accessing Oracles =

== Introduction ==

These classes present an OO Python interface to the Oracles interface of the æternity blockchain.

== General Usage ==

The Python classes expect the following environment variables:

```
AE_LOCAL_PORT
AE_LOCAL_INTERNAL_PORT
AE_WEBSOCKET
```

== Server usage ==

```
from oracle import Oracle
import sys

oracle = Oracle()
def respond(data):
    oracle.respond(data['payload']['query_id'], 5, "Response!")

query_format, response_format, query_fee, ttl, fee = sys.argv[1:6]
oracle_id = oracle.register(query_format, response_format, query_fee, ttl, fee)
oracle.subscribe(oracle_id, respond)

```

query_fee can be zero, and fee is calculated at 4 + 1 per 1000 ttl units

the `respond` callback will be invoked whenever a request is received. The response message is used to give a response to the client. Fees for this are 2 + 1 per 1000 ttl.

Sample output:

```
{"target": "oracle", "action": "register", "payload": {"type": "OracleRegisterTxObject", "vsn": 1, "account": "akYFhGwtmmFwo6x3p3dPjy6Qzhkc4eDYHcRe8uTUHG3BxUpX6dhwm3cFCMHjZ5T9QZtmy1iNWWmaV8cTsmjxPu5Xbn1zKyS", "query_format": "foo2", "response_format": "bar2", "query_fee": 1, "ttl": {"type": "delta", "value": 10}, "fee": 4}}
{'hash': 'bh$93WHfWtQNAW2UEiarQrjSqRts94WawvZxpdetRkK713gRy8ae', 'height': 11, 'nonce': 16610995362795444235, 'pow': [1354, 2707, 3759, 4685, 6699, 7279, 9076, 10810, 11588, 11765, 12084, 12192, 13043, 13155, 14016, 14156, 15210, 15654, 15763, 16118, 16158, 16255, 16718, 16980, 17086, 18170, 18342, 18449, 19115, 19392, 19706, 20176, 21571, 23140, 23638, 24807, 25100, 25745, 25909, 27219, 28473, 29876], 'prev_hash': 'bh$gdWRyG9hJd2UQvZxLejAN2jhJbFshjUcprSaQLKBYZRWB92vU', 'state_hash': 'bs$Ah57vofAaHRpLjPCtodf14bcMTghmi9rwZzf7UyWZPkCREnNx', 'target': 537537628, 'time': 1517480508740, 'txs_hash': 'bx$rKHYeMWYUvN547MCwNF5VdcLCohkaB1oCfNuJGeVcGvMviyWj', 'version': 5}
{'hash': 'bh$kABgxJWSUb3AuQ2iK8E7A8YMDT7BQNqD6ZWP7teMCn4qU9trp', 'height': 12, 'nonce': 14693118216982891171, 'pow': [375, 544, 1428, 1964, 2834, 3326, 4800, 4888, 5349, 6836, 9316, 9895, 9900, 10839, 11137, 11462, 11972, 12610, 13145, 16588, 17257, 17497, 17641, 18097, 19177, 19219, 20093, 21444, 21468, 22207, 23471, 23998, 24354, 24443, 25183, 25785, 26057, 29413, 29438, 31943, 32163, 32186], 'prev_hash': 'bh$93WHfWtQNAW2UEiarQrjSqRts94WawvZxpdetRkK713gRy8ae', 'state_hash': 'bs$VT1ihaNMwLqvCUSAhrAxUZdZo8Nfs7AzdCU5DaKC5WHjSAQn2', 'target': 538353343, 'time': 1517480548297, 'txs_hash': 'bx$tddLrTYL9WT6j1xLmPhuw5k37Adh43TdreyTT2WPiAhwR6N4z', 'version': 5}
{'action': 'mined_block', 'origin': 'miner', 'payload': {'height': 12, 'hash': 'bh$kABgxJWSUb3AuQ2iK8E7A8YMDT7BQNqD6ZWP7teMCn4qU9trp'}}
{'action': 'subscribe', 'origin': 'oracle', 'payload': {'result': 'ok', 'subscribed_to': {'oracle_id': 'ok$3YFhGwtmmFwo6x3p3dPjy6Qzhkc4eDYHcRe8uTUHG3BxUpX6dhwm3cFCMHjZ5T9QZtmy1iNWWmaV8cTsmjxPu5Xbn1zKyS', 'type': 'query'}}}
```

From the output, what is important is the oracle_id, which can be used by clients to query this oracle.

And the response:

```
{'action': 'new_oracle_query', 'origin': 'node', 'payload': {'sender': 'ak$3YFhGwtmmFwo6x3p3dPjy6Qzhkc4eDYHcRe8uTUHG3BxUpX6dhwm3cFCMHjZ5T9QZtmy1iNWWmaV8cTsmjxPu5Xbn1zKyS', 'query': 'foo5', 'query_id': 'oq$q4ZWKeFwtCFwUzDuAE7xttBsoZRihjwBcTqfVuRgaubMYtd3s'}}
{"target": "oracle", "action": "response", "payload": {"type": "OracleResponseTxObject", "vsn": 1, "query_id": "oq$q4ZWKeFwtCFwUzDuAE7xttBsoZRihjwBcTqfVuRgaubMYtd3s", "fee": 5, "response": "Response!"}}
{'action': 'response', 'origin': 'oracle', 'payload': {'result': 'ok', 'query_id': 'oq$q4ZWKeFwtCFwUzDuAE7xttBsoZRihjwBcTqfVuRgaubMYtd3s'}}
```

== Client usage

```
from oracle import Oracle
import sys

oracle = Oracle()

oracle_pubkey, query_fee, query_ttl, response_ttl, fee, query = sys.argv[1:7]
query_id = oracle.query(oracle_pubkey, query_fee, query_ttl, response_ttl,
                        fee, query)
oracle.subscribe_query(query_id)
```

Sample usage:

```
newby@bigly:~/backup/projects/aeternity/dev-tools$ ./oracle-client.py 'ok$3YFhGwtmmFwo6x3p3dPjy6Qzhkc4eDYHcRe8uTUHG3BxUpX6dhwm3cFCMHjZ5T9QZtmy1iNWWmaV8cTsmjxPu5Xbn1zKyS' 1 5 5 10 "foo5"
{"target": "oracle", "action": "query", "payload": {"type": "OracleQueryTxObject", "vsn": 1, "oracle_pubkey": "ok$3YFhGwtmmFwo6x3p3dPjy6Qzhkc4eDYHcRe8uTUHG3BxUpX6dhwm3cFCMHjZ5T9QZtmy1iNWWmaV8cTsmjxPu5Xbn1zKyS", "query_fee": 1, "query_ttl": {"type": "delta", "value": 5}, "response_ttl": {"type": "delta", "value": 5}, "fee": 10, "query": "foo5"}}
{"action":"query","origin":"oracle","payload":{"result":"ok","query_id":"oq$2q6BWRU9FVAYixjP2ZQpHmCPxBSDRhK5gVuarpJwetcS6H8zPN"}}
{"target": "oracle", "action": "subscribe", "payload": {"type": "response", "query_id": "oq$2q6BWRU9FVAYixjP2ZQpHmCPxBSDRhK5gVuarpJwetcS6H8zPN"}}
{'action': 'subscribe', 'origin': 'oracle', 'payload': {'result': 'ok', 'subscribed_to': {'query_id': 'oq$2q6BWRU9FVAYixjP2ZQpHmCPxBSDRhK5gVuarpJwetcS6H8zPN', 'type': 'response'}}}
{'action': 'mined_block', 'origin': 'miner', 'payload': {'height': 64, 'hash': 'bh$2npJWKZ1u1e5pjZcwywZRh6FobtmPFTK3RpincLPWVdeqvYSZ5'}}
{'action': 'mined_block', 'origin': 'miner', 'payload': {'height': 65, 'hash': 'bh$oAAAEkmEZgHSFqyjChnnkdmy1a9DMTAQL5j263nsdjxMoBzgr'}}
{'action': 'new_oracle_response', 'origin': 'node', 'payload': {'query_id': 'oq$2q6BWRU9FVAYixjP2ZQpHmCPxBSDRhK5gVuarpJwetcS6H8zPN', 'response': 'Response!'}}
{'query_id': 'oq$2q6BWRU9FVAYixjP2ZQpHmCPxBSDRhK5gVuarpJwetcS6H8zPN', 'response': 'Response!'}
```


