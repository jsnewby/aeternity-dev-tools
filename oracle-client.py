#!/usr/bin/python

"""
A class for aeternity oracle clients and servers.
Author: John Newby

(c) Ape Unit 2018
"""

from oracle import Oracle
import sys

oracle = Oracle()

oracle_pubkey, query_fee, query_ttl, response_ttl, fee, query = sys.argv[1:7]
query_id = oracle.query(oracle_pubkey, query_fee, query_ttl, response_ttl,
                        fee, query)
oracle.subscribe_query(query_id)
