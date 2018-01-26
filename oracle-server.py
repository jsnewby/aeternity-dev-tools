#!/usr/bin/python

"""
A class for aeternity oracle clients and servers.
Author: John Newby

(c) Ape Unit 2018
"""

from oracle import Oracle
import sys

oracle = Oracle()
def respond(data):
    oracle.respond(data['payload']['query_id'], 5, "Response!")

query_format, response_format, query_fee, ttl, fee = sys.argv[1:6]
oracle_id = oracle.register(query_format, response_format, query_fee, ttl, fee)
oracle.subscribe(oracle_id, respond)
