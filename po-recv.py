#!/usr/bin/python

"""Simple post office for aeternity. 

Usage: po-get.py post_office

Sends mail via post_office to recipient consisting of body

Author: John Newby

(c) Ape Unit 2018

"""

import json
from oracle import Oracle
import sys

oracle = Oracle()

oracle_pubkey = sys.argv[1]

query = json.dumps({"action": "recv"})
query_id = oracle.query(oracle_pubkey, 0, 5, 5, 3, query)
oracle.subscribe_query(query_id)

