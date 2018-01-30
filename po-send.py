#!/usr/bin/python

"""Simple post office for aeternity. 

Usage: po-send.py post_office recipient body

Sends mail via post_office to recipient consisting of body

Author: John Newby

(c) Ape Unit 2018

"""

import json
from oracle import Oracle
import sys

oracle = Oracle()

oracle_pubkey, recipient, body = sys.argv[1:4]

query = json.dumps({"action": "send",
                    "rcpt": recipient,
                    "body": body})

query_id = oracle.query(oracle_pubkey, 0, 5, 5, 3, query)
oracle.subscribe_query(query_id)

